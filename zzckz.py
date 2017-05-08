#coding=utf8
import threading
Lock = threading.Lock()
class cicy(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(cicy, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance
    def __init__(self):
        pass
    @staticmethod
    def test(msg):
        return 'cicy'