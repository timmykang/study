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

#include <stdbool.h> // bool
#include <stdio.h> // FILE

#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

// ----------------------------------------------------------------------------
// control functions
// ----------------------------------------------------------------------------
void gmem_start(void);
void gmem_stop(void);
bool gmem_verbose();
void gmem_set_verbose(bool value);
FILE* gmem_err();
void gmem_set_err(FILE* value);
FILE* gmem_out();
void gmem_set_out(FILE* value);

// ----------------------------------------------------------------------------
// replace functions for c
// ----------------------------------------------------------------------------
void* gmem_malloc (              size_t size, const char* file, const int line);
void  gmem_free   (void *ptr,                 const char* file, const int line);
void* gmem_calloc (size_t nmemb, size_t size, const char* file, const int line);
void* gmem_realloc(void *ptr,    size_t size, const char* file, const int line);

#ifdef __cplusplus
}
#endif // __cplusplus

#ifdef __cplusplus

#include <new> // bad_alloc

// ----------------------------------------------------------------------------
// replace operators for cpp
// ----------------------------------------------------------------------------
void* operator new  (size_t size, const char* file, const int line);
void* operator new[](size_t size, const char* file, const int line);

#endif // __cplusplus
