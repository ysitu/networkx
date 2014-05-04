# -*- coding: utf-8 -*-
"""
Wrappers of METIS graph partitioning functions.
"""

__author__ = """ysitu <ysitu@users.noreply.github.com>"""
# Copyright (C) 2014 ysitu <ysitu@users.noreply.github.com>
# All rights reserved.
# BSD license.

from contextlib import contextmanager
from itertools import chain
from sys import exc_info

import networkx as nx
from networkx.utils import not_implemented_for, convert_exceptions
from networkx.external.metis import *

try:
    from networkx.external.metis import (node_nd, part_graph,
                                         compute_vertex_separator)
    __all__ = ['node_nested_dissection','partition', 'vertex_separator',
               'MetisOptions']
except ImportError:
    __all__ = []


@contextmanager
def _zero_numbering(options):
    if options:
        numbering = options.numbering
        options.numbering = MetisNumbering.zero
    try:
        yield
    finally:
        if options:
            options.numbering = numbering


def _convert_graph(G):
    """Convert a graph to the numbered adjacency list structure expected by
    METIS.
    """
    index = dict(zip(G, range(len(G))))
    xadj = [0]
    adjncy= []
    for u in G:
        adjncy.extend(index[v] for v in G[u])
        xadj.append(len(adjncy))
    return xadj, adjncy


@convert_exceptions(nx.NetworkXError, (ValueError, TypeError, MetisError))
def node_nested_dissection(G, weight='weight', options=None):
    """Compute a node ordering of a graph that reduces fill when the Laplacian
    matrix of the graph is LU factorized. The algorithm aims to minimize the
    sum of weights of vertices in separators computed in the process.

    Parameters
    ----------
    G : NetworkX graph
        A graph.

    weight : object, optional
        The data key used to determine the weight of each node. If None, each
        node has unit weight. Default value: 'weight'.

    options : MetisOptions, optional
        METIS options. If None, the default options are used. Default value:
        None.

    Returns
    -------
    perm : list of nodes
        The node ordering.

    Raises
    ------
    NetworkXError
        If the parameters cannot be converted to valid METIS input format, or
        METIS returns an error status.
    """
    if len(G) == 0:
        return []

    vwgt = [G.node[u].get(weight, 1) for u in G]
    if all(w == 1 for w in vwgt):
        vwgt = None

    if G.is_directed() or G.is_multigraph():
        G = nx.Graph(G.edges_iter())
    xadj, adjncy = _convert_graph(G)

    with _zero_numbering(options):
        perm = node_nd(xadj, adjncy, vwgt, options)[0]

    nodes = list(G)
    perm = [nodes[i] for i in perm]

    return perm


