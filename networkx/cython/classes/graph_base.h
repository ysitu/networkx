#ifndef NETWORKX_CYTHON_CLASSES_GRAPH_BASE_H
#define NETWORKX_CYTHON_CLASSES_GRAPH_BASE_H

#include <Python.h>
#include <cstddef>

#include "networkx/cython/utils/containers.h"

namespace networkx {
namespace classes {

class GraphBase {
public:
    typedef std::size_t Node;
    typedef std::size_t Edge;

    virtual ~GraphBase() noexcept = default;
};

}  // namespace classes
}  // namespace networkx

#endif  // NETWORKX_CYTHON_CLASSES_GRAPH_BASE_H
