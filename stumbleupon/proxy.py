# coding=utf8
import threading
import common

proxiesCondition = threading.Condition()
proxiesUsingSet = set()

class ProxiesHolder(object):
    '''Класс работы с прокси'''
    
    @classmethod
    def Acquire(self, proxyHost):
        '''Ждем освобожения требуемого прокси и захватываем его'''
        proxiesCondition.acquire()
        try:
            while proxyHost in proxiesUsingSet:
                proxiesCondition.wait(common.WAIT_TIMEOUT)
            proxiesUsingSet.add(proxyHost)
        finally:
            proxiesCondition.release()
    
    @classmethod
    def AcquireRandom(self):
        '''Возвращаем рандомный прокси'''
        pass  # TODO: реализовать
    
    @classmethod
    def Release(self, proxyHost):
        '''Освобождаем захваченный прокси'''
        proxiesCondition.acquire()
        try:
            proxiesUsingSet.remove(proxyHost)
            proxiesCondition.notifyAll()
        finally:
            proxiesCondition.release()


if (__name__ == '__main__') and common.DevelopmentMode():
    pass
