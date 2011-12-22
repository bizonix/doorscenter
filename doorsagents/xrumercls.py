# coding=utf8
import os, shutil, codecs, random, kwk8, baseparser, basechecker
from xml.sax.saxutils import escape
from xrumerxdf import *

'''Классы XrumerHelperBaseSpam и XrumerHelperBaseDoors не протестированы на 
работу с предварительной регистрацией.'''

class XrumerHelper(object):
    '''Абстрактный предок хэлперов'''
    
    def __init__(self, agent):
        self.agent = agent
        self.linker = XrumerTopicLinker(self)
        self.creationType = self.agent.currentTask['creationType']
        self.registerRun = self.agent.currentTask['registerRun']
        snippetsFolder = 'C:\\Work\\snippets'
        keywordsFolder = os.path.join(self.agent.appFolder, 'Keywords')
        self.keywordsFile = os.path.join(keywordsFolder, '%s.txt' % self.agent.currentTask['niche'])
        self.keywordsFileEsc = escape(self.keywordsFile)
        self.snippetsFileEsc = escape(os.path.join(snippetsFolder, self.agent.currentTask['snippetsFile']))
        self.anchorsFileEsc = escape(self.linker.GetSpamAnchorsFile())
        self.profilesFileEsc = escape(self.linker.GetProfilesFile())
    
    def _WriteKeywords(self):
        '''Пишем кейворды'''
        with codecs.open(self.keywordsFile, 'w', 'cp1251') as fd:
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
        '''Фильтруем базу от неуспешных и считаем число ссылок'''
        try:
            if kwk8.Kwk8Links(self.agent.logFails).Count() > 700:
                kwk8.Kwk8Links(baseFileName).DeleteByFile(self.agent.logFails).Save(baseFileName)
        except Exception as error:
            print('Cannot filter base: %s' % error)
        self.agent._CountLinks('baseLinksCount', baseFileName, 'base')
    
    def GetProjectName(self):
        '''Имя проекта'''
        return 'ProjectX%d' % self.agent.currentTask['id']
    
    def ActionOn(self):
        '''Действия при старте'''
        pass
    
    def ActionOff(self):
        '''Действия при финише'''
        pass

class XrumerHelperBaseRaw(XrumerHelper):
    '''Парсим и чекаем новую базу'''
    
    def GetProjectName(self):
        return 'ProjectN%d' % self.agent.currentTask['id']
    
    def ActionOn(self):
        pass
    
    def ActionOff(self):
        pass
        
