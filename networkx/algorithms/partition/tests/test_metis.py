from itertools import chain
from nose import SkipTest
from nose.tools import *

import networkx as nx

class TestMetis:

    @classmethod
    def setupClass(cls):
        try:
            from networkx import (node_nested_dissection, partition,
                                  vertex_separator)
        except ImportError:
            raise SkipTest('METIS not available.')

    def test_node_nested_dissection(self):
        def check_perm(perm):
            assert_equal(set(perm), set(G))
            assert_equal(abs(perm[-1] - perm[-2]), n // 2)
            ok_(set(range(min(perm[-2:]) + 1, max(perm[-2:]))) in
                (set(perm[0: n // 2 - 1]), set(perm[n // 2 - 1:-2])))

        n = 16
        G = nx.cycle_graph(n, create_using=nx.DiGraph())
        check_perm(nx.node_nested_dissection(G))
        G.add_edges_from((i, i) for i in range(n))
        check_perm(nx.node_nested_dissection(G))

    def test_partition(self):
        n = 16
        G = nx.cycle_graph(n)
        for recursive in (False, True):
            # nparts == 1
            objval, parts = nx.partition(G, 1, recursive=recursive)
            assert_equal(objval, 0)
            assert_equal(len(parts), 1)
            assert_equal(sorted(parts[0]), list(range(n)))
            # nparts == 2
            objval, parts = nx.partition(G, 2, recursive=recursive)
            assert_equal(objval, 2)
            assert_equal(len(parts), 2)
            ok_(all(isinstance(part, list) for part in parts))
            ok_(all(len(part) == n // 2 for part in parts))
            assert_equal(sorted(chain.from_iterable(parts)), list(range(n)))
            parts = list(map(sorted, parts))
            ok_(any(abs(part[-1] - part[0]) == n // 2 - 1 for part in parts))

    def test_partition_uneven(self):
        n = 10
        G = nx.cycle_graph(n)
        tpwgts = [[0.2], [0.3], [0.5]]
        ubvec = [1.000001]
        options = nx.MetisOptions()
        options.numbering = 1
        for recursive in (False, True):
            objval, parts = nx.partition(G, 3, tpwgts=tpwgts, ubvec=ubvec,
                                         options=options, recursive=recursive)
            assert_equal(objval, 3)
            assert_equal(list(map(len, parts)), [2, 3, 5])
            assert_equal(options.numbering, 1)

    def test_vertex_separator(self):
        n = 16
        G = nx.cycle_graph(n, create_using=nx.DiGraph())
        sep, part1, part2 = nx.vertex_separator(G)
        ok_(isinstance(sep, list))
        ok_(isinstance(part1, list))
        ok_(isinstance(part2, list))
        assert_equal(sorted(sep + part1 + part2), list(range(n)))
        assert_equal(len(sep), 2)
        assert_equal(abs(sep[1] - sep[0]), n // 2)
        assert_equal(
            sorted(map(sorted, [part1, part2])),
            sorted(map(sorted,
                       [[(sep[0] + i) % n for i in range(1, n // 2)],
                        [(sep[1] + i) % n for i in range(1, n // 2)]])))

    def test_empty_graph(self):
        G = nx.Graph()
        assert_equal(nx.node_nested_dissection(G), [])
        assert_equal(nx.partition(G, 3, recursive=False), (0, [[], [], []]))
        assert_equal(nx.partition(G, 3, recursive=True), (0, [[], [], []]))
        assert_equal(nx.vertex_separator(G), ([], [], []))

    def test_exceptions(self):
        G = nx.complete_graph(5)
        assert_raises(nx.NetworkXError, nx.partition, G, 0)
        assert_raises(nx.NetworkXError, nx.partition, G, 2,
                      tpwgts=[[0.1, 0.2]])
        assert_raises(nx.NetworkXError, nx.partition, G, 2,
                      tpwgts=[[0.1, 0.2], [0.9]])
        assert_raises(nx.NetworkXError, nx.partition, G, 2,
                      tpwgts=[[0.1, 0.2], [0.9, 0.8]], ubvec=[1.1])
