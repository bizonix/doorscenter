# coding=utf8
import os, random, time, agent

class TestAgent(agent.BaseAgent):
    ''' Параметры (см. методы GetTaskDetails и SetTaskDetails):
    Входные: input.
    Выходные: output.'''
    
    def _Settings(self):
        '''Настройки'''
        pass
        
    def _ActionOn(self):
        self._Settings()
        time.sleep(random.randint(1, 3))
        print(self.currentTask['paramIn'])
        self._Done()
        return True
    
    def _ActionOff(self):
        #self._Settings()  # в текущей это не нужно
        '''Значения по умолчанию'''
        self.currentTask['paramIn'] = ''
        self.currentTask['paramOut'] = str(random.randint(100, 999))
        return True

if __name__ == '__main__':
    #agent = TestAgent('http://searchpro.name/doorscenter/doorsadmin')
    agent = TestAgent('http://127.0.0.1:8000/doorsadmin')
