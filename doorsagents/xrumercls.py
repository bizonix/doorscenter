# coding=utf8
import os, shutil, codecs, random, string, kwk8, baseparser, basechecker
from xml.sax.saxutils import escape
from xrumerxdf import *

'''Классы XrumerHelperBaseSpam и XrumerHelperBaseDoors не протестированы на 
работу с предварительной регистрацией.'''

class XrumerHelper(object):
    '''Абстрактный предок хэлперов'''
    
    def __init__(self, agent):
        self.agent = agent
        self.currentTask = self.agent.currentTask
        self.linker = XrumerTopicLinker(self)
        self.creationType = self.currentTask['creationType']
        self.registerRun = self.currentTask['registerRun']
        snippetsFolder = os.path.dirname(os.path.abspath(__file__)) + '/snippets'
        keywordsFolder = os.path.join(self.agent.appFolder, 'Keywords')
        self.keywordsFile = os.path.join(keywordsFolder, '%s.txt' % self.currentTask['niche'])
        self.keywordsFileEsc = escape(self.keywordsFile)
        self.snippetsFileEsc = escape(os.path.join(snippetsFolder, self.currentTask['snippetsFile']))
        self.anchorsFileEsc = escape(self.linker.GetSpamAnchorsFile())
        self.profilesFileEsc = escape(self.linker.GetProfilesFile())
    
    def _WriteKeywords(self):
        '''Пишем кейворды'''
        with codecs.open(self.keywordsFile, 'w', 'cp1251') as fd:
            fd.write('\n'.join(self.currentTask['keywordsList']))
    
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
        return 'ProjectX%d' % self.currentTask['id']
    
    def ActionOn(self):
        '''Действия при старте'''
        pass
    
    def ActionOff(self):
        '''Действия при финише'''
        pass

class XrumerHelperBaseRaw(XrumerHelper):
    '''Парсим и чекаем новую базу'''
    
    def GetProjectName(self):
        return 'ProjectN%d' % self.currentTask['id']
    
    def ActionOn(self):
        '''Парсим базу'''
        parseTimeout = 90 * 60
        if 'parseTimeout' in self.currentTask:
            parseTimeout = int(self.currentTask['parseTimeout']) * 60
        startTopics = self.currentTask['parseParams']
        baseparser.Parse(self.agent.appFolder, startTopics, parseTimeout, self.currentTask['baseNumberMain'])
        '''Содержимое проекта'''
        randomToken = ''.join(random.choice(string.letters) for _ in xrange(10))
        projSubject = '#file_links[%s,1,N]' % (self.keywordsFileEsc)
        projBody = '#file_links[%s,10,S] %s #file_links[%s,3,S] #file_links[%s,3,S] #file_links[%s,10,S]' % (self.snippetsFileEsc, randomToken, self.anchorsFileEsc, self.profilesFileEsc, self.snippetsFileEsc)
        '''Пишем кейворды и удаляем старые базы'''
        self._WriteKeywords()
        self._DeleteBase(self.agent.baseMainRFile)
        self._DeleteBase(self.agent.baseMainZFile)
        self._DeleteBase(self.agent.baseMainEFile)
        '''Создаем настройки'''
        threadsCount = 110
        self.agent._CreateSettings('none', '', 'post', 'LinksList', threadsCount, projSubject, projBody)
    
    def ActionOff(self):
        '''Проверяем базу'''
        basechecker.Check(self.agent.appFolder, self.agent.projectName, self.currentTask['baseNumberMain'])
        '''Считаем число ссылок'''
        self.agent._CountLinks('baseLinksCount', self.agent.baseMainFile, 'base')
        
