# coding=utf8
import os, agent, kwk8

class SnippetsAgent(agent.BaseAgent):
    ''' Параметры (см. методы GetTaskDetails и SetTaskDetails):
    Входные: keywordsList, stopwordsList, language.
    Выходные: phrasesCount.'''
    
    def _Settings(self):
        '''Настройки'''
        self.appFolder = 'c:/work/snippets/parser'  # папка с приложением
        self.snippetsFolder = 'c:/work/snippets'  # папка с готовыми сниппетами
        self.appKeysFile = os.path.join(self.appFolder, 'keywords.txt')  # где приложение берет файл с кеями
        self.appTextFile = os.path.join(self.appFolder, 'text.txt')  # куда приложение пишет сниппеты
        self.localFile = os.path.join(self.snippetsFolder, self.currentTask['localFile'])  # куда поместить конечный файл
        self.stopwordsFile = os.path.join(self.appFolder, 'stopwords.txt')  # файл со стоп-словами
        self.appLanguageFile = os.path.join(self.appFolder, 'language.txt')  # откуда читается язык (en, ru)
        
    def _ActionOn(self):
        self._Settings()
        with open(self.appKeysFile, 'w') as fd:
            fd.write('\n'.join(self.currentTask['keywordsList']))
        with open(self.stopwordsFile, 'w') as fd:
            fd.write('\n'.join(self.currentTask['stopwordsList']))
        with open(self.appLanguageFile, 'w') as fd:
            fd.write(self.currentTask['language'])
        self._RunApp(os.path.join(self.appFolder, 'parse.bat'))
        return True
    
    def _ActionOff(self):
        self._Settings()
        kwk8.ProcessSnippets(self.appTextFile, self.localFile, self.stopwordsFile)
        self.currentTask['keywordsList'] = []
        self.currentTask['stopwordsList'] = []
        phrasesCount = 0
        for _ in open(self.localFile, 'r'):
            phrasesCount += 1
        self.currentTask['phrasesCount'] = phrasesCount
        return True

if __name__ == '__main__':
    agent = SnippetsAgent('http://searchpro.name/doorscenter/doorsadmin', 2)
