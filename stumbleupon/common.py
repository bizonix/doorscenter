# coding=utf8
from __future__ import print_function
import os, datetime, signal, platform, threading, ConfigParser

''' 
На платформе Windows прерывание работы скрипта работает через Ctrl+Break штатными средствами.
Для возможности прерывания скрипта по Ctrl+C на платформе Linux сделано следующее:

1. Задан обработчик прерывания (KeyboardInterruptHandler).
2. Задан таймаут для всех threading.Condition.wait().
3. Все потоки сделаны демонами.
'''

threadLock = threading.Lock()

config = ConfigParser.RawConfigParser()
config.read('config.ini')

LOG_LEVEL = int(config.get('Bot', 'LogLevel'))
LOG_FOLDER = 'logs'
TEMP_FOLDER = 'temp'
WAIT_TIMEOUT = 60 * 60 * 24 * 7
MAX_THREADS = 100

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

sessionLogFileName = '# session ' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.txt'
sessionLogFileName = os.path.join(LOG_FOLDER, sessionLogFileName)

class ScreenSlot(object):
    '''Слот для вывода на экран'''
    
    _slotsCondition = threading.Condition()
    _slotsList = range(MAX_THREADS)
    
    @classmethod
    def Acquire(self):
        '''Захватываем слот'''
        screenSlot = None
        ScreenSlot._slotsCondition.acquire()
        try:
            while len(ScreenSlot._slotsList) == 0:
                ScreenSlot._slotsCondition.wait(WAIT_TIMEOUT)
            screenSlot = ScreenSlot._slotsList.pop(0)
        except Exception:
            pass
        ScreenSlot._slotsCondition.release()
        return screenSlot
    
    @classmethod
    def Release(self, screenSlot):
        '''Освобождаем захваченный слот'''
        if screenSlot == None:
            return
        ScreenSlot._slotsCondition.acquire()
        try:
            ScreenSlot._slotsList.append(screenSlot)
            ScreenSlot._slotsList.sort()
            ScreenSlot._slotsCondition.notifyAll()
        except Exception:
            pass
        ScreenSlot._slotsCondition.release()

def ThreadSafePrint(text):
    '''Thread-safe print function + пишем текст в сессионный файл'''
    threadLock.acquire()
    print(text)
    if LOG_LEVEL > 0:
        open(sessionLogFileName, 'a').write(text + '\n')
    threadLock.release()

def KeyboardInterruptHandler(signal, frame):
    '''Обработчик нажатия на Ctrl+C и Ctrl+Break'''
    ThreadSafePrint('\n=== Interrupted')
    raise SystemExit
signal.signal(signal.SIGINT, KeyboardInterruptHandler)

def DevelopmentMode():
    '''Запуск на компьютере разработчика'''
    return platform.node() == 'sasch-note'


if (__name__ == '__main__') and DevelopmentMode():
    print(GenerateBirthdate())
