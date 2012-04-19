# coding=utf8
import random, time, agent

class TestAgent(agent.BaseAgent):
    ''' Параметры (см. методы GetTaskDetails и SetTaskDetails):
    Входные: input.
    Выходные: output.'''
    
    def _Settings(self):
        '''Настройки'''
        self.currentTask['paramOut'] = ''
        
    def _ActionOn(self):
        self._Settings()
        time.sleep(1)
        print(self.currentTask['paramIn'])
        #raise Exception('Error test #1')
        self._Done()
        #self._Cron()
        return True
    
    def _ActionOff(self):
        self._Settings()
        self.currentTask['paramIn'] = ''
        self.currentTask['paramOut'] = str(random.randint(100, 999))
        #raise Exception('Error test #2')
        return True

if __name__ == '__main__':
    #agent = TestAgent('http://searchpro.name/doorscenter/doorsadmin')
    agent = TestAgent('http://127.0.0.1:8000/doorsadmin')
