from concurrent.futures import ThreadPoolExecutor
import threading
from traceback import print_exc
import os
import time

lock = threading.Lock()

class Log:
    def __init__(self, log_path: str="download.log"):
        self.log_path = log_path
        self.f = open(log_path, 'a', encoding='utf8')
    
    def print(self, *args, **kwargs):
        with lock:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"{now}:{__file__}:", *args, **kwargs, file=self.f, flush=True)