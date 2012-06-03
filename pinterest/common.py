# coding=utf8
from __future__ import print_function
import threading

threadLock = threading.Lock()

def PrintThreaded(text, end=None):
    '''Thread-safe print function'''
    threadLock.acquire()
    print(text, end=end)
    threadLock.release()


if __name__ == '__main__':
    pass
