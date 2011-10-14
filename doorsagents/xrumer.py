# coding=utf8
import os, shutil, datetime, time, codecs, kwk8, agent, common, win32gui
from xml.sax.saxutils import escape

xrumerSettingsGroup1 = ('', 'register-only', 'from-registered')
xrumerSettingsGroup2 = ('edit-profile')
xrumerSettingsGroup3 = ('post', 'reply')
xrumerSettingsGroup4 = ('LinksList', 'RLinksList')

class XrumerAgent(agent.BaseAgent):
    ''' Параметры (см. методы GetTaskDetails и SetTaskDetails):
    Входные: niche, baseNumberMain, baseNumberSource, snippetsFile, nickName, realName, password, emailAddress, emailPassword, 
    emailLogin, emailPopServer, subject, spamLinksList, creationType, registerRun.
    Выходные: successCount, halfSuccessCount, failsCount, profilesCount, registeredAccountsCount, baseLinksCount.'''
    
    def _CreateSettings(self, settings1, settings2, settings3, settings4, threadsCount, controlTimeRange, 
                       projSubject, projBody, projHomePage = '', projSignature = ''):
        '''Создаем настройки'''
        configFile = os.path.join(self.appFolder, 'config.ini')
        settingsFile = os.path.join(self.appFolder, 'xuser.ini')
        scheduleFile = os.path.join(self.appFolder, 'schedule.xml')
        projectFile = os.path.join(self.appFolder, 'Projects', self.projectName + '.xml')
        settingsControl1File = os.path.join(self.appFolderControl1, 'control.ini')
        settingsControl2File = os.path.join(self.appFolderControl2, 'control.ini')
        
        '''Файл config.ini'''
        with open(configFile, 'r') as fd:
            config = fd.readlines()
        config[3] = '%d\n' % threadsCount
        config[8] = 'ON\n'  # автопродолжение
        with open(self.appConfigFile, 'w') as fd:
            fd.writelines(config)
        
        '''Файл xuser.ini'''
        settingsDict = {'OnlyRegistering': ('1' if settings1 == 'register-only' else '0'),
            'RegisteringPlusPosting': '0', 
            'FromRegistered': ('1' if settings1 == 'from-registered' else '0'), 
            'AggressiveMode': '0', 
            'CheckForActiveLink': '0', 
            'EditProfileAfterLogin': ('1' if settings2 == 'edit-profile' else '0'), 
            'UploadAvatars': '0', 
            'EnableRefspam': '0', 
            'BBtoHTML': '1', 
            'PostNewMode': ('1' if settings3 == 'post' else '3'),
            'SchedulerEnabled': '1',
            'CurrentJob': '0'}
        common.ModifyIniFile(settingsFile, settingsDict)
        
        '''Расписание schedule.xml'''
        with open(scheduleFile, 'w') as fd:
            fd.write('''<?xml version="1.0" encoding="UTF-8"?>
<body>
  <Schedule0>
    <PerformedTime></PerformedTime>
    <EventNum>2</EventNum>
    <EventParameter>''' + (datetime.datetime.now() + datetime.timedelta(0, 30)).strftime('%d.%m.%y %H:%M:%S') + '''</EventParameter>
    <JobNum>4</JobNum>
    <JobParameter>''' + escape(self.projectName) + '''</JobParameter>
  </Schedule0>
  <Schedule1>
    <PerformedTime></PerformedTime>
    <EventNum>6</EventNum>
    <EventParameter></EventParameter>
    <JobNum>12</JobNum>
    <JobParameter></JobParameter>
  </Schedule1>
  <Schedule2>
    <PerformedTime></PerformedTime>
    <EventNum>6</EventNum>
    <EventParameter></EventParameter>
    <JobNum>5</JobNum>
    <JobParameter>''' + ('0' if settings1 == 'LinksList' else '3') + '''</JobParameter>
  </Schedule2>
  <Schedule3>
    <PerformedTime></PerformedTime>
    <EventNum>6</EventNum>
    <EventParameter></EventParameter>
    <JobNum>10</JobNum>
    <JobParameter>''' + self.currentTask['baseNumber'] + '''</JobParameter>
  </Schedule3>
  <Schedule4>
    <PerformedTime></PerformedTime>
    <EventNum>6</EventNum>
    <EventParameter></EventParameter>
    <JobNum>1</JobNum>
    <JobParameter></JobParameter>
  </Schedule4>
  <Schedule5>
    <PerformedTime></PerformedTime>
    <EventNum>0</EventNum>
    <EventParameter></EventParameter>
    <JobNum>0</JobNum>
    <JobParameter></JobParameter>
  </Schedule5>
  <Schedule6>
    <PerformedTime></PerformedTime>
    <EventNum>6</EventNum>
    <EventParameter></EventParameter>
    <JobNum>13</JobNum>
    <JobParameter>''' + escape(self.doneScript) + '''</JobParameter>
  </Schedule6>
</body>
''')
            
        '''Проект'''
        with codecs.open(projectFile, 'w', 'utf8') as fd:
            fd.write('''<?xml version="1.0" encoding="UTF-8"?>
<XRumerProject>
  <PrimarySection>
    <ProjectName>''' + escape(self.projectName) + '''</ProjectName>
    <NickName>''' + escape(self.currentTask['nickName']) + '''</NickName>
    <RealName>''' + escape(self.currentTask['realName']) + '''</RealName>
    <Password>''' + escape(self.currentTask['password']) + '''</Password>
    <EmailAddress>''' + escape(self.currentTask['emailAddress']) + '''</EmailAddress>
    <EmailPassword>''' + escape(self.currentTask['emailPassword']) + '''</EmailPassword>
    <EmailLogin>''' + escape(self.currentTask['emailLogin']) + '''</EmailLogin>
    <EmailPOP>''' + escape(self.currentTask['emailPopServer']) + '''</EmailPOP>
    <Homepage>''' + projHomePage + '''</Homepage>
    <ICQ></ICQ>
    <City>#file_links[C:\Work\lists\cities-en.txt]</City>
    <Country>#file_links[C:\Work\lists\countries-en.txt]</Country>
    <Occupation></Occupation>
    <Interests></Interests>
    <Signature>''' + projSignature + '''</Signature>
    <Gender>0</Gender>
    <UnknownFields></UnknownFields>
    <PollTitle></PollTitle>
    <PollOption1></PollOption1>
    <PollOption2></PollOption2>
    <PollOption3></PollOption3>
    <PollOption4></PollOption4>
    <PollOption5></PollOption5>
  </PrimarySection>
  <SecondarySection>
    <Subject1>''' + projSubject + '''</Subject1>
    <Subject2></Subject2>
    <PostText>''' + projBody + '''</PostText>
    <Prior></Prior>
    <OnlyPriors>false</OnlyPriors>
  </SecondarySection>
</XRumerProject>
''')
    
        '''Настройки control.exe'''
        with open(settingsControl1File, 'w') as fd:
            fd.write('''[Settings]
ApplicationName=''' + self.appApplication + '''
Mode=0
TimeRange=''' + str(controlTimeRange) + '''
''')
        with open(settingsControl2File, 'w') as fd:
            fd.write('''[Settings]
ApplicationName=''' + self.appApplication + '''
Mode=1
TimeRange=''' + str(controlTimeRange) + '''
''')
    
    def _Settings(self):
        '''Создание класса-хелпера'''
        if self.currentTask['type'] == 'XrumerBaseSpam':
            self.helper = XrumerHelperBaseSpam()
        elif self.currentTask['type'] == 'SpamTask':
            self.helper = XrumerHelperSpamTask()
        elif self.currentTask['type'] == 'XrumerBaseDoors':
            self.helper = XrumerHelperBaseDoors()
        elif self.currentTask['type'] == 'XrumerBaseProfiles':
            self.helper = XrumerHelperBaseProfiles()
        '''Настройки'''
        self.appFolder = 'D:\\Miscellaneous\\Lodger6\\xrumer707'
        self.appFolderControl1 = 'D:\\Miscellaneous\\Lodger6\\control1'
        self.appFolderControl2 = 'D:\\Miscellaneous\\Lodger6\\control2'
        self.appApplication = os.path.join(self.appFolder, 'xpymep.exe')
        self.appApplicationControl1 = os.path.join(self.appFolderControl1, 'control.exe')
        self.appApplicationControl2 = os.path.join(self.appFolderControl2, 'control.exe')
        self.appCaption = 'XRumer 7.07 Elite, Copyright BotmasterRu.Com, Support ICQ 876975, Administration e-mail botmaster@bk.ru'
        self.appCaptionControl = 'Control of permanent running'
        self.doneScript = 'C:\\Work\\doorscenter\\doorsagents\\xrumer-done.bat'
        self.snippetsFolder = 'C:\\Work\\snippets'
        self.snippetsFile = os.path.join(self.snippetsFolder, self.currentTask['snippetsFile'])
        self.projectName = self.helper.GetProjectName()
        self.logFileTemplate = os.path.join(self.appFolder, 'Logs', self.projectName, '%s id%d.txt' % ('%s', self.currentTask['baseNumber']))
        self.logSuccess = self.logFileTemplate % 'Success'
        self.logHalfSuccess = self.logFileTemplate % 'Halfsuccess'
        self.logFails = self.logFileTemplate % 'Others'
        self.logProfiles = self.logFileTemplate % 'Profiles'
        self.logRegisteredAccounts = os.path.join(self.appFolder, 'Logs', self.projectName, 'Registered Accounts.txt')
        self.logAnchors = self.logFileTemplate % 'Anchors'
        self.nicheAnchorsFile = os.path.join(self.appFolder, 'Anchors', '%s.txt' % self.currentTask['niche'])
        self.subjectsFile = os.path.join(self.appFolder, 'Subjects', '%s.txt' % self.currentTask['niche'])
        self.appLinksFolder = os.path.join(self.appFolder, 'Links')
        self.baseMainFile = os.path.join(self.appLinksFolder, 'LinksList id%d.txt' % self.currentTask['baseNumberMain'])
        self.baseMainRFile = os.path.join(self.appLinksFolder, 'RLinksList id%d.txt' % self.currentTask['baseNumberMain'])
        self.baseSourceFile = os.path.join(self.appLinksFolder, 'LinksList id%d.txt' % self.currentTask['baseNumberSource'])
        self.baseSourceRFile = os.path.join(self.appLinksFolder, 'RLinksList id%d.txt' % self.currentTask['baseNumberSource'])
        
    def _CloseApp(self, appCaption):
        '''Закрытие приложения под Windows по заголовку окна'''
        p = win32gui.FindWindow(None, appCaption)
        win32gui.SendMessage(p, 0x10, 0, 0)
    
    def _FilterBaseR(self):
        '''Фильтрация базы R по успешным и полууспешным'''
        logTemp = self.logFileTemplate % 'Temporary'
        with open(logTemp, 'w') as fd:
            for line in open(self.logSuccess, 'r'):
                fd.write(line)
            for line in open(self.logHalfSuccess, 'r'):
                fd.write(line)
        kwk8.Kwk8Links(self.baseMainRFile).SelectByFile(logTemp).Save(self.baseMainRFile)
        os.unlink(logTemp)
        
    def _ActionOn(self):
        self._Settings()
        '''Вызываем хэлпер'''
        self.helper.ActionOn()
        '''Если анкоров по нише нет, создаем пустой файл'''
        if not os.path.exists(self.nicheAnchorsFile):
            with open(self.nicheAnchorsFile, 'w') as fd:
                fd.write('')
        '''Запуск приложений'''
        self._RunApp(self.appApplication)
        time.sleep(3)
        self._RunApp(self.appApplicationControl1)
        time.sleep(1)
        self._RunApp(self.appApplicationControl2)
        return True

    def _ActionOff(self):
        self._Settings()
        '''Значения по умолчанию'''
        self.currentTask['successCount'] = 0
        self.currentTask['halfSuccessCount'] = 0 
        self.currentTask['failsCount'] = 0 
        self.currentTask['profilesCount'] = 0
        self.currentTask['registeredAccountsCount'] = 0
        self.currentTask['baseLinksCount'] = 0
        '''Закрытие приложений'''
        self._CloseApp(self.appCaptionControl)
        time.sleep(1)
        self._CloseApp(self.appCaptionControl)
        time.sleep(3)
        self._CloseApp(self.appCaption)
        '''Вызываем хэлпер'''
        self.helper.ActionOff()
        '''Копирование анкоров'''
        try:
            shutil.copyfile(self.logAnchors, self.nicheAnchorsFile)
        except Exception as error:
            print('Cannot copy anchors: %s' % error)
        '''Выходные параметры'''
        self.currentTask['spamLinksList'] = []
        try:
            self.currentTask['successCount'] = kwk8.Kwk8Links(self.logSuccess).Count()
        except Exception as error:
            print('Cannot count success links: %s' % error)
        try:
            self.currentTask['halfSuccessCount'] = kwk8.Kwk8Links(self.logHalfSuccess).Count()
        except Exception as error:
            print('Cannot count halfsuccess links: %s' % error)
        try:
            self.currentTask['failsCount'] = kwk8.Kwk8Links(self.logFails).Count()
        except Exception as error:
            print('Cannot count fails links: %s' % error)
        try:
            self.currentTask['profilesCount'] = kwk8.Kwk8Links(self.logProfiles).Count()
        except Exception as error:
            print('Cannot count profiles links: %s' % error)
        try:
            self.currentTask['registeredAccountsCount'] = kwk8.Kwk8Links(self.logRegisteredAccounts).Count()
        except Exception as error:
            print('Cannot count success links: %s' % error)
        try:
            self.currentTask['baseLinksCount'] = kwk8.Kwk8Links(self.baseMainRFile).Count()
        except Exception as error:
            print('Cannot count base R links: %s' % error)
        return True

