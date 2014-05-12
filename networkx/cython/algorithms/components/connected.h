#ifndef NETWORKX_CYTHON_ALGORITHMS_COMPONENTS_CONNECTED_H
#define NETWORKX_CYTHON_ALGORITHMS_COMPONENTS_CONNECTED_H

#include <Python.h>

#include "networkx/cython/classes/graph.h"

namespace networkx {
namespace algorithms {
namespace components {

bool IsConnected(const classes::Graph &G);

}  // namespace components
}  // namespace algorithms
}  // namespace networkx

#endif  // NETWORKX_CYTHON_ALGORITHMS_COMPONENTS_CONNECTED_H
