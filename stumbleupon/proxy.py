# coding=utf8
import os, random, threading
import common

'''
Формат файла со списоком прокси "proxies.txt": 
proxy_host:proxy_port[:proxy_login:proxy_password]
'''

class ProxiesHolder(object):
    '''Класс работы с прокси'''
    
    _proxiesCondition = threading.Condition()
    _proxiesUsingSet = set()
    
    def __init__(self, proxiesFileName='proxies.txt'):
        '''Инициализация'''
        self.proxiesSet = {''}  # по умолчанию в списке прокси есть только локальный адрес
        self.proxiesDict = {'': ''}
        if not proxiesFileName:
            return
        if not os.path.exists(proxiesFileName):
            return
        for line in open(proxiesFileName).read().splitlines():
            if line.strip() == '':
                continue
            data = (line.strip() + ':' * 6).split(':')
            proxyHost = data[0] + ':' + data[1]
            proxyPassword = data[2] + ':' + data[3]
            if proxyPassword == ':':
                proxyPassword = ''
            self.proxiesSet.add(proxyHost)
            self.proxiesDict[proxyHost] = proxyPassword
    
    @classmethod
    def Acquire(self, proxyHost):
        '''Ждем освобожения требуемого прокси и захватываем его'''
        ProxiesHolder._proxiesCondition.acquire()
        try:
            while proxyHost in ProxiesHolder._proxiesUsingSet:
                ProxiesHolder._proxiesCondition.wait(common.WAIT_TIMEOUT)
            ProxiesHolder._proxiesUsingSet.add(proxyHost)
        finally:
            ProxiesHolder._proxiesCondition.release()
    
    def AcquireRandom(self):
        '''Возвращаем незанятый рандомный прокси из файла, либо локальный адрес'''
        ProxiesHolder._proxiesCondition.acquire()
        try:
            while len(self.proxiesSet - ProxiesHolder._proxiesUsingSet) == 0:
                ProxiesHolder._proxiesCondition.wait(common.WAIT_TIMEOUT)
            proxyHost = random.choice(self.proxiesSet - ProxiesHolder._proxiesUsingSet)
            ProxiesHolder._proxiesUsingSet.add(proxyHost)
        finally:
            ProxiesHolder._proxiesCondition.release()
        return proxyHost, self.proxiesDict[proxyHost]
    
    @classmethod
    def Release(self, proxyHost):
        '''Освобождаем захваченный прокси'''
        ProxiesHolder._proxiesCondition.acquire()
        try:
            ProxiesHolder._proxiesUsingSet.remove(proxyHost)
            ProxiesHolder._proxiesCondition.notifyAll()
        finally:
            ProxiesHolder._proxiesCondition.release()


if (__name__ == '__main__') and common.DevelopmentMode():
    pass
