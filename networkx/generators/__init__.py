"""
A package for generating various graphs in networkx.

"""
from .atlas import *
from .bipartite import *
from .classic import *
from .community import *
from .degree_seq import *
from .directed import *
from .ego import *
from .geometric import *
from .hybrid import *
from .intersection import *
from .line import *
from .random_clustered import *
from .random_graphs import *
from .small import *
from .social import *
from .stochastic import *
from .threshold import *

__all__ = sum([atlas.__all__,
               bipartite.__all__,
               classic.__all__,
               community.__all__,
               degree_seq.__all__,
               directed.__all__,
               ego.__all__,
               geometric.__all__,
               hybrid.__all__,
               intersection.__all__,
               line.__all__,
               random_clustered.__all__,
               random_graphs.__all__,
               small.__all__,
               social.__all__,
               stochastic.__all__,
               threshold.__all__
               ], [])
