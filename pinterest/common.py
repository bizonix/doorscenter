# coding=utf8
from __future__ import print_function
import os, time, platform, threading, ConfigParser

threadLock = threading.Lock()

config = ConfigParser.RawConfigParser()
config.read('config.ini')
LOG_LEVEL = int(config.get('Pinterest', 'LogLevel'))
LOG_FOLDER = 'logs'

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)
sessionLogFileName = 'session-' + str(int(time.time() * 100)) + '.txt'
sessionLogFileName = os.path.join(LOG_FOLDER, sessionLogFileName)

def CommandsListFromText(text):
    '''Разбиваем строку на список команд'''
    return [item.strip() for item in text.splitlines() if (item.strip() != '') and not item.strip().startswith('#')]

def DevelopmentMode():
    '''Запуск на компьютере разработчика'''
    return platform.node() == 'sasch-note'

if (__name__ == '__main__') and DevelopmentMode():
    print(os.getcwd())
