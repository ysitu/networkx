#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for networkx

You can install networkx with

python setup_egg.py install
"""
from glob import glob
import os
import sys
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

from setuptools import setup, Extension
try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = None

if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'")
    print()

if sys.version_info[:2] < (2, 6):
    print("NetworkX requires Python version 2.6 or later (%d.%d detected)." %
          sys.version_info[:2])
    sys.exit(-1)

# Write the version information.
sys.path.insert(0, 'networkx')
import release
version = release.write_versionfile()
sys.path.pop(0)

packages=["networkx",
          "networkx.algorithms",
          "networkx.algorithms.approximation",
          "networkx.algorithms.assortativity",
          "networkx.algorithms.bipartite",
          "networkx.algorithms.centrality",
          "networkx.algorithms.chordal",
          "networkx.algorithms.community",
          "networkx.algorithms.components",
          "networkx.algorithms.connectivity",
          "networkx.algorithms.flow",
          "networkx.algorithms.isomorphism",
          "networkx.algorithms.link_analysis",
          "networkx.algorithms.operators",
          "networkx.algorithms.partition",
          "networkx.algorithms.shortest_paths",
          "networkx.algorithms.traversal",
          "networkx.algorithms.tree",
          "networkx.classes",
          "networkx.drawing",
          "networkx.external",
          "networkx.external.decorator",
          "networkx.external.metis",
          "networkx.generators",
          "networkx.linalg",
          "networkx.readwrite",
          "networkx.readwrite.json_graph",
          "networkx.testing",
          "networkx.tests",
          "networkx.utils"]

if sys.version_info[0] >= 3:
    packages.append('networkx.external.decorator.decorator3')
else:
    packages.append('networkx.external.decorator.decorator2')

if cythonize:
    libraries = [('gklib',
                  {'sources': glob('networkx/external/metis/src/GKlib/*.c'),
                   'depends': glob('networkx/external/metis/src/GKlib/*.h'),
                   'include_dirs': ['networkx/external/metis/src/GKlib']}),
                 ('metis',
                  {'sources': glob('networkx/external/metis/src/libmetis/*.c'),
                   'depends': glob('networkx/external/metis/src/libmetis/*.h'),
                   'include_dirs': ['networkx/external/metis/src/GKlib',
                                    'networkx/external/metis/src/libmetis']})]
    ext_modules = cythonize([Extension(
        'networkx.external.metis._metis',
        ['networkx/external/metis/*.pyx'],
        include_dirs=['networkx/external/metis/src/GKlib',
                      'networkx/external/metis/src/libmetis'],
        libraries=['metis', 'gklib'])])
else:
    libraries = None
    ext_modules = None

if sys.version_info[:2] < (3, 4):
    install_requires = ['enum34']
else:
    install_requires = None

docdirbase  = 'share/doc/networkx-%s' % version
# add basic documentation
data = [(docdirbase, glob("*.txt"))]
# add examples
for d in ['advanced',
          'algorithms',
          'basic',
          '3d_drawing',
          'drawing',
          'graph',
          'multigraph',
          'pygraphviz',
          'readwrite']:
    dd=os.path.join(docdirbase,'examples',d)
    pp=os.path.join('examples',d)
    data.append((dd,glob(os.path.join(pp,"*.py"))))
    data.append((dd,glob(os.path.join(pp,"*.bz2"))))
    data.append((dd,glob(os.path.join(pp,"*.gz"))))
    data.append((dd,glob(os.path.join(pp,"*.mbox"))))
    data.append((dd,glob(os.path.join(pp,"*.edgelist"))))

# add the tests
package_data     = {
    'networkx': ['tests/*.py'],
    'networkx.algorithms': ['tests/*.py'],
    'networkx.algorithms.approximation': ['tests/*.py'],
    'networkx.algorithms.assortativity': ['tests/*.py'],
    'networkx.algorithms.bipartite': ['tests/*.py'],
    'networkx.algorithms.centrality': ['tests/*.py'],
    'networkx.algorithms.chordal': ['tests/*.py'],
    'networkx.algorithms.community': ['tests/*.py'],
    'networkx.algorithms.components': ['tests/*.py'],
    'networkx.algorithms.connectivity': ['tests/*.py'],
    'networkx.algorithms.flow': ['tests/*.py', 'tests/*.bz2'],
    'networkx.algorithms.isomorphism': ['tests/*.py','tests/*.*99'],
    'networkx.algorithms.link_analysis': ['tests/*.py'],
    'networkx.algorithms.operators': ['tests/*.py'],
    'networkx.algorithms.partition': ['tests/*.py'],
    'networkx.algorithms.shortest_paths': ['tests/*.py'],
    'networkx.algorithms.traversal': ['tests/*.py'],
    'networkx.algorithms.tree': ['tests/*.py'],
    'networkx.classes': ['tests/*.py'],
    'networkx.drawing': ['tests/*.py'],
    'networkx.external.metis': ['tests/*.py'],
    'networkx.generators': ['tests/*.py'],
    'networkx.linalg': ['tests/*.py'],
    'networkx.readwrite': ['tests/*.py'],
    'networkx.readwrite.json_graph': ['tests/*.py'],
    'networkx.testing': ['tests/*.py'],
    'networkx.utils': ['tests/*.py']
    }

if __name__ == "__main__":

    setup(
        name             = release.name.lower(),
        version          = version,
        maintainer       = release.maintainer,
        maintainer_email = release.maintainer_email,
        author           = release.authors['Hagberg'][0],
        author_email     = release.authors['Hagberg'][1],
        description      = release.description,
        keywords         = release.keywords,
        long_description = release.long_description,
        license          = release.license,
        platforms        = release.platforms,
        url              = release.url,
        download_url     = release.download_url,
        classifiers      = release.classifiers,
        packages         = packages,
        libraries        = libraries,
        ext_modules      = ext_modules,
        data_files       = data,
        package_data     = package_data,
        install_requires = install_requires
      )