class XrumerHelperBaseSpam(XrumerHelper):
    '''Базы L, R и Z для спама по топикам'''
    
    def GetProjectName(self):
        return 'ProjectR%d' % self.currentTask['id']
    
    def ActionOn(self):
        '''Содержимое проекта'''
        spamLinksList = escape(codecs.decode(' '.join(self.currentTask['spamLinksList']), 'cp1251'))
        projSubject = '#file_links[%s,1,N]' % (self.keywordsFileEsc)
        projBody = '#file_links[%s,10,S] %s #file_links[%s,3,S] #file_links[%s,3,S] #file_links[%s,10,S]' % (self.snippetsFileEsc, spamLinksList, self.anchorsFileEsc, self.profilesFileEsc, self.snippetsFileEsc)
        '''Пишем кейворды, копируем исходную базу в целевую и удаляем существующую базу R или Z'''
        self._WriteKeywords()
        self._CopyBase(self.agent.baseSourceFile, self.agent.baseMainFile)
        if self.currentTask['baseType'] == 'RLinksList':
            self._DeleteBase(self.agent.baseMainRFile)
        elif self.currentTask['baseType'] == 'ZLinksList': 
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
        if self.currentTask['baseType'] == 'RLinksList':
            self._FilterBase(self.agent.baseMainRFile)
            self._DeleteBase(self.agent.baseMainFile) 
        elif self.currentTask['baseType'] == 'ZLinksList':
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
            agent.currentTask['nickName'] = agent.currentTask['nickNameRandom']
            agent.currentTask['realName'] = agent.currentTask['realNameRandom']
            agent.currentTask['password'] = agent.currentTask['passwordRandom']
            agent.currentTask['emailAddress'] = agent.currentTask['emailAddressRandom']
        if 'baseL' in agent.currentTask:
            agent.currentTask['baseType'] = 'LinksList'
            agent.currentTask['baseNumberMain'] = int(agent.currentTask['baseL'])
            agent.currentTask['nickName'] = agent.currentTask['nickNameRandom']
            agent.currentTask['realName'] = agent.currentTask['realNameRandom']
            agent.currentTask['password'] = agent.currentTask['passwordRandom']
            agent.currentTask['emailAddress'] = agent.currentTask['emailAddressRandom']
        super(XrumerHelperSpamTask, self).__init__(agent)
        
    def GetProjectName(self):
        return 'ProjectS%d' % self.currentTask['id']
    
    def ActionOn(self):
        '''Содержимое проекта'''
        spamLinksList = escape(codecs.decode(' '.join(self.currentTask['spamLinksList']), 'cp1251'))
        projSubject = '#file_links[%s,1,N]' % (self.keywordsFileEsc)
        projBody = '#file_links[%s,10,S] %s #file_links[%s,3,S] #file_links[%s,3,S] #file_links[%s,10,S]' % (self.snippetsFileEsc, spamLinksList, self.anchorsFileEsc, self.profilesFileEsc, self.snippetsFileEsc)
        '''Пишем кейворды'''
        self._WriteKeywords()
        '''Создаем настройки'''
        if self.currentTask['baseType'] == 'RLinksList':
            self.agent._CreateSettings('from-registered', '', 'reply', 'RLinksList', 160, projSubject, projBody)
        elif self.currentTask['baseType'] == 'ZLinksList':
            self.agent._CreateSettings('none', '', 'post', 'ZLinksList', 160, projSubject, projBody, '', '', random.randint(1, 999))
        else:
            self.agent._CreateSettings('none', '', 'post-reply', 'LinksList', 160, projSubject, projBody, '', '', random.randint(1, 999))
    
    def ActionOff(self):
        '''Копируем анкоры и фильтруем базу R от неуспешных'''
        self.linker.AddSpamAnchorsFile()
        if self.currentTask['baseType'] == 'RLinksList':
            self._FilterBase(self.agent.baseMainRFile)
        elif self.currentTask['baseType'] == 'ZLinksList':
            self.agent._CountLinks('baseLinksCount', self.agent.baseMainZFile, 'base')
        else:
            self.agent._CountLinks('baseLinksCount', self.agent.baseMainFile, 'base')

class XrumerHelperBaseDoors(XrumerHelper):
    '''Доры на форумах'''
    
    def GetProjectName(self):
        return 'ProjectD%d' % self.currentTask['id']
    
    def ActionOn(self):
        '''Содержимое проекта'''
        body = escape(self.currentTask['body'])
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
        return 'ProjectP%d' % self.currentTask['id']
    
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
            self.agent._CreateSettings('from-registered', 'edit-profile', 'post', 'LinksList', 100, 'none', r'#file_links[x:\foo.txt,1,N]', self.currentTask['homePage'], self.currentTask['signature'])
    
    def ActionOff(self):
        '''Фильтруем базу от неуспешных и копируем профили для последующего спама'''
        self._FilterBase(self.agent.baseMainFile)
        if not self.registerRun:
            self.linker.AddProfilesFile()
