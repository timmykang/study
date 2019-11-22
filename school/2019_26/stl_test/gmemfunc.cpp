#include "gmemfunc.h"
#include "gmemmgr.h"

// ----------------------------------------------------------------------------
// control functions
// ----------------------------------------------------------------------------
void gmem_start(void) {
  GMemMgr::start();
}

void gmem_stop(void) {
  GMemMgr::stop();
}

bool gmem_verbose() {
  return GMemMgr::verbose();
}

void gmem_set_verbose(bool value) {
  GMemMgr::setVerbose(value);
}

FILE* gmem_err() {
  return GMemMgr::err();
}

void gmem_set_err(FILE* value) {
  GMemMgr::setErr(value);
}

FILE* gmem_out() {
  return GMemMgr::out();
}

void gmem_set_out(FILE* value) {
  GMemMgr::setOut(value);
}

// ----------------------------------------------------------------------------
// replace functions for c
// ----------------------------------------------------------------------------
void* gmem_malloc(size_t size, const char* file, const int line) {
  void* res = GMemMgr::_malloc(size, file, line);
  if (GMemMgr::verbose())
    fprintf(GMemMgr::out(), "[gmem] gmem_malloc(%d, %s, %d) > %p\n", (int)size, file, line, res);
  return res;
}

void gmem_free(void *ptr, const char* file, const int line) {
  if (GMemMgr::verbose())
    fprintf(GMemMgr::out(), "[gmem] gmem_free(%p, %s, %d)\n", ptr, file, line);
  return GMemMgr::_free(ptr, file, line);
}

void* gmem_calloc(size_t nmemb, size_t size, const char* file, const int line) {
  void* res = GMemMgr::_calloc(nmemb, size, file, line);
  if (GMemMgr::verbose())
    fprintf(GMemMgr::out(), "[gmem] gmem_calloc(%d, %d, %s, %d) > %p\n", (int)nmemb, (int)size,file, line, res);
  return res;
}

void* gmem_realloc(void *ptr, size_t size, const char* file, const int line) {
  void* res = GMemMgr::_realloc(ptr, size, file, line);
  if (GMemMgr::verbose())
    fprintf(GMemMgr::out(), "[gmem] gmem_realloc(%p, %d, %s, %d) > %p\n", ptr, (int)size,file, line, res);
  return res;
}

// ----------------------------------------------------------------------------
// replace operators for cpp
// ----------------------------------------------------------------------------
void* operator new(size_t size, const char* file, const int line) {
  void* res = GMemMgr::_malloc(size, file, line);
  if (GMemMgr::verbose())
    fprintf(GMemMgr::out(), "[gmem] new(%d, %s, %d) > %p\n", (int)size, file, line, res);
  return res;
}

void* operator new[](size_t size, const char* file, const int line) {
  void* res = GMemMgr::_malloc(size, file, line);
  if (GMemMgr::verbose())
    fprintf(GMemMgr::out(), "[gmem] new[](%d, %s, %d) > %p\n", (int)size, file, line, res);
  return res;
}

// ----------------------------------------------------------------------------
// global operators for cpp
// ----------------------------------------------------------------------------
void* operator new(size_t size) {
  void* res = GMemMgr::_malloc(size, nullptr, 0);
  if (GMemMgr::verbose())
    fprintf(GMemMgr::out(), "[gmem] new(%d) > %p\n", (int)size, res);
  return res;
}

void* operator new[](size_t size) {
  void* res = GMemMgr::_malloc(size, nullptr, 0);
  if (GMemMgr::verbose())
    fprintf(GMemMgr::out(), "[gmem] new[](%d) > %p\n", (int)size, res);
  return res;
}

void operator delete(void* ptr) throw() {
  if (GMemMgr::verbose())
    fprintf(GMemMgr::out(), "[gmem] delete(%p)\n", ptr);
  GMemMgr::_free(ptr, nullptr, 0);
}

void operator delete[](void* ptr) throw() {
  if (GMemMgr::verbose())
    fprintf(GMemMgr::out(), "[gmem] delete[](%p)\n", ptr);
  GMemMgr::_free(ptr, nullptr, 0);
}
