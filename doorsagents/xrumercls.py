# coding=utf8
import os, shutil, codecs, kwk8
from xml.sax.saxutils import escape

class XrumerHelper():
    '''Абстрактный предок хэлперов'''
    
    def __init__(self, agent):
        self.agent = agent
        self.linker = XrumerTopicLinker(self)
        self.creationType = self.agent.currentTask['creationType']
        self.registerRun = self.agent.currentTask['registerRun']
    
    def GetProjectName(self):
        return 'Project%d' % self.agent.currentTask['id']
    
    def ActionOn(self):
        pass
    
    def ActionOff(self):
        pass
    
class XrumerHelperBaseSpam(XrumerHelper):
    '''База R для спама по топикам'''
    
    def GetProjectName(self):
        return 'ProjectR%d' % self.agent.currentTask['id']
    
    def ActionOn(self):
        '''Пишем кейворды'''
        with codecs.open(self.agent.keywordsFile, 'w', 'cp1251') as fd:
            fd.write('\n'.join(self.agent.currentTask['keywordsList']))
        '''Содержимое проекта'''
        keywordsFile = escape(self.agent.keywordsFile)
        snippetsFile = escape(self.agent.snippetsFile)
        spamLinksList = escape(codecs.decode(' '.join(self.agent.currentTask['spamLinksList']), 'cp1251'))
        anchorsFile = escape(self.linker.GetSpamAnchorsFile())
        profilesFile = escape(self.linker.GetProfilesFile())
        projSubject = '#file_links[%s,1,N]' % (keywordsFile)
        projBody = '#file_links[%s,7,S] %s #file_links[%s,3,S] #file_links[%s,3,S] #file_links[%s,3,S]' % (snippetsFile, spamLinksList, anchorsFile, profilesFile, snippetsFile)
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
        '''Копируем исходную базу в целевую'''
        try:
            shutil.copyfile(self.agent.baseSourceFile, self.agent.baseMainFile)
        except Exception as error:
            print('Cannot copy source base to main: %s' % error)
        '''Удаляем существующую базу R'''
        if os.path.isfile(self.agent.baseMainRFile): 
            try:
                os.remove(self.agent.baseMainRFile)
            except Exception as error:
                print('Cannot remove old base R: %s' % error)
    
    def ActionOff(self):
        '''Копируем анкоры'''
        self.linker.AddSpamAnchorsFile(self.agent.logAnchors)
        '''Удаляем целевую базу, которую копировали ранее'''
        if os.path.isfile(self.agent.baseMainFile): 
            try:
                os.remove(self.agent.baseMainFile)
            except Exception as error:
                print('Cannot remove old base R: %s' % error)

class XrumerHelperSpamTask(XrumerHelper):
    '''Задание для спама по топикам'''
    
    def GetProjectName(self):
        return 'ProjectS%d' % self.agent.currentTask['id']
    
    def ActionOn(self):
        '''Содержимое проекта'''
        keywordsFile = escape(self.agent.keywordsFile)
        snippetsFile = escape(self.agent.snippetsFile)
        spamLinksList = escape(codecs.decode(' '.join(self.agent.currentTask['spamLinksList']), 'cp1251'))
        anchorsFile = escape(self.linker.GetSpamAnchorsFile())
        profilesFile = escape(self.linker.GetProfilesFile())
        projSubject = '#file_links[%s,1,N]' % (keywordsFile)
        projBody = '#file_links[%s,7,S] %s #file_links[%s,3,S] #file_links[%s,3,S] #file_links[%s,3,S]' % (snippetsFile, spamLinksList, anchorsFile, profilesFile, snippetsFile)
        '''Создаем настройки'''
        threadsCount = 160
        controlTimeRange = 60
        self.agent._CreateSettings('from-registered', '', 'reply', 'RLinksList', threadsCount, controlTimeRange, projSubject, projBody)
    
    def ActionOff(self):
        '''Копируем анкоры'''
        self.linker.AddSpamAnchorsFile(self.agent.logAnchors)
        '''Фильтруем базу R от неуспешных'''
        try:
            if kwk8.Kwk8Links(self.agent.logFails).Count() > 700:
                kwk8.Kwk8Links(self.agent.baseMainRFile).DeleteByFile(self.agent.logFails).Save(self.agent.baseMainRFile)
        except Exception as error:
            print('Cannot filter new base R: %s' % error)

