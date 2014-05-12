#ifndef NETWORKX_CYTHON_ALGORITHMS_CONNECTIVITY_STOER_WAGNER_H
#define NETWORKX_CYTHON_ALGORITHMS_CONNECTIVITY_STOER_WAGNER_H

#include <Python.h>
#include <cstddef>
#include <functional>
#include <stdexcept>
#include <tuple>
#include <utility>
#include <vector>

#include "networkx/cython/algorithms/components/connected.h"
#include "networkx/cython/classes/graph.h"
#include "networkx/cython/utils/containers.h"
#include "networkx/cython/utils/heaps.h"

namespace networkx {
namespace algorithms {
namespace connectivity {

template<typename T>
std::tuple<utils::Vector<classes::Graph::Node>,
           utils::Vector<classes::Graph::Node>>
StoerWagner(classes::Graph G, classes::Graph::EdgeMap<T> w) {
    typedef classes::Graph Graph;
    typedef Graph::Node Node;
    typedef utils::UnorderedSet<Node> NodeSet;
    typedef Graph::Edge Edge;
    struct NodeWeight {
        Node u;
        T w;

        bool operator<(const NodeWeight &other) const {
            return w < other.w;
        }
    };
    typedef utils::PairingHeap<NodeWeight, std::greater<NodeWeight>> Heap;
    typedef typename Heap::NodeRef HeapNodeRef;

    auto &adj = G.adj();
    size_t n = adj.size();
    if (n < 2)
        throw std::invalid_argument("G has less than two nodes.");
    if (!components::IsConnected(G))
        throw std::invalid_argument("G is not connected.");
    for (auto &entry_n : adj)
        for (auto &entry_e : entry_n.second)
            if (w[entry_e.second] < static_cast<T>(0))
                throw std::invalid_argument("G has a negative-weight edge.");

    NodeSet non_reachable;
    for (auto &entry : adj)
        non_reachable.insert(entry.first);
    utils::Vector<std::tuple<Node, Node>> contractions;
    T cut_value;
    std::size_t best_phase = 0;

    for (std::size_t i = 0; i < n - 1; ++i) {
        Node u = adj.begin()->first;
        NodeSet A{u};
        Heap heap;
        Graph::NodeMap<HeapNodeRef> heap_node_refs;
        for (auto &entry : adj.find(u)->second) {
            Node v = entry.first;
            Edge e = entry.second;
            heap_node_refs.insert({v, heap.Insert({v, w[e]})});
        }
        for (size_t j = 0; j < n - i - 2; ++j) {
            u = heap.Pop().u;
            A.insert(u);
            for (auto &entry : adj.find(u)->second) {
                Node v = entry.first;
                Edge e = entry.second;
                if (A.find(v) == A.end()) {
                    auto it = heap_node_refs.find(v);
                    if (it != heap_node_refs.end())
                        heap_node_refs.insert({v, heap.Insert({v, w[e]})});
                    else
                        heap.Modify(it->second, {v, w[e]});
                }
            }
        }
        Node v = heap.Top().u;
        T w = heap.Top().w;
        if (i == 0 || w < cut_value) {
            cut_value = w;
            best_phase = i;
        }
        contractions.emplace_back(u, v);
        for (auto &entry : adj.find(v)->second) {
            Node t = entry.first;
            Edge e = entry.second;
            if (t != u)
                w[G.AddEdge(u, t)] += w[e];
        }
        G.RemoveNode(v);
    }
    G.Clear();
    for (std::size_t i = 0; i < best_phase; ++i)
        G.AddEdge(std::get<0>(contractions[i]), std::get<1>(contractions[i]));
    Node u = std::get<1>(contractions[best_phase]);
    G.AddNode(u);
    NodeSet reachable{u};
    non_reachable.erase(u);
    utils::Queue<Node> queue;
    queue.push(u);
    do {
        u = queue.front();
        queue.pop();
        for (auto &entry : adj.find(u)->second) {
            Node v = entry.first;
            if (reachable.insert(v).second) {
                non_reachable.erase(v);
                queue.push(v);
            }
        }
    } while (!queue.empty());
    return std::make_tuple(
        utils::Vector<Node>(reachable.begin(), reachable.end()),
        utils::Vector<Node>(non_reachable.begin(), non_reachable.end()));
}

}  // namespace connectivity
}  // namespace algorithms
}  // namespace networkx

#endif  // NETWORKX_CYTHON_ALGORITHMS_CONNECTIVITY_STOER_WAGNER_H
