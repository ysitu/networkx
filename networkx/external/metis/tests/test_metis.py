from itertools import chain, cycle, dropwhile, takewhile
from nose import SkipTest
from nose.tools import *


def make_cycle(n):
    xadj = list(range(0, 2 * n + 1, 2))
    adjncy = list(chain.from_iterable(zip(chain([n - 1], range(n - 1)),
                                          chain(range(1, n), [0]))))
    return xadj, adjncy


class TestMetis:

    @classmethod
    def setupClass(cls):
        global node_nd, part_graph, compute_vertex_separator
        try:
            from networkx.external.metis import (node_nd, part_graph,
                                                 compute_vertex_separator)
        except ImportError:
            raise SkipTest('METIS not available.')

    def test_node_nd(self):
        n = 16
        xadj, adjncy = make_cycle(n)
        perm, iperm = node_nd(xadj, adjncy)
        assert_equal(set(perm), set(range(n)))
        assert_equal(abs(perm[-1] - perm[-2]), n // 2)
        ok_(set(range(min(perm[-2:]) + 1, max(perm[-2:]))) in
            (set(perm[0:n // 2 - 1]), set(perm[n // 2 - 1:-2])))
        ok_(all(i == perm[iperm[i]] for i in range(n)))


    def test_selfloops(self):
        n = 16
        xadj = list(range(0, 3 * n + 1, 3))
        adjncy = list(chain.from_iterable(zip(chain([n - 1], range(n - 1)),
                                              range(n),
                                              chain(range(1, n), [0]))))
        perm, iperm = node_nd(xadj, adjncy)
        assert_equal(set(perm), set(range(n)))
        assert_equal(abs(perm[-1] - perm[-2]), n // 2)
        ok_(set(range(min(perm[-2:]) + 1, max(perm[-2:]))) in
            (set(perm[0:n // 2 - 1]), set(perm[n // 2 - 1:-2])))
        ok_(all(i == perm[iperm[i]] for i in range(n)))


    def test_part_graph(self):
        n = 16
        xadj, adjncy = make_cycle(n)
        for recursive in (False, True):
            objval, part = part_graph(xadj, adjncy, 2, recursive=recursive)
            assert_equal(objval, 2)
            assert_equal(set(part), set(range(2)))
            it = dropwhile(lambda x: x == 0, cycle(part))
            assert_equal(list(takewhile(lambda x: x == 1, it)), [1] * (n // 2))

    def test_compute_vertex_separator(self):
        n = 16
        xadj, adjncy = make_cycle(n)
        sepsize, part = compute_vertex_separator(xadj, adjncy)
        assert_equal(sepsize, 2)
        assert_equal(len(part), n)
        part1, part2, sep = (list(filter(lambda i: part[i] == k, range(n)))
                             for k in range(3))
        assert_equal(sorted(part1 + part2 + sep), list(range(n)))
        assert_equal(len(sep), 2)
        assert_equal(abs(sep[1] - sep[0]), n // 2)
        assert_equal(
            sorted(map(sorted, [part1, part2])),
            sorted(map(sorted,
                       [[(sep[0] + i) % n for i in range(1, n // 2)],
                        [(sep[1] + i) % n for i in range(1, n // 2)]])))
