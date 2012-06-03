# coding=utf8
from __future__ import print_function
import os, time, threading

LOG_LEVEL = 2
LOG_FOLDER = 'log'

threadLock = threading.Lock()

def PrintThreaded(text, end=None):
    '''Thread-safe print function'''
    threadLock.acquire()
    print(text, end=end)
    threadLock.release()

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)
sessionLogFileName = 'session-' + str(int(time.time() * 100)) + '.txt'
sessionLogFileName = os.path.join(LOG_FOLDER, sessionLogFileName)

def PrintLogThreaded(text, end=None):
    '''Thread-safe write to log function'''
    threadLock.acquire()
    if end == None:
        text += '\n'
    open(sessionLogFileName, 'a').write(text)
    threadLock.release()
