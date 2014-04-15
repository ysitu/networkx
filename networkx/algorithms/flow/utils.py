# -*- coding: utf-8 -*-
"""
Utility classes and functions for network flow algorithms.
"""

__author__ = """ysitu <ysitu@users.noreply.github.com>"""
# Copyright (C) 2014 ysitu <ysitu@users.noreply.github.com>
# All rights reserved.
# BSD license.

from collections import deque
from itertools import chain, tee
import networkx as nx

__all__ = ['CurrentEdge', 'Level', 'GlobalRelabelThreshold',
           'build_residual_network', 'build_flow_dict']


class CurrentEdge(object):
    """Mechanism for iterating over out-edges incident to a node in a circular
    manner. StopIteration exception is raised when wraparound occurs.
    """
    __slots__ = ('_edges', '_it', '_curr')

    def __init__(self, edges):
        self._edges = edges
        if self._edges:
            self.rewind()

    def get(self):
        return self._curr

    def move_to_next(self):
        try:
            self._curr = next(self._it)
        except StopIteration:
            self.rewind()
            raise

    def tee(self):
        self._it, it = tee(self._it)
        return chain([self._curr], it)

    def rewind(self):
        self._it = iter(self._edges.items())
        self._curr = next(self._it)


class Level(object):
    """Active and inactive nodes in a level.
    """
    __slots__ = ('active', 'inactive')

    def __init__(self):
        self.active = set()
        self.inactive = set()


class GlobalRelabelThreshold(object):
    """Measurement of work before the global relabeling heuristic should be
    applied.
    """

    def __init__(self, n, m, freq):
        self._threshold = (n + m) / freq if freq else float('inf')
        self._work = 0

    def add_work(self, work):
        self._work += work

    def is_reached(self):
        return self._work >= self._threshold

    def clear_work(self):
        self._work = 0


def build_residual_network(G, s, t, capacity):
    """Build the residual network. Initialize the edge capacities so that they
    correspond to a zero flow.
    """
    if G.is_multigraph():
        raise nx.NetworkXError(
                'MultiGraph and MultiDiGraph not supported (yet).')

    if s not in G:
        raise nx.NetworkXError('node %s not in graph' % str(s))
    if t not in G:
        raise nx.NetworkXError('node %s not in graph' % str(t))
    if s == t:
        raise nx.NetworkXError('source and sink are the same node')

    R = nx.DiGraph()
    R.add_nodes_from(G, excess=0)

    # Extract edges with positive capacities. Self loops excluded.
    edge_list = [(u, v, attr) for u, v, attr in G.edges_iter(data=True)
                 if u != v and (capacity not in attr or attr[capacity] > 0)]
    # Simulate infinity with twice the sum of the finite edge capacities or any
    # positive value if the sum is zero. This allows the infinite-capacity
    # edges to be distinguished for detecting unboundedness. If the maximum
    # flow is finite, these edge still cannot appear in the minimum cut and
    # thus guarantee correctness.
    inf = float('inf')
    inf = 2 * sum(attr[capacity] for u, v, attr in edge_list
                  if capacity in attr and attr[capacity] != inf) or 1
    if G.is_directed():
        for u, v, attr in edge_list:
            r = attr[capacity] if capacity in attr else inf
            if not R.has_edge(u, v):
                # Both (u, v) and (v, u) must be present in the residual
                # network.
                R.add_edge(u, v, capacity=r, flow=0)
                R.add_edge(v, u, capacity=0, flow=0)
            else:
                # The edge (u, v) was added when (v, u) was visited.
                R[u][v]['capacity'] = r
    else:
        for u, v, attr in edge_list:
            # Add a pair of edges with equal residual capacities.
            r = attr[capacity] if capacity in attr else inf
            R.add_edge(u, v, capacity=r, flow=0)
            R.add_edge(v, u, capacity=r, flow=0)

    # Detect unboundedness by determining reachability of t from s using only
    # infinite-capacity edges.
    q = deque([s])
    seen = set([s])
    while q:
        u = q.popleft()
        for v, attr in R[u].items():
            if attr['capacity'] == inf and v not in seen:
                if v == t:
                    raise nx.NetworkXUnbounded(
                            'Infinite capacity path, flow unbounded above.')
                seen.add(v)
                q.append(v)

    return R


def build_flow_dict(G, R):
    """Build a flow dictionary from a residual network.
    """
    flow_dict = {}
    for u in G:
        flow_dict[u] = dict((v, 0) for v in G[u])
        flow_dict[u].update((v, R[u][v]['flow']) for v in R[u]
                            if R[u][v]['flow'] > 0)
    return flow_dict
