# coding=utf8
from __future__ import print_function
import os, datetime, signal, platform, threading, ConfigParser

threadLock = threading.Lock()

config = ConfigParser.RawConfigParser()
config.read('config.ini')
LOG_LEVEL = int(config.get('Bot', 'LogLevel'))
LOG_FOLDER = 'logs'

WAIT_TIMEOUT = 60 * 60 * 24 * 7

''' Для возможности прерывания скрипта по Ctrl+C введены следующие особенности:
1. Задан обработчик прерывания (см. ниже).
2. Задан таймаут для всех threading.Condition.wait().
3. Все потоки сделаны демонами.
'''

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)
sessionLogFileName = '# session ' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.txt'
sessionLogFileName = os.path.join(LOG_FOLDER, sessionLogFileName)

def ThreadSafePrint(text):
    '''Thread-safe print function + пишем текст в сессионный файл'''
    threadLock.acquire()
    print(text)
    if LOG_LEVEL > 0:
        open(sessionLogFileName, 'a').write(text + '\n')
    threadLock.release()


screenSlotsCondition = threading.Condition()
screenSlotsList = range(20)  # также ограничение общего числа работающих потоков

class ScreenSlot(object):
    '''Слот для вывода на экран'''
    
    @classmethod
    def Acquire(self):
        '''Захватываем слот'''
        screenSlot = None
        screenSlotsCondition.acquire()
        try:
            while len(screenSlotsList) == 0:
                screenSlotsCondition.wait(WAIT_TIMEOUT)
            screenSlot = screenSlotsList.pop(0)
        except Exception:
            pass
        screenSlotsCondition.release()
        return screenSlot
    
    @classmethod
    def Release(self, screenSlot):
        '''Освобождаем захваченный слот'''
        if screenSlot == None:
            return
        screenSlotsCondition.acquire()
        try:
            screenSlotsList.append(screenSlot)
            screenSlotsList.sort()
            screenSlotsCondition.notifyAll()
        except Exception:
            pass
        screenSlotsCondition.release()


def KeyboardInterruptHandler(signal, frame):
    ThreadSafePrint('\n=== Interrupted')
    raise SystemExit
signal.signal(signal.SIGINT, KeyboardInterruptHandler)

def DevelopmentMode():
    '''Запуск на компьютере разработчика'''
    return platform.node() == 'sasch-note'


if (__name__ == '__main__') and DevelopmentMode():
    pass
