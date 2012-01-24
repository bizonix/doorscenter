# coding=utf8
import os, agent, kwk8, codecs
from snippets.snippets import Snippets

class SnippetsAgent(agent.BaseAgent):
    ''' Параметры (см. методы GetTaskDetails и SetTaskDetails):
    Входные: keywordsList, stopwordsList, language.
    Выходные: phrasesCount.'''
    
    def _Settings(self):
        '''Настройки'''
        self.localFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snippets', self.currentTask['localFile'])  # куда поместить конечный файл
        
    def _ActionOn(self):
        self._Settings()
        self.snippets = Snippets()
        self.snippets.Parse(self.currentTask['keywordsList'], self.currentTask['language'])
        self._Done()
        self._Cron()
        return True
    
    def _ActionOff(self):
        #self._Settings()  # в текущей версии парсера это не нужно
        '''Обработка'''
        with codecs.open(self.localFile, 'w', 'cp1251', 'ignore') as fd:
            fd.write('\n'.join(self.snippets.snippetsList))
        self.currentTask['phrasesCount'] = kwk8.ProcessSnippets(self.localFile, self.localFile, self.currentTask['stopwordsList'], ['http://', '[url', '.com', '.net', '.org', '.info', '.us', '.ru', '.ua', '.by', '.htm', '.html', '.php'])
        '''Значения по умолчанию'''
        self.currentTask['keywordsList'] = []
        self.currentTask['stopwordsList'] = []
        return True

if __name__ == '__main__':
    agent = SnippetsAgent('http://searchpro.name/doorscenter/doorsadmin')
