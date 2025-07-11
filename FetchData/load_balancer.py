from collections import deque
import threading
class load_balancer:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, thread, parent=None):
        if not hasattr(self, "_initialized"):
            self.thread = thread
            self._initialized = True
            self.__tasks = deque()
            self.parent = parent  # Store parent if needed globally

    def add_task(self, url, widget):
        self.__tasks.appendleft({url: widget})
        print(f"🆕 Task added: {url} → {widget}")
        self.executeNext()  # No parent argument needed

    def __execute(self, url, widget):
        from Services.Quality_Checking_Manager import QualityCheckingManager
        print(f"Calling start_quality_check for {url}")
        if self.thread.activeThreadCount() < self.thread.maxThreadCount():
            QualityCheckingManager().start_quality_check(url, widget)
        else:
            print("🚦 All threads busy. Task deferred.")

    def executeNext(self):
        if(self.__tasks):
            url, widget = self.__get_last_entry()
            if url and widget:
                print(f"▶️ Executing: {url} → {widget}")
                self.__execute(url, widget)

    def __get_last_entry(self):
        if self.__tasks:
            last_item = self.__tasks.pop()
            url, widget = next(iter(last_item.items()))
            print(url,widget)
            return url, widget
        return None, None