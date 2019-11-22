// ----------------------------------------------------------------------------
//
// G Library
//
// http://www.gilgil.net
//
// Copyright (c) Gilbert Lee All rights reserved
//
// ----------------------------------------------------------------------------

#include "gmemfunc.h"

// ----------------------------------------------------------------------------
// macro for c
// ----------------------------------------------------------------------------
#undef  malloc
#define malloc(SIZE)        gmem_malloc ((SIZE),          __FILE__, __LINE__)
#undef  free
#define free(PTR)           gmem_free   ((PTR),           __FILE__, __LINE__)
#undef  calloc
#define calloc(NMEMB, SIZE) gmem_calloc ((NMEMB), (SIZE), __FILE__, __LINE__)
#undef  realloc
#define realloc(PTR, SIZE)  gmem_realloc((PTR),   (SIZE), __FILE__, __LINE__)

// ----------------------------------------------------------------------------
// macro for cpp
// ----------------------------------------------------------------------------
#ifdef __cplusplus

#undef  gmem_new
#define gmem_new new(__FILE__, __LINE__)
#undef  new
#define new gmem_new

#endif // __cplusplus