class XrumerHelperBaseSpam(XrumerHelper):
    '''Базы L, R и Z для спама по топикам'''
    
    def GetProjectName(self):
        return 'ProjectR%d' % self.agent.currentTask['id']
    
    def ActionOn(self):
        '''Содержимое проекта'''
        spamLinksList = escape(codecs.decode(' '.join(self.agent.currentTask['spamLinksList']), 'cp1251'))
        projSubject = '#file_links[%s,1,N]' % (self.keywordsFileEsc)
        projBody = '#file_links[%s,7,S] %s #file_links[%s,3,S] #file_links[%s,3,S] #file_links[%s,3,S]' % (self.snippetsFileEsc, spamLinksList, self.anchorsFileEsc, self.profilesFileEsc, self.snippetsFileEsc)
        '''Пишем кейворды, копируем исходную базу в целевую и удаляем существующую базу R или Z'''
        self._WriteKeywords()
        self._CopyBase(self.agent.baseSourceFile, self.agent.baseMainFile)
        if self.agent.currentTask['baseType'] == 'RLinksList':
            self._DeleteBase(self.agent.baseMainRFile)
        elif self.agent.currentTask['baseType'] == 'ZLinksList': 
            self._DeleteBase(self.agent.baseMainZFile)
        else:
            pass 
        '''Создаем настройки'''
        threadsCount = 110
        if self.creationType == 'post':
            self.agent._CreateSettings('none', '', 'post', 'LinksList', threadsCount, projSubject, projBody)
        elif self.creationType == 'reply':
            self.agent._CreateSettings('none', '', 'reply', 'LinksList', threadsCount, projSubject, projBody)
        elif self.creationType == 'reg + post' and self.registerRun:
            self.agent._CreateSettings('register-only', '', 'post', 'LinksList', threadsCount, projSubject, projBody)
        elif self.creationType == 'reg + post' and not self.registerRun:
            self.agent._CreateSettings('from-registered', '', 'post', 'LinksList', threadsCount, projSubject, projBody)
        elif self.creationType == 'reg + reply' and self.registerRun:
            self.agent._CreateSettings('register-only', '', 'reply', 'LinksList', threadsCount, projSubject, projBody)
        elif self.creationType == 'reg + reply' and not self.registerRun:
            self.agent._CreateSettings('from-registered', '', 'reply', 'LinksList', threadsCount, projSubject, projBody)
    
    def ActionOff(self):
        '''Копируем анкоры и удаляем базу, которую копировали ранее'''
        self.linker.AddSpamAnchorsFile()
        if self.agent.currentTask['baseType'] == 'RLinksList':
            self._FilterBase(self.agent.baseMainRFile)
            self._DeleteBase(self.agent.baseMainFile) 
        elif self.agent.currentTask['baseType'] == 'ZLinksList':
            self._FilterBase(self.agent.baseMainZFile)
            self._DeleteBase(self.agent.baseMainFile) 
        else:
            pass

class XrumerHelperSpamTask(XrumerHelper):
    '''Задание для спама по базам L, R и Z'''
    
    def __init__(self, agent):
        '''Обработка параметров агента'''
        if 'baseZ' in agent.currentTask:
            agent.currentTask['baseType'] = 'ZLinksList'
            agent.currentTask['baseNumberMain'] = int(agent.currentTask['baseZ'])
        if 'baseL' in agent.currentTask:
            agent.currentTask['baseType'] = 'LinksList'
            agent.currentTask['baseNumberMain'] = int(agent.currentTask['baseL'])
            agent.currentTask['nickName'] = agent.currentTask['nickNameRandom']
            agent.currentTask['realName'] = agent.currentTask['realNameRandom']
            agent.currentTask['password'] = agent.currentTask['passwordRandom']
            agent.currentTask['emailAddress'] = agent.currentTask['emailAddressRandom']
        super(XrumerHelperSpamTask, self).__init__(agent)
        
    def GetProjectName(self):
        return 'ProjectS%d' % self.agent.currentTask['id']
    
    def ActionOn(self):
        '''Содержимое проекта'''
        spamLinksList = escape(codecs.decode(' '.join(self.agent.currentTask['spamLinksList']), 'cp1251'))
        projSubject = '#file_links[%s,1,N]' % (self.keywordsFileEsc)
        projBody = '#file_links[%s,7,S] %s #file_links[%s,3,S] #file_links[%s,3,S] #file_links[%s,3,S]' % (self.snippetsFileEsc, spamLinksList, self.anchorsFileEsc, self.profilesFileEsc, self.snippetsFileEsc)
        '''Пишем кейворды'''
        self._WriteKeywords()
        '''Создаем настройки'''
        if self.agent.currentTask['baseType'] == 'RLinksList':
            self.agent._CreateSettings('from-registered', '', 'reply', 'RLinksList', 160, projSubject, projBody)
        elif self.agent.currentTask['baseType'] == 'ZLinksList':
            self.agent._CreateSettings('none', '', 'post', 'ZLinksList', 160, projSubject, projBody, '', '', random.randint(1, 999))
        else:
            self.agent._CreateSettings('none', '', 'post-reply', 'LinksList', 160, projSubject, projBody, '', '', random.randint(1, 999))
    
    def ActionOff(self):
        '''Копируем анкоры и фильтруем базу R или Z от неуспешных'''
        self.linker.AddSpamAnchorsFile()
        if self.agent.currentTask['baseType'] == 'RLinksList':
            self._FilterBase(self.agent.baseMainRFile)
        elif self.agent.currentTask['baseType'] == 'ZLinksList':
            self.agent._CountLinks('baseLinksCount', self.agent.baseMainZFile, 'base')
        else:
            self.agent._CountLinks('baseLinksCount', self.agent.baseMainFile, 'base')

