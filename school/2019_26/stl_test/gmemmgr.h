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

#include <cstddef> // size_t
#include <cstdio>

// ----------------------------------------------------------------------------
// GMemMgr
// ----------------------------------------------------------------------------
class GMemMgr {
public:
  static void start();
  static void stop();
  static bool verbose();
  static void setVerbose(bool value);
  static FILE* err();
  static void setErr(FILE* value);
  static FILE* out();
  static void setOut(FILE* value);

public:
  static void* _malloc (size_t size,               const char* file, const int line);
  static void  _free   (void*  ptr,                const char* file, const int line);
  static void* _calloc (size_t nmemb, size_t size, const char* file, const int line);
  static void* _realloc(void*  ptr,   size_t size, const char* file, const int line);
};
