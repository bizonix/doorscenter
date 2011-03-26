# coding=utf8
import os, agent, kwk8

class SnippetsAgent(agent.BaseAgent):
    ''' Параметры (см. методы GetTaskDetails и SetTaskDetails):
    Входные: keywordsList, stopwordsList, language.
    Выходные: phrasesList.'''
    
    def _Settings(self):
        '''Настройки'''
        self.appFolder = 'c:/work/snippets/parser'  # папка с приложением
        self.snippetsFolder = 'c:/work/snippets'  # папка с готовыми сниппетами
        # self.appFolder = '/home/sasch/workspace/doorscenter/src/doorscenter/test/snippets/parser'  # папка с приложением
        # self.snippetsFolder = '/home/sasch/workspace/doorscenter/src/doorscenter/test/snippets'  # папка с готовыми сниппетами
        self.appKeysFile = os.path.join(self.appFolder, 'keys.txt')  # где приложение берет файл с кеями
        self.appTextFile = os.path.join(self.appFolder, 'text.txt')  # куда приложение пишет сниппеты
        self.localFile = os.path.join(self.snippetsFolder, self.currentTask['localFile'])  # куда поместить конечный файл
        self.stopwordsFile = os.path.join(self.appFolder, 'stopwords.txt')  # файл со стоп-словами
        
    def _ActionOn(self):
        print('Starting task #%s' % self._GetCurrentTaskId())
        self._Settings()
        with open(self.appKeysFile, 'w') as fd:
            fd.write('\n'.join(self.currentTask['keywordsList']))
        with open(self.stopwordsFile, 'w') as fd:
            fd.write('\n'.join(self.currentTask['stopwordsList']))
        self._RunApp('start ' + os.path.join(self.appFolder, 'parse.bat'))
        return True
    
    def _ActionOff(self):
        print('Ending task #%s' % self._GetCurrentTaskId())
        self._Settings()
        kwk8.ProcessKeys(self.appTextFile, self.localFile, self.stopwordsFile)
        self.currentTask['keywordsList'] = []
        self.currentTask['stopwordsList'] = []
        self.currentTask['phrasesList'] = []
        for line in open(self.localFile, 'r'):
            self.currentTask['phrasesList'].append(line.strip())
        return True

if __name__ == '__main__':
    agent = SnippetsAgent('http://searchpro.name/doorscenter/doorsadmin', 2)
