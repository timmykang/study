#include <unordered_map>
#include "gmemallocator.h"
#include "gmemhook.h"
#include "gmemmgr.h"

// ----------------------------------------------------------------------------
// GMemLeak
// ----------------------------------------------------------------------------
class GMemLeak {
public:
  struct Item {
    size_t size;
    char* file;
    int line;
  };
  typedef std::unordered_map<void*/*ptr*/, Item,
    std::hash<void*>,
    std::equal_to<void*>,
    GMemAllocator<std::pair<const void*,Item>>> Items;
  Items items_;

public:
  GMemLeak() {
    clear();
  }

  virtual ~GMemLeak() {
    check();
    clear();
  }

  void clear() {
    items_.clear();
  }

  void check() {
    if (items_.size() > 0) {
      fprintf(GMemMgr::err(), "[gmem] ***********************************************************************\n");
      for (Items::iterator it = items_.begin(); it != items_.end(); it++) {
        void* ptr = it->first;
        Item& item = it->second;
        fprintf(GMemMgr::err(), "[gmem] memory leak %p(%d bytes) %s:%d\n", ptr, (int)item.size, item.file, item.line);
      }
      fprintf(GMemMgr::err(), "[gmem] ***********************************************************************\n");
      items_.clear();
    }
  }

  bool exists(void* ptr) {
    Items::iterator it = items_.find(ptr);
    return it != items_.end();
  }

  void add(void* ptr, size_t size, const char* file, const int line) {
    if (items_.find(ptr) != items_.end()) {
      fprintf(GMemMgr::err(), "[gmem] ***********************************************************************\n");
      fprintf(GMemMgr::err(), "[gmem] already exist ptr(%p) file=%s line=%d\n", ptr, file, line);
      fprintf(GMemMgr::err(), "[gmem] ***********************************************************************\n");
      return;
    }
    Item item;
    item.size = size;
    item.file = (char*)file;
    item.line = line;
    items_[ptr] = item;
  }

  void del(void* ptr, const char* file, const int line) {
    Items::iterator it = items_.find(ptr);
    if (it == items_.end()) {
      fprintf(GMemMgr::err(), "[gmem] ***********************************************************************\n");
      fprintf(GMemMgr::err(), "[gmem] can not find ptr(%p) file=%s line=%d\n", ptr, file, line);
      fprintf(GMemMgr::err(), "[gmem] ***********************************************************************\n");
      return;
    }
    items_.erase(it);
  }

  static GMemLeak& instance() {
    static GMemLeak _memLeakImpl;
    return _memLeakImpl;
  }
};

// ----------------------------------------------------------------------------
// GMemMgrImpl
// ----------------------------------------------------------------------------
class GMemMgrImpl {
protected:
  bool verbose_;
  FILE* err_;
  FILE* out_;
  GMemLeak memLeak_;

public:
  GMemMgrImpl() {
    verbose_ = false;
    err_ = stderr;
    out_ = stdout;
    GMemHook::instance().hook(_malloc, _free, _calloc, _realloc);
    start();
  }

  virtual ~GMemMgrImpl() {
    GMemHook::instance().unhook();
    stop();
  }

  void start() {
    memLeak_.clear();
  }

  void stop() {
    memLeak_.check();
    memLeak_.clear();
  }

  bool verbose() {
    return verbose_;
  }

  void setVerbose(bool value) {
    verbose_ = value;
  }

  FILE* err() {
    return err_;
  }

  void setErr(FILE* value) {
    err_ = value;
  }

  FILE* out() {
    return out_;
  }

  void setOut(FILE* value) {
    out_ = value;
  }

protected:
  static void* _malloc(size_t size) {
    return instance().malloc(size, nullptr, 0);
  }

  static void _free(void* ptr) {
    return instance().free(ptr, nullptr, 0);
  }

  static void* _calloc(size_t nmemb, size_t size) {
    return instance().calloc(nmemb, size, nullptr, 0);
  }

  static void* _realloc(void* ptr, size_t size) {
    return instance().realloc(ptr, size, nullptr, 0);
  }

public:
  void* malloc(size_t size, const char* file, const int line) {
    void* res = GMemHook::instance().orgMallocFunc_(size);
    memLeak_.add(res, size, file, line);
    return res;
  }

  void free(void* ptr, const char* file, const int line) {
    memLeak_.del(ptr, file, line);
    GMemHook::instance().orgFreeFunc_(ptr);
  }

  void* calloc(size_t nmemb, size_t size, const char* file, const int line) {
    void* res = GMemHook::instance().orgCallocFunc_(nmemb, size);
    memLeak_.add(res, size, file, line);
    return res;
  }

  void* realloc(void* ptr, size_t size, const char* file, const int line) {
    void* res = GMemHook::instance().orgReallocFunc_(ptr, size);
    memLeak_.del(ptr, file, line);
    memLeak_.add(res, size, file, line);
    return res;
  }

  static GMemMgrImpl& instance() {
    static GMemMgrImpl _memMgrImpl;
    return _memMgrImpl;
  }
};

// ----------------------------------------------------------------------------
// GMemMgr
// ----------------------------------------------------------------------------
void GMemMgr::start() {
  GMemMgrImpl::instance().start();
}

void GMemMgr::stop() {
  GMemMgrImpl::instance().stop();
}

bool GMemMgr::verbose() {
  return GMemMgrImpl::instance().verbose();
}

void GMemMgr::setVerbose(bool value) {
  GMemMgrImpl::instance().setVerbose(value);
}

FILE* GMemMgr::err() {
return GMemMgrImpl::instance().err();
}

void GMemMgr::setErr(FILE* value) {
  GMemMgrImpl::instance().setErr(value);
}

FILE* GMemMgr::out() {
  return GMemMgrImpl::instance().out();
}

void GMemMgr::setOut(FILE* value) {
  GMemMgrImpl::instance().setOut(value);
}

void* GMemMgr::_malloc(size_t size, const char* file, const int line) {
  return GMemMgrImpl::instance().malloc(size, file, line);
}

void GMemMgr::_free(void* ptr, const char* file, const int line) {
  return GMemMgrImpl::instance().free(ptr, file, line);
}

void* GMemMgr::_calloc(size_t nmemb, size_t size, const char* file, const int line) {
  return GMemMgrImpl::instance().calloc(nmemb, size, file, line);
}

void* GMemMgr::_realloc(void* ptr, size_t size, const char* file, const int line) {
  return GMemMgrImpl::instance().realloc(ptr, size, file, line);
}
