try:
    from ._metis import *
    __all__ = ['part_graph', 'node_nd', 'compute_vertex_separator']
except ImportError:
    pass
