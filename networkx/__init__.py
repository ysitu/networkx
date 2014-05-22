"""
NetworkX
========

    NetworkX (NX) is a Python package for the creation, manipulation, and
    study of the structure, dynamics, and functions of complex networks.

    https://networkx.lanl.gov/

Using
-----

    Just write in Python

    >>> import networkx as nx
    >>> G=nx.Graph()
    >>> G.add_edge(1,2)
    >>> G.add_node(42)
    >>> print(sorted(G.nodes()))
    [1, 2, 42]
    >>> print(sorted(G.edges()))
    [(1, 2)]
"""
#    Copyright (C) 2004-2010 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
#
# Add platform dependent shared library path to sys.path
#

from __future__ import absolute_import

import sys
if sys.version_info[:2] < (2, 6):
    m = "Python version 2.6 or later is required for NetworkX (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])

# Release data
from . import release

__author__ = ('%s <%s>\n%s <%s>\n%s <%s>' %
              (release.authors['Hagberg'] + release.authors['Schult'] +
               release.authors['Swart']))
__license__ = release.license
__date__ = release.date
__version__ = release.version

import networkx
from .exception import *
from . import external, utils
from .algorithms import *
from .classes import *
from .convert import *
from .convert_matrix import *
from .drawing import *
from .generators import *
from .linalg import *
from .readwrite import *
from .relabel import *
from .tests.test import run as test

__all__ = sum([algorithms.__all__,
               classes.__all__,
               convert.__all__,
               convert_matrix.__all__,
               drawing.__all__,
               exception.__all__,
               generators.__all__,
               linalg.__all__,
               readwrite.__all__,
               relabel.__all__,
               ['test']
               ], ['networkx'])
