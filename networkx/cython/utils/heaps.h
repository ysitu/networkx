#ifndef NETWORKX_CYTHON_UTILS_HEAPS_H
#define NETWORKX_CYTHON_UTILS_HEAPS_H

#include <Python.h>
#include <cstddef>
#include <algorithm>
#include <functional>

#include "networkx/cython/utils/memory.h"

namespace networkx {
namespace utils {

template<typename T, typename Less = std::less<T>>
class PairingHeap : public PyAllocated {
public:
    class Node : private PyAllocated {
    public:
        T value;

    protected:
        friend class PairingHeap<T, Less>;

        virtual ~Node() noexcept;

        Node* Link(Node *other) noexcept;
        Node* MergeChildren() noexcept;
        void Cut() noexcept;

        Node *left = nullptr;
        Node *next = nullptr;
        Node *prev = nullptr;
        Node *parent = nullptr;
    };

    class NodeRef final {
    public:
        NodeRef(const NodeRef &other) noexcept = default;
        ~NodeRef() noexcept = default;
        NodeRef& operator=(const NodeRef &other) = default;

        const T& operator*() const noexcept { return _node.value; }
        const T* operator->() const noexcept { return &_node.value; }

    private:
        friend class PairingHeap<T, Less>;

        NodeRef(Node &node) : _node(node) { }

        Node &_node;
    };

    PairingHeap() noexcept = default;
    PairingHeap(const PairingHeap<T, Less> &other) = delete;
    PairingHeap& operator=(const PairingHeap<T, Less> &other) = delete;
    virtual ~PairingHeap() noexcept;

    const T& Top() const noexcept { return _root->value; }
    T Pop() noexcept;
    NodeRef Insert(T value);
    void Modify(NodeRef ref, T value) noexcept;

protected:
    Node *_root = nullptr;
};

template<typename T, typename Less>
PairingHeap<T, Less>::Node::~Node() noexcept {
    for (Node *child = left; child != nullptr; child = child->next)
        delete child;
}

template<typename T, typename Less>
typename PairingHeap<T, Less>::Node*
PairingHeap<T, Less>::Node::Link(Node *other) noexcept {
    Node *root = this;
    if (Less()(other->value, root->value))
        std::swap(root, other);
    Node *next = root->left;
    other->next = next;
    if (next != nullptr)
        next->prev = other;
    other->prev = nullptr;
    root->left = other;
    other->parent = root;
    return root;
}

template<typename T, typename Less>
typename PairingHeap<T, Less>::Node*
PairingHeap<T, Less>::Node::MergeChildren() noexcept {
    Node *node = left;
    left = nullptr;
    if (node != nullptr) {
        Node *prev = nullptr;
        for (;;) {
            Node *next = node->next;
            if (next == nullptr) {
                node->prev = prev;
                break;
            }
            Node *next_next = next->next;
            node = node->Link(next);
            node->prev = prev;
            prev = node;
            if (next_next == nullptr)
                break;
            node = next_next;
        }
        prev = node->prev;
        while (prev != nullptr) {
            Node *prev_prev = prev->prev;
            node = prev->Link(node);
            prev = prev_prev;
        }
        node->prev = nullptr;
        node->next = nullptr;
        node->parent = nullptr;
    }
    return node;
}

template<typename T, typename Less>
void PairingHeap<T, Less>::Node::Cut() noexcept {
    if (prev != nullptr)
        prev->next = next;
    else
        parent->left = next;
    if (next != nullptr) {
        next->prev = prev;
        next = nullptr;
    }
    prev = nullptr;
    parent = nullptr;
}

template<typename T, typename Less>
PairingHeap<T, Less>::~PairingHeap() noexcept {
    delete _root;
}

template<typename T, typename Less>
T PairingHeap<T, Less>::Pop() noexcept {
    Node *root = _root;
    _root = _root->MergeChildren();
    T value(move(root->value));
    delete root;
    return value;
}

template<typename T, typename Less>
typename PairingHeap<T, Less>::NodeRef PairingHeap<T, Less>::Insert(T value) {
    Node *node = new Node{std::move(value)};
    _root = _root->Link(node);
    return NodeRef(*node);
}

template<typename T, typename Less>
void PairingHeap<T, Less>::Modify(NodeRef ref, T value) noexcept {
    Node *node = &ref._node;
    if (Less()(value, node->value)) {
        node->value = std::move(value);
        if (node->parent != nullptr &&
            Less()(node->value, node->parent->value)) {
            node->Cut();
            _root = _root->Link(node);
        }
    } else if (Less()(node->value, value)) {
        node->value = std::move(value);
        Node *child = node->MergeChildren();
        if (child != nullptr)
            _root = _root->Link(child);
    }
}

}  // namespace utils
}  // namespace networkx

#endif  // NETWORKX_CYTHON_UTILS_HEAPS_H