class XrumerHelperBaseDoors(XrumerHelper):
    '''Доры на форумах'''
    
    def GetProjectName(self):
        return 'ProjectD%d' % self.agent.currentTask['id']
    
    def ActionOn(self):
        '''Содержимое проекта'''
        body = escape(self.agent.currentTask['body'])
        projSubject = '#file_links[%s,1,N]' % (self.keywordsFileEsc)
        projBody = '%s #file_links[%s,10,L] #file_links[%s,3,L] #file_links[%s,3,L] #file_links[%s,10,S]' % (body, self.keywordsFileEsc, self.anchorsFileEsc, self.profilesFileEsc, self.snippetsFileEsc)
        '''Если первый проход'''
        if not os.path.isfile(self.agent.baseMainRFile):
            '''Пишем кейворды, копируем исходную базу в целевую и удаляем существующую базу R'''
            self._WriteKeywords()
            self._CopyBase(self.agent.baseSourceFile, self.agent.baseMainFile)
            self._DeleteBase(self.agent.baseMainRFile) 
            '''Создаем настройки'''
            threadsCount = 110
            if self.creationType == 'post':
                self.agent._CreateSettings('none', '', 'post', 'LinksList', threadsCount, projSubject, projBody)
            elif self.creationType == 'reply':
                self.agent._CreateSettings('none', '', 'reply', 'LinksList', threadsCount, projSubject, projBody)
            elif self.creationType == 'reg + post' and self.registerRun:
                self.agent._CreateSettings('register-only', '', 'post', 'LinksList', threadsCount, projSubject, projBody)
            elif self.creationType == 'reg + post' and not self.registerRun:
                self.agent._CreateSettings('from-registered', '', 'post', 'LinksList', threadsCount, projSubject, projBody)
            elif self.creationType == 'reg + reply' and self.registerRun:
                self.agent._CreateSettings('register-only', '', 'reply', 'LinksList', threadsCount, projSubject, projBody)
            elif self.creationType == 'reg + reply' and not self.registerRun:
                self.agent._CreateSettings('from-registered', '', 'reply', 'LinksList', threadsCount, projSubject, projBody)
        else:
            '''Пишем кейворды'''
            self._WriteKeywords()
            '''Создаем настройки'''
            self.agent._CreateSettings('from-registered', '', 'reply', 'RLinksList', 160, projSubject, projBody, '', '', random.randint(0, 19))
            
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
        self.agent._DeleteLog(self.agent.logAnchors)
        self.agent._DeleteLog(self.agent.logProfiles)
        if self.registerRun:
            '''Копируем исходную базу в целевую'''
            self._CopyBase(self.agent.baseSourceFile, self.agent.baseMainFile)
            '''Создаем настройки'''
            self.agent._CreateSettings('register-only', '', 'post', 'LinksList', 100, 'none', 'none', '', '')
        else:
            '''Создаем настройки'''
            self.agent._CreateSettings('from-registered', 'edit-profile', 'post', 'LinksList', 100, 'none', r'#file_links[x:\foo.txt,1,N]', self.agent.currentTask['homePage'], self.agent.currentTask['signature'])
    
    def ActionOff(self):
        '''Фильтруем базу от неуспешных и копируем профили для последующего спама'''
        self._FilterBase(self.agent.baseMainFile)
        if not self.registerRun:
            self.linker.AddProfilesFile()
