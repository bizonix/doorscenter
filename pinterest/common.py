# coding=utf8
from __future__ import print_function
import os, datetime, signal, platform, threading, ConfigParser

threadLock = threading.Lock()

config = ConfigParser.RawConfigParser()
config.read('config.ini')
LOG_LEVEL = int(config.get('Pinterest', 'LogLevel'))
LOG_FOLDER = 'logs'

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)
sessionLogFileName = '# session ' + datetime.datetime.now().strftime('%Y-%m-%d %H-%m') + '.txt'
sessionLogFileName = os.path.join(LOG_FOLDER, sessionLogFileName)

''' Для возможности прерывания скрипта по Ctrl+C введены следующие особенности:
1. Задан обработчик прерывания (см. ниже).
2. Задан таймаут для всех threading.Condition.wait().
3. Потоки сделаны демонами.
'''

def KeyboardInterruptHandler(signal, frame):
    ThreadSafePrint('\n=== Interrupted')
    raise SystemExit
signal.signal(signal.SIGINT, KeyboardInterruptHandler)

def ThreadSafePrint(text):
    '''Thread-safe print function + пишем текст в сессионный файл'''
    threadLock.acquire()
    print(text)
    if LOG_LEVEL > 0:
        open(sessionLogFileName, 'a').write(text + '\n')
    threadLock.release()
    
def CommandsListFromText(text):
    '''Разбиваем строку на список команд'''
    return [item.strip() for item in text.splitlines() if (item.strip() != '') and not item.strip().startswith('#')]

def DevelopmentMode():
    '''Запуск на компьютере разработчика'''
    return platform.node() == 'sasch-note'

if (__name__ == '__main__') and DevelopmentMode():
    print(os.getcwd())
