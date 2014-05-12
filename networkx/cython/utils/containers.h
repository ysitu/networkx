#ifndef NETWORKX_CYTHON_UTILS_CONTAINERS_H
#define NETWORKX_CYTHON_UTILS_CONTAINERS_H

#include <Python.h>
#include <functional>
#include <deque>
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

#include "networkx/cython/utils/memory.h"

namespace networkx {
namespace utils {

template<typename T>
using Queue = std::queue<T, std::deque<T, PyAllocator<T>>>;

template<typename K, typename V>
using UnorderedMap = std::unordered_map<K, V, std::hash<K>, std::equal_to<K>,
                                        PyAllocator<std::pair<const K, V>>>;

template<typename T>
using UnorderedSet = std::unordered_set<T, std::hash<T>, std::equal_to<T>,
                                        PyAllocator<T>>;

template<typename T>
using Vector = std::vector<T, PyAllocator<T>>;

}  // namespace utils
}  // namespace networkx

#endif // NETWORKX_CYTHON_UTILS_CONTAINERS_H
