#ifndef NETWORKX_CYTHON_UTILS_MEMORY_H
#define NETWORKX_CYTHON_UTILS_MEMORY_H

#include <Python.h>
#include <memory>
#include <new>

namespace networkx {
namespace utils {

template<typename T>
struct PyAllocator : public std::allocator<T> {
private:
    typedef PyAllocator<T> Self;

public:
    static typename Self::pointer allocate(
        typename Self::size_type n,
        std::allocator<void>::const_pointer /* hint */ = nullptr) {
        void *ptr = PyObject_Malloc(n * sizeof(T));
        if (ptr == nullptr)
            throw std::bad_alloc();
        return static_cast<typename Self::pointer>(ptr);
    }

    static void deallocate(typename Self::pointer ptr,
                           typename Self::size_type /* n */) {
        PyObject_Free(ptr);
    }

    template<typename U>
    struct rebind {
        typedef PyAllocator<U> other;
    };
};

template<typename T, typename U>
bool operator==(const PyAllocator<T>&, const PyAllocator<U>&) {
    return true;
}

template<typename T, typename U>
bool operator!=(const PyAllocator<T>&, const PyAllocator<U>&) {
    return false;
}

class PyAllocated {
public:
    virtual ~PyAllocated() noexcept = default;

    static void* operator new(std::size_t size) {
        void *ptr = PyObject_Malloc(size);
        if (ptr == nullptr)
            throw std::bad_alloc();
        return ptr;
    }

    static void* operator new[](std::size_t size) {
        return operator new(size);
    }

    static void operator delete(void *ptr) noexcept {
        PyObject_Free(ptr);
    }

    static void operator delete[](void *ptr) noexcept {
        operator delete(ptr);
    }
};

}  // namespace utils
}  // namespace networkx

#endif  // NETWORKX_CYTHON_UTILS_MEMORY_H
