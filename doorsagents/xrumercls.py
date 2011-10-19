# coding=utf8
import os, shutil, codecs, kwk8
from xml.sax.saxutils import escape
from xrumerxdf import *

class XrumerHelper():
    '''Абстрактный предок хэлперов'''
    
    def __init__(self, agent):
        self.agent = agent
        self.linker = XrumerTopicLinker(self)
        self.creationType = self.agent.currentTask['creationType']
        self.registerRun = self.agent.currentTask['registerRun']
        snippetsFolder = 'C:\\Work\\snippets'
        keywordsFolder = os.path.join(self.agent.appFolder, 'Keywords')
        self.keywordsFile = escape(os.path.join(keywordsFolder, '%s.txt' % self.agent.currentTask['niche']))
        self.snippetsFile = escape(os.path.join(snippetsFolder, self.agent.currentTask['snippetsFile']))
        self.anchorsFile = escape(self.linker.GetSpamAnchorsFile())
        self.profilesFile = escape(self.linker.GetProfilesFile())
    
    def _WriteKeywords(self):
        '''Пишем кейворды'''
        with codecs.open(self.agent.keywordsFile, 'w', 'cp1251') as fd:
            fd.write('\n'.join(self.agent.currentTask['keywordsList']))
    
    def _CopyBase(self, sourceFileName, destFileName):
        '''Копируем базу'''
        try:
            shutil.copyfile(sourceFileName, destFileName)
        except Exception as error:
            print('Cannot copy base: %s' % error)
    
    def _DeleteBase(self, baseFileName):
        '''Удаляем базу'''
        if os.path.isfile(baseFileName): 
            try:
                os.remove(baseFileName)
            except Exception as error:
                print('Cannot remove base: %s' % error)
    
    def _FilterBase(self, baseFileName):
        '''Фильтруем базу от неуспешных'''
        try:
            if kwk8.Kwk8Links(self.agent.logFails).Count() > 700:
                kwk8.Kwk8Links(baseFileName).DeleteByFile(self.agent.logFails).Save(baseFileName)
        except Exception as error:
            print('Cannot filter base: %s' % error)
    
    def GetProjectName(self):
        '''Имя проекта'''
        return 'ProjectX%d' % self.agent.currentTask['id']
    
    def ActionOn(self):
        '''Действия при старте'''
        pass
    
    def ActionOff(self):
        '''Действия при финише'''
        pass
    
class XrumerHelperBaseSpam(XrumerHelper):
    '''База R для спама по топикам'''
    
    def GetProjectName(self):
        return 'ProjectR%d' % self.agent.currentTask['id']
    
    def ActionOn(self):
        '''Содержимое проекта'''
        spamLinksList = escape(codecs.decode(' '.join(self.agent.currentTask['spamLinksList']), 'cp1251'))
        projSubject = '#file_links[%s,1,N]' % (self.keywordsFile)
        projBody = '#file_links[%s,7,S] %s #file_links[%s,3,S] #file_links[%s,3,S] #file_links[%s,3,S]' % (self.snippetsFile, spamLinksList, self.anchorsFile, self.profilesFile, self.snippetsFile)
        '''Создаем настройки'''
        threadsCount = 110
        controlTimeRange = 120
        if self.creationType == 'post':
            self.agent._CreateSettings('', '', 'post', 'LinksList', threadsCount, controlTimeRange, projSubject, projBody)
        elif self.creationType == 'reply':
            self.agent._CreateSettings('', '', 'reply', 'LinksList', threadsCount, controlTimeRange, projSubject, projBody)
        elif self.creationType == 'reg + post' and self.registerRun:
            self.agent._CreateSettings('register-only', '', 'post', 'LinksList', threadsCount, controlTimeRange, projSubject, projBody)
        elif self.creationType == 'reg + post' and not self.registerRun:
            self.agent._CreateSettings('from-registered', '', 'post', 'LinksList', threadsCount, controlTimeRange, projSubject, projBody)
        elif self.creationType == 'reg + reply' and self.registerRun:
            self.agent._CreateSettings('register-only', '', 'reply', 'LinksList', threadsCount, controlTimeRange, projSubject, projBody)
        elif self.creationType == 'reg + reply' and not self.registerRun:
            self.agent._CreateSettings('from-registered', '', 'reply', 'LinksList', threadsCount, controlTimeRange, projSubject, projBody)
        '''Пишем кейворды, копируем исходную базу в целевую и удаляем существующую базу R'''
        self._WriteKeywords()
        self._CopyBase(self.agent.baseSourceFile, self.agent.baseMainFile)
        self._DeleteBase(self.agent.baseMainRFile) 
    
    def ActionOff(self):
        '''Копируем анкоры и удаляем базу, которую копировали ранее'''
        self.linker.AddSpamAnchorsFile()
        self._DeleteBase(self.agent.baseMainFile) 