class XrumerHelper():
    '''Абстрактный предок хэлперов'''
    def __init__(self, agent):
        self.agent = agent
        self.creationType = self.agent.currentTask['creationType']
        self.registerRun = self.agent.currentTask['registerRun']
    def GetProjectName(self):
        return 'Project%d' % self.agent.currentTask['id']
    def ActionOn(self):
        pass
    def ActionOff(self):
        pass
    
class XrumerHelperBaseSpam():
    '''База R для спама по топикам'''
    def GetProjectName(self):
        return 'ProjectR%d' % self.agent.currentTask['id']
    def ActionOn(self):
        '''Содержимое проекта'''
        projSubject = '#file_links[%s,1,N]' % (escape(self.agent.subjectsFile))
        projBody = '#file_links[%s,7,S] %s #file_links[%s,1,N]' % (escape(self.agent.snippetsFile), escape(codecs.decode(' '.join(self.agent.currentTask['spamLinksList']), 'cp1251')), escape(self.agent.nicheAnchorsFile))
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
        '''Пишем темы'''
        with codecs.open(self.agent.subjectsFile, 'w', 'cp1251') as fd:
            fd.write('\n'.join(self.agent.currentTask['subjectsList']))
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
        '''Удаляем целевую базу, которую копировали ранее'''
        if os.path.isfile(self.agent.baseMainFile): 
            try:
                os.remove(self.agent.baseMainFile)
            except Exception as error:
                print('Cannot remove old base R: %s' % error)

