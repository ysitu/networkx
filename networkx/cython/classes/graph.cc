#include <Python.h>
#include <stdexcept>
#include <tuple>
#include <utility>

#include "networkx/cython/classes/graph.h"

using std::invalid_argument;
using std::make_tuple;
using std::move;
using std::tuple;

namespace networkx {
namespace classes {

void Graph::AddNode(Node u) {
    _adj[u];
}

void Graph::RemoveNode(Node u) {
    auto it = _adj.find(u);
    if (it == _adj.end())
        throw invalid_argument("u is not in the graph.");
    for (auto &entry : it->second)
        _adj[entry.first].erase(u);
    _adj.erase(it);
}

Graph::Edge Graph::AddEdge(Node u, Node v) {
    auto pair = _adj[u].insert({v, _new_edge});
    if (!pair.second)
        return pair.first->second;
    _adj[v].insert({u, _new_edge});
    return _new_edge++;
}

Graph::Edge Graph::RemoveEdge(Node u, Node v) {
    auto it_u = _adj.find(u);
    if (it_u != _adj.end()) {
        auto &nbrs_u = it_u->second;
        auto it_v = nbrs_u.find(v);
        if (it_v != nbrs_u.end()) {
            Edge e = it_v->second;
            nbrs_u.erase(it_v);
            _adj[v].erase(u);
            return e;
        }
    }
    throw invalid_argument("(u, v) is not in the graph.");
}

const Graph::AdjList& Graph::Neighbors(Node u) const {
    auto it = _adj.find(u);
    if (it == _adj.end())
        throw invalid_argument("u is not in the graph.");
    return it->second;
}

tuple<Graph::NodeMap<Graph::Node>, Graph::EdgeMap<Graph::Edge>>
Graph::Compact() {
    NodeMap<Node> node_map;
    EdgeMap<Edge> edge_map;
    for (auto &entry_n : _adj) {
        node_map.insert({entry_n.first, static_cast<Node>(node_map.size())});
        for (auto &entry_e : entry_n.second)
            edge_map.insert({entry_e.second,
                             static_cast<Edge>(edge_map.size())});
    }
    AdjMap adj;
    for (auto &entry_n : _adj) {
        AdjList nbrs;
        for (auto &entry_e : entry_n.second)
            nbrs.insert({node_map[entry_e.first], edge_map[entry_e.second]});
        adj.insert({node_map[entry_n.first], move(nbrs)});
    }
    _adj = move(adj);
    _new_edge = static_cast<Edge>(_adj.size());
    return make_tuple(move(node_map), move(edge_map));
}

void Graph::Clear() {
    _adj.clear();
    _new_edge = static_cast<Edge>(0);
}

}  // namespace classes
}  // namespace networkx
