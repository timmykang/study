// ----------------------------------------------------------------------------
//
// G Library
//
// http://www.gilgil.net
//
// Copyright (c) Gilbert Lee All rights reserved
//
// ----------------------------------------------------------------------------

#pragma once

#include <memory>
#include "gmemhook.h"

template <typename T>
struct GMemAllocator : std::allocator<T> {
  GMemAllocator() {}
  template <typename U> GMemAllocator(GMemAllocator<U> const&) {}

  typedef T value_type;
  template <typename U> struct rebind { typedef GMemAllocator<U> other; };
  T* allocate(size_t n) {
    T* res = (T*)GMemHook::instance().orgMallocFunc_(n * sizeof(T));
    return res;
  }
  void deallocate(T* p, size_t n) {
    (void)n;
    GMemHook::instance().orgFreeFunc_(p);
  }
};
