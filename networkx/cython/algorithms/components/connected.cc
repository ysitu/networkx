#include <Python.h>
#include <stdexcept>

#include "networkx/cython/algorithms/components/connected.h"
#include "networkx/cython/classes/graph.h"
#include "networkx/cython/utils/containers.h"

using networkx::classes::Graph;
using networkx::utils::Queue;
using networkx::utils::UnorderedSet;
using std::invalid_argument;

namespace networkx {
namespace algorithms {
namespace components {

bool IsConnected(const Graph &G) {
    auto &adj = G.adj();
    if (adj.empty())
        throw invalid_argument("G is empty.");
    Graph::Node u = adj.begin()->first;
    UnorderedSet<Graph::Node> visited{u};
    Queue<Graph::Node> queue;
    queue.push(u);
    do {
        u = queue.front();
        queue.pop();
        for (auto &entry : adj.find(u)->second) {
            Graph::Node v = entry.first;
            if (visited.insert(v).second)
                queue.push(v);
        }
    } while (!queue.empty());
    return visited.size() == adj.size();
}

}  // namespace components
}  // namespace algorithms
}  // namespace networkx
