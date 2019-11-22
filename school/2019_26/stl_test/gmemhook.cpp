#include <cstdio>
#include <cstdlib>
#include <dlfcn.h> // dlsym
#include "gmemhook.h"

// ----------------------------------------------------------------------------
// GMemHook
// ----------------------------------------------------------------------------
GMemHook::GMemHook() {
  orgMallocFunc_ = nowMallocFunc_ = (MallocFunc)dlsym(RTLD_NEXT, "malloc");
  if (orgMallocFunc_ == nullptr) {
    fprintf(stderr, "[gmem] dlsym('malloc') return nullptr dlerror=%s\n", dlerror());
    goto _fail;
  }
  orgFreeFunc_ = nowFreeFunc_ = (FreeFunc)dlsym(RTLD_NEXT, "free");
  if (orgFreeFunc_ == nullptr) {
    fprintf(stderr, "[gmem] dlsym('malloc') return nullptr dlerror=%s\n", dlerror());
    goto _fail;
  }
  orgCallocFunc_ = nowCallocFunc_ = (CallocFunc)dlsym(RTLD_NEXT, "calloc");
  if (orgCallocFunc_ == nullptr) {
    fprintf(stderr, "[gmem] dlsym('calloc') return nullptr dlerror=%s\n", dlerror());
    goto _fail;
  }
  orgReallocFunc_ = nowReallocFunc_ = (ReallocFunc)dlsym(RTLD_NEXT, "realloc");
  if (orgReallocFunc_ == nullptr) {
    fprintf(stderr, "[gmem] dlsym('realloc') return nullptr dlerror=%s\n", dlerror());
    goto _fail;
  }
  return;
_fail:
  abort();
}

GMemHook::~GMemHook() {
}

void GMemHook::hook(
  MallocFunc mallocFunc,
  FreeFunc freeFunc,
  CallocFunc callocFunc,
  ReallocFunc reallocFunc) {
  if (mallocFunc  != nullptr) nowMallocFunc_  = mallocFunc;
  if (freeFunc    != nullptr) nowFreeFunc_    = freeFunc;
  if (callocFunc  != nullptr) nowCallocFunc_  = callocFunc;
  if (reallocFunc != nullptr) nowReallocFunc_ = reallocFunc;
}

void GMemHook::unhook() {
  nowMallocFunc_  = orgMallocFunc_;
  nowFreeFunc_    = orgFreeFunc_;
  nowCallocFunc_  = orgCallocFunc_;
  nowReallocFunc_ = orgReallocFunc_;
}

GMemHook& GMemHook::instance() {
  static GMemHook _instance;
  return _instance;
}

#ifdef GMEM_GLOBAL_HOOK
// ----------------------------------------------------------------------------
// global functions
// ----------------------------------------------------------------------------
void* malloc(size_t size) {
  return GMemHook::instance().nowMallocFunc_(size);
}

void free(void* ptr) {
  GMemHook::instance().nowFreeFunc_(ptr);
}

void* calloc(size_t nmemb, size_t size) {
  return GMemHook::instance().nowCallocFunc_(nmemb, size);
}

void* realloc(void* ptr, size_t size) {
  return GMemHook::instance().nowReallocFunc_(ptr, size);
}
#endif // GMEM_GLOBAL_HOOK