class XrumerHelperSpamTask():
    '''Задание для спама по топикам'''
    def GetProjectName(self):
        return 'ProjectS%d' % self.agent.currentTask['id']
    def ActionOn(self):
        '''Содержимое проекта'''
        projSubject = '#file_links[%s,1,N]' % (escape(self.agent.subjectsFile))
        projBody = '#file_links[%s,7,S] %s #file_links[%s,1,N]' % (escape(self.agent.snippetsFile), escape(codecs.decode(' '.join(self.agent.currentTask['spamLinksList']), 'cp1251')), escape(self.agent.nicheAnchorsFile))
        '''Создаем настройки'''
        threadsCount = 160
        controlTimeRange = 60
        self.agent._CreateSettings('from-registered', '', 'reply', 'RLinksList', threadsCount, controlTimeRange, projSubject, projBody)
    def ActionOff(self):
        '''Фильтрация базы R по успешным и полууспешным'''
        try:
            if kwk8.Kwk8Links(self.agent.logFails).Count() > 700:
                self.agent._FilterBaseR()
        except Exception as error:
            print('Cannot filter new base R: %s' % error)

class XrumerHelperBaseDoors():
    '''Доры на форумах'''
    def GetProjectName(self):
        return 'ProjectD%d' % self.agent.currentTask['id']
    def ActionOn(self):
        pass
    def ActionOff(self):
        pass

class XrumerHelperBaseProfiles():
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
            self.agent._CreateSettings('from-registered', 'edit-profile', 'post', 'LinksList', threadsCount, controlTimeRange, 'none', '#file_links[x:\foo.txt,1,N]', self.agent.currentTask['homePage'], self.agent.currentTask['signature'])
    def ActionOff(self):
        pass

if __name__ == '__main__':
    agent = XrumerAgent('http://127.0.0.1:8000/doorsadmin', 3)