class XrumerHelperBaseDoors(XrumerHelper):
    '''Доры на форумах'''
    
    def GetProjectName(self):
        return 'ProjectD%d' % self.agent.currentTask['id']
    
    def ActionOn(self):
        '''Пишем кейворды'''
        with codecs.open(self.agent.keywordsFile, 'w', 'cp1251') as fd:
            fd.write('\n'.join(self.agent.currentTask['keywordsList']))
        '''Содержимое проекта'''
        body = escape(self.agent.currentTask['body'])
        keywordsFile = escape(self.agent.keywordsFile)
        snippetsFile = escape(self.agent.snippetsFile)
        anchorsFile = escape(self.linker.GetDoorsAnchorsFile())
        profilesFile = escape(self.linker.GetProfilesFile())
        projSubject = '#file_links[%s,1,N]' % (keywordsFile)
        projBody = '%s #file_links[%s,10,L] #file_links[%s,3,L] #file_links[%s,3,L] #file_links[%s,10,S]' % (body, keywordsFile, anchorsFile, profilesFile, snippetsFile)
        '''Если первый проход'''
        firstPost = not os.path.isfile(self.agent.baseMainRFile)
        if firstPost:
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
            '''Копируем исходную базу в целевую'''
            try:
                    shutil.copyfile(self.agent.baseSourceFile, self.agent.baseMainFile)
            except Exception as error:
                print('Cannot copy source base to main: %s' % error)
            '''Удаляем существующую базу R'''
            if os.path.isfile(self.agent.baseMainRFile): 
                try:
                    os.remove(self.agent.baseMainRFile)
                except Exception as error:
                    print('Cannot remove old base R: %s' % error)
        else:
            '''Создаем настройки'''
            threadsCount = 160
            controlTimeRange = 60
            self.agent._CreateSettings('from-registered', '', 'reply', 'RLinksList', threadsCount, controlTimeRange, projSubject, projBody)
            
    def ActionOff(self):
        '''Копируем анкоры'''
        self.linker.AddDoorsAnchorsFile(self.agent.logAnchors)
        '''Удаляем целевую базу, которую копировали ранее'''
        if os.path.isfile(self.agent.baseMainFile): 
            try:
                os.remove(self.agent.baseMainFile)
            except Exception as error:
                print('Cannot remove base: %s' % error)

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
        try:
            shutil.copyfile(self.agent.baseSourceFile, self.agent.baseMainFile)
        except Exception as error:
            print('Cannot copy source base to main: %s' % error)
    
    def ActionOff(self):
        '''Копируем профили для последующего спама'''
        if not self.registerRun:
            self.linker.AddProfilesFile(self.agent.logProfiles)

class XrumerTopicLinker(object):
    '''Менеджер перелинковки топиков и профилей'''

    def __init__(self, helper):
        self.helper = helper
        self.agent = self.helper.agent
        self.allFileName = 'total.txt'
        self.anchorsSpamFolder = os.path.join(self.agent.appFolder, 'AnchorsSpam')
        self.anchorsSpamFile = os.path.join(self.anchorsSpamFolder, self.allFileName)
        if not os.path.exists(self.anchorsSpamFile):
            open(self.anchorsSpamFile, 'w').write('')
        self.anchorsDoorsFolder = os.path.join(self.agent.appFolder, 'AnchorsDoors')
        self.anchorsDoorsFile = os.path.join(self.anchorsDoorsFolder, self.allFileName)
        if not os.path.exists(self.anchorsDoorsFile):
            open(self.anchorsDoorsFile, 'w').write('')
        self.anchorsProfilesFolder = os.path.join(self.agent.appFolder, 'AnchorsProfiles')
        self.anchorsProfilesFile = os.path.join(self.anchorsProfilesFolder, self.allFileName)
        if not os.path.exists(self.anchorsProfilesFile):
            open(self.anchorsProfilesFile, 'w').write('')
    
    def GetSpamAnchorsFile(self):
        '''Отдаем файл с анкорами по топикам спама'''
        return self.anchorsSpamFile
    
    def GetDoorsAnchorsFile(self):
        '''Отдаем файл с анкорами по дорам на форумах'''
        return self.anchorsDoorsFile
    
    def GetProfilesFile(self):
        '''Отдаем файл с анкорами по топикам спама'''
        return self.anchorsProfilesFile
    
    def AddSpamAnchorsFile(self, fileName):
        '''Копируем новые анкоры в базу'''
        self._AddAnchorsFile(fileName, self.anchorsSpamFolder)
    
    def AddDoorsAnchorsFile(self, fileName):
        '''Копируем новые анкоры в базу'''
        self._AddAnchorsFile(fileName, self.anchorsDoorsFolder)
    
    def AddProfilesFile(self, fileName):
        '''Копируем новые анкоры в базу'''
        self._AddAnchorsFile(fileName, self.anchorsProfilesFolder)

    def _AddAnchorsFile(self, fileName, anchorsFolder):
        '''Копируем файл в папку и объединяем имеющиеся файлы'''
        try:
            shutil.copy(fileName, anchorsFolder)
            with open(os.path.join(anchorsFolder, self.allFileName), 'w') as fd:
                for fileName in os.listdir(anchorsFolder):
                    if fileName != self.allFileName:
                        fd.write(open(os.path.join(anchorsFolder, fileName)).read())
        except Exception as error:
            print('Cannot update anchors: %s' % error)