class XrumerHelperSpamTask(XrumerHelper):
    '''Задание для спама по топикам'''
    
    def GetProjectName(self):
        return 'ProjectS%d' % self.agent.currentTask['id']
    
    def ActionOn(self):
        '''Содержимое проекта'''
        spamLinksList = escape(codecs.decode(' '.join(self.agent.currentTask['spamLinksList']), 'cp1251'))
        projSubject = '#file_links[%s,1,N]' % (self.keywordsFile)
        projBody = '#file_links[%s,7,S] %s #file_links[%s,3,S] #file_links[%s,3,S] #file_links[%s,3,S]' % (self.snippetsFile, spamLinksList, self.anchorsFile, self.profilesFile, self.snippetsFile)
        '''Создаем настройки'''
        threadsCount = 160
        controlTimeRange = 60
        self.agent._CreateSettings('from-registered', '', 'reply', 'RLinksList', threadsCount, controlTimeRange, projSubject, projBody)
    
    def ActionOff(self):
        '''Копируем анкоры и фильтруем базу R от неуспешных'''
        self.linker.AddSpamAnchorsFile()
        self._FilterBase(self.agent.baseMainRFile)

class XrumerHelperBaseDoors(XrumerHelper):
    '''Доры на форумах'''
    
    def GetProjectName(self):
        return 'ProjectD%d' % self.agent.currentTask['id']
    
    def ActionOn(self):
        '''Содержимое проекта'''
        body = escape(self.agent.currentTask['body'])
        projSubject = '#file_links[%s,1,N]' % (self.keywordsFile)
        projBody = '%s #file_links[%s,10,L] #file_links[%s,3,L] #file_links[%s,3,L] #file_links[%s,10,S]' % (body, self.keywordsFile, self.anchorsFile, self.profilesFile, self.snippetsFile)
        '''Если первый проход'''
        if not os.path.isfile(self.agent.baseMainRFile):
            '''Создаем настройки'''
            threadsCount = 110
            controlTimeRange = 120
            if self.creationType == 'post':
                self.agent._CreateSettings('', '', 'post', 'LinksList', threadsCount, controlTimeRange, projSubject, projBody)
            elif self.creationType == 'reply':
                self.agent._CreateSettings('', '', 'reply', 'LinksList', threadsCount, controlTimeRange, projSubject, projBody)
            elif self.creationType == 'reg + post' and self.registerRun:
                self.agent._CreateSettings('register-only', '', 'post', 'LinksList', threadsCount, controlTimeRange, projSubject, projBody)
            elif self.creationType == 'reg + post' and not self.registerRun:
                self.agent._CreateSettings('from-registered', '', 'post', 'LinksList', threadsCount, controlTimeRange, projSubject, projBody)
            elif self.creationType == 'reg + reply' and self.registerRun:
                self.agent._CreateSettings('register-only', '', 'reply', 'LinksList', threadsCount, controlTimeRange, projSubject, projBody)
            elif self.creationType == 'reg + reply' and not self.registerRun:
                self.agent._CreateSettings('from-registered', '', 'reply', 'LinksList', threadsCount, controlTimeRange, projSubject, projBody)
            '''Пишем кейворды, копируем исходную базу в целевую и удаляем существующую базу R'''
            self._WriteKeywords()
            self._CopyBase(self.agent.baseSourceFile, self.agent.baseMainFile)
            self._DeleteBase(self.agent.baseMainRFile) 
        else:
            '''Создаем настройки'''
            threadsCount = 160
            controlTimeRange = 60
            self.agent._CreateSettings('from-registered', '', 'reply', 'RLinksList', threadsCount, controlTimeRange, projSubject, projBody)
            '''Пишем кейворды'''
            self._WriteKeywords()
            
    def ActionOff(self):
        '''Копируем анкоры, фильтруем базу R от неуспешных и удаляем базу, которую копировали ранее'''
        self.linker.AddDoorsAnchorsFile()
        self._FilterBase(self.agent.baseMainRFile)
        self._DeleteBase(self.agent.baseMainFile) 

class XrumerHelperBaseProfiles(XrumerHelper):
    '''Профили'''
    
    def GetProjectName(self):
        return 'ProjectP%d' % self.agent.currentTask['id']
    
    def ActionOn(self):
        '''Создаем настройки'''
        threadsCount = 160
        controlTimeRange = 60
        if self.registerRun:
            self.agent._CreateSettings('register-only', '', 'post', 'LinksList', threadsCount, controlTimeRange, 'none', 'none', '', '')
        else:
            self.agent._CreateSettings('from-registered', 'edit-profile', 'post', 'LinksList', threadsCount, controlTimeRange, 'none', r'#file_links[x:\foo.txt,1,N]', self.agent.currentTask['homePage'], self.agent.currentTask['signature'])
        '''Копируем исходную базу в целевую'''
        if self.registerRun:
            self._CopyBase(self.agent.baseSourceFile, self.agent.baseMainFile)
    
    def ActionOff(self):
        '''Фильтруем базу от неуспешных и копируем профили для последующего спама'''
        self._FilterBase(self.agent.baseMainFile)
        if not self.registerRun:
            self.linker.AddProfilesFile()
