#ifndef NETWORKX_CYTHON_CLASSES_GRAPH_H
#define NETWORKX_CYTHON_CLASSES_GRAPH_H

#include <Python.h>
#include <cstddef>
#include <tuple>

#include "networkx/cython/classes/graph_base.h"

namespace networkx {
namespace classes {

class Graph : public GraphBase {
public:
    template<typename V>
    using NodeMap = utils::UnorderedMap<Node, V>;
    template<typename V>
    using EdgeMap = utils::UnorderedMap<Edge, V>;

    typedef NodeMap<Edge> AdjList;
    typedef NodeMap<AdjList> AdjMap;

    virtual ~Graph() noexcept = default;

    void AddNode(Node u);
    void RemoveNode(Node u);
    Edge AddEdge(Node u, Node v);
    Edge RemoveEdge(Node u, Node v);
    const AdjList& Neighbors(Node u) const;
    std::tuple<NodeMap<Node>, EdgeMap<Edge>> Compact();
    void Clear();

    const AdjMap& adj() const { return _adj; }

protected:
    AdjMap _adj;
    Edge _new_edge = static_cast<Edge>(0);
};

}  // namespace classes
}  // namespace networkx

#endif  // NETWORKX_CYTHON_CLASSES_GRAPH_H
