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

#include <cstddef> // for size_t

// ----------------------------------------------------------------------------
// GMemHook
// ----------------------------------------------------------------------------
class GMemHook {
protected:
  GMemHook();
  virtual ~GMemHook();

public:
  typedef void* (*MallocFunc) (size_t size);
  typedef void  (*FreeFunc)   (void*  ptr);
  typedef void* (*CallocFunc) (size_t nmemb, size_t size);
  typedef void* (*ReallocFunc)(void*  ptr,   size_t size);

  MallocFunc  orgMallocFunc_  = nullptr, nowMallocFunc_  = nullptr;
  FreeFunc    orgFreeFunc_    = nullptr, nowFreeFunc_    = nullptr;
  CallocFunc  orgCallocFunc_  = nullptr, nowCallocFunc_  = nullptr;
  ReallocFunc orgReallocFunc_ = nullptr, nowReallocFunc_ = nullptr;

public:
  void hook(
    MallocFunc  mallocFunc = nullptr,
    FreeFunc    freeFunc = nullptr,
    CallocFunc  callocFunc = nullptr,
    ReallocFunc reallocFunc = nullptr);
  void unhook();

public:
  static GMemHook& instance();
};
