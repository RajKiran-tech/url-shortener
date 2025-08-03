
import threading
from datetime import datetime

class URLStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.urls = {}

    def add(self, short_code, original_url):
        with self.lock:
            self.urls[short_code] = {
                "original_url": original_url,
                "clicks": 0,
                "created_at": datetime.utcnow()
            }

    def get(self, short_code):
        with self.lock:
            return self.urls.get(short_code)

    def increment_clicks(self, short_code):
        with self.lock:
            if short_code in self.urls:
                self.urls[short_code]["clicks"] += 1