@not_implemented_for('directed')
@not_implemented_for('multigraph')
@convert_exceptions(nx.NetworkXError, (ValueError, TypeError, MetisError))
def partition(G, nparts, node_weight='weight', node_size='size',
              edge_weight='weight', tpwgts=None, ubvec=None, options=None,
              recursive=False):
    """Partition a graph using multilevel recursive bisection or multilevel
    multiway partitioning.

    Parameters
    ----------
    G : NetworkX graph
        An undirected graph.

    nparts : int
        Number of parts to partition the graph. It should be at least 2.

    node_weight : object, optional
        The data key used to determine the weight of each node. If None, each
        node has unit weight. Default value: 'weight'.

    node_size : object, optional
        The data key used to determine the size of each node when computing the
        total communication volumne. If None, each node has unit size. Default
        value: 'size'

    edge_weight : object, optional
        The data key used to determine the weight of each edge. If None, each
        edge has unit weight. Default value: 'weight'.

    tpwgts : list of lists of floats, optional
        The target weights of the partitions and the constraints. The target
        weight of the `i`th partition and the `j`th constraint is given by
        :samp:`tpwgts[i][j]` (the numbering for both partitions and
        constraints starts from zero). For each constraint of the
        :samp:`tpwgts[][]` entries must be 1.0 (i.e.,
        `\sum_i \text{tpwgts}[i][j] = 1.0`)

        If None, the graph is equally divided among the partitions. Default
        value: None.

    ubvec : list of floats, optional
        The allowed load imbalance tolerance for each constraint. For the`i`th
        and the `j`th constraint, the allowed weight is the
        :samp:`ubvect[j] * tpwgts[i][j]` fraction of the `j`th constraint's
        total weight. The load imbalances must be greater 1.0.

        If None, the load imbalance tolerance is 1.001 if there is exactly one
        constraint or 1.01 if there are more. Default value: None.

    options : MetisOptions, optional.
        METIS options. If None, the default options are used. Default value:
        None.

    recursive : bool, optional
        If True, multilevel recursive bisection is used. Otherwise, multileve
        multilevel multiway partitioning is used. Default value: False.

    Returns
    -------
    objval : int
        The edge-cut or the total communication volume of the partitioning
        solution. The value returned depends on the partitioining's objective
        function.

    parts : lists of nodes
        The partitioning.

    Raises
    ------
    NetworkXNotImplemented
        If the graph is directed or is a multigraph.

    NetworkXError
        If the parameters cannot be converted to valid METIS input format, or
        METIS returns an error status.
    """
    if nparts < 1:
        raise nx.NetworkXError('nparts is less than one.')
    if nparts == 1:
        return 0, [list(G)]

    if len(G) == 0:
        return 0, [[] for i in range(nparts)]

    xadj, adjncy = _convert_graph(G)

    vwgt = [G.node[u].get(node_weight, 1) for u in G]
    if all(w == 1 for w in vwgt):
        vwgt = None

    vsize = [G.node[u].get(node_size, 1) for u in G]
    if all(w == 1 for w in vsize):
        vsize = None

    adjwgt = [G[u][v].get(edge_weight, 1) for u in G for v in G[u]]
    if all(w == 1 for w in adjwgt):
        adjwgt = None

    if tpwgts is not None:
        if len(tpwgts) != nparts:
            raise nx.NetworkXError('length of tpwgts is not equal to nparts.')
        ncon = len(tpwgts[0])
        if any(len(tpwgts[j]) != ncon for j in range(1, nparts)):
            raise nx.NetworkXError(
                'lists in tpwgts are not of the same length.')
        if ubvec is not None and len(ubvec) != ncon:
            raise nx.NetworkXError(
                'ubvec is not of the same length as tpwgts.')
        tpwgts = list(chain.from_iterable(tpwgts))

    with _zero_numbering(options):
        objval, part = part_graph(xadj, adjncy, nparts, vwgt, vsize, adjwgt,
                                  tpwgts, ubvec, options, recursive)

    parts = [[] for i in range(nparts)]
    for u, i in zip(G, part):
        parts[i].append(u)

    return objval, parts


@convert_exceptions(nx.NetworkXError, (ValueError, TypeError, MetisError))
def vertex_separator(G, weight='weight', options=None):
    """Compute a vertex separator that bisects a graph. The algorithm aims to
    minimize the sum of weights of vertices in the separator.

    Parameters
    ----------
    G : NetworkX graph
        A graph.

    weight : object, optional
        The data key used to determine the weight of each node. If None, each
        node has unit weight. Default value: 'weight'.

    options : MetisOptions, optional
        METIS options. If None, the default options are used. Default value:
        None.

    Returns
    -------
    sep, part1, part2 : lists of nodes
        The separator and the two parts of the bisection represented as lists.

    Raises
    ------
    NetworkXError
        If the parameters cannot be converted to valid METIS input format, or
        METIS returns an error status.
    """
    if len(G) == 0:
        return [], [], []

    vwgt = [G.node[u].get(weight, 1) for u in G]
    if all(w == 1 for w in vwgt):
        vwgt = None

    if G.is_directed() or G.is_multigraph():
        G = nx.Graph(G.edges_iter())
    xadj, adjncy = _convert_graph(G)


    with _zero_numbering(options):
        part = compute_vertex_separator(xadj, adjncy, vwgt, options)[1]

    groups = [[], [], []]
    for u, i in zip(G, part):
        groups[i].append(u)

    return groups[2], groups[0], groups[1]
