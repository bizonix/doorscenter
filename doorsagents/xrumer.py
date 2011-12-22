# coding=utf8
import os, shutil, datetime, time, codecs, kwk8, agent, common, win32gui
from xrumercls import *
from xml.sax.saxutils import escape

xrumerSettingsGroup1 = ('none', 'register-only', 'from-registered')
xrumerSettingsGroup2 = ('edit-profile')
xrumerSettingsGroup3 = ('post', 'post-reply', 'reply')
xrumerSettingsGroup4 = ('LinksList', 'RLinksList', 'ZLinksList')

class XrumerAgent(agent.BaseAgent):
    ''' Параметры (см. методы GetTaskDetails и SetTaskDetails):
    Входные: niche, baseNumberMain, baseNumberSource, snippetsFile, nickName, realName, password, emailAddress, emailPassword, 
    emailLogin, emailPopServer, subject, spamLinksList, creationType, registerRun, baseType.
    Выходные: successCount, halfSuccessCount, failsCount, profilesCount, registeredAccountsCount, baseLinksCount.'''
    
    def _DeleteLog(self, logFileName):
        '''Удаляем логи'''
        if os.path.isfile(logFileName): 
            try:
                os.remove(logFileName)
            except Exception as error:
                print('Cannot remove log: %s' % error)
    
    def _ModifyName(self, name, addon):
        '''Изменяем имя для рассылки от разных пользователей'''
        if addon != 0:
            name = name.replace(']', '%d]' % addon)
        return name
    
    def _ModifyPassword(self, password, addon):
        '''Изменяем пароль для рассылки от разных пользователей'''
        if addon != 0:
            password += str(addon)
        return password
    
    def _CreateSettings(self, settings1, settings2, settings3, settings4, threadsCount,  
                       projSubject, projBody, projHomePage = '', projSignature = '', 
                       nameAddon = 0):
        '''Создаем настройки'''
        configFile = os.path.join(self.appFolder, 'config.ini')
        settingsFile = os.path.join(self.appFolder, 'xuser.ini')
        scheduleFile = os.path.join(self.appFolder, 'schedule.xml')
        projectFile = os.path.join(self.appFolder, 'Projects', self.projectName + '.xml')
        settingsControl1File = os.path.join(self.appFolderControl1, 'control.ini')
        settingsControl2File = os.path.join(self.appFolderControl2, 'control.ini')
        
        '''Считаем число ссылок в базе'''
        baseLinksCount = 0
        try:
            baseLinksCount = max(kwk8.Kwk8Links(self.baseMainFile if settings4 == 'LinksList' else (self.baseMainRFile if settings4 == 'RLinksList' else (self.baseMainZFile))).Count() - 1, 0)
        except Exception as error:
            print('Cannot count links: %s' % error)
        
        '''Удаляем старый LastURL'''
        if os.path.isfile(self.logLastURL): 
            try:
                os.remove(self.logLastURL)
            except Exception as error:
                print('Cannot remove last url: %s' % error)

        '''Файл config.ini'''
        with open(configFile, 'r') as fd:
            config = fd.readlines()
        config[0] = '%s\n' % self.projectName
        config[2] = '%d\n' % self.currentTask['baseNumberMain']
        config[3] = '%d\n' % threadsCount
        config[5] = '%s\n' % ('ON' if settings1 == 'register-only' else 'OFF')  # использовать прокси (socks)
        config[8] = 'ON\n'  # автопродолжение
        config[9] = '%s\n' % ('ON' if settings1 == 'register-only' else 'OFF')
        config[11] = '%s\n' % ('0' if settings4 == 'LinksList' else ('3' if settings4 == 'RLinksList' else ('1')))
        with open(configFile, 'w') as fd:
            fd.writelines(config)
        
        '''Файл xuser.ini'''
        settingsDict = {'OnlyRegistering': ('1' if settings1 == 'register-only' else '0'),
            'RegisteringPlusPosting': '0', 
            'FromRegistered': ('1' if settings1 == 'from-registered' else '0'), 
            'AggressiveMode': '0', 
            'CheckForActiveLink': '0', 
            'EditProfileAfterLogin': ('1' if settings2 == 'edit-profile' else '0'), 
            'UploadAvatars': ('1' if settings2 == 'edit-profile' else '0'), 
            'LogInIfBusy': '0',
            'BBtoHTML': '1', 
            'EnableRefspam': '0', 
            'PostNewMode': ('1' if settings3 == 'post' else ('3' if settings3 == 'reply' else '2')),
            'SchedulerEnabled': '1',
            'CurrentJob': '0',
            'EnableSleepMode': '0'}
        common.ModifyIniFile(settingsFile, settingsDict)

        '''Расписание schedule.xml'''
        with open(scheduleFile, 'w') as fd:
            fd.write('''<?xml version="1.0" encoding="UTF-8"?>
<body>
  <Schedule0>
    <PerformedTime></PerformedTime>
    <EventNum>4</EventNum>
    <EventParameter>''' + str(baseLinksCount) + '''</EventParameter>
    <JobNum>0</JobNum>
    <JobParameter></JobParameter>
  </Schedule0>
  <Schedule1>
    <PerformedTime></PerformedTime>
    <EventNum>6</EventNum>
    <EventParameter></EventParameter>
    <JobNum>13</JobNum>
    <JobParameter>''' + escape(self.doneScript) + '''</JobParameter>
  </Schedule1>
</body>
''')
            
        '''Проект'''
        with codecs.open(projectFile, 'w', 'utf8') as fd:
            fd.write('''<?xml version="1.0" encoding="UTF-8"?>
<XRumerProject>
  <PrimarySection>
    <ProjectName>''' + escape(self.projectName) + '''</ProjectName>
    <NickName>''' + escape(self._ModifyName(self.currentTask['nickName'], nameAddon)) + '''</NickName>
    <RealName>''' + escape(self._ModifyName(self.currentTask['realName'], nameAddon)) + '''</RealName>
    <Password>''' + escape(self._ModifyPassword(self.currentTask['password'], nameAddon)) + '''</Password>
    <EmailAddress>''' + escape(self._ModifyName(self.currentTask['emailAddress'], nameAddon)) + '''</EmailAddress>
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
    <Gender>1</Gender>
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
    <Prior>''' + ('zxcvfdsa' if settings2 == 'edit-profile' else '') + '''</Prior>
    <OnlyPriors>''' + ('true' if settings2 == 'edit-profile' else 'false') + '''</OnlyPriors>
  </SecondarySection>
</XRumerProject>
''')
    
        '''Настройки control.exe'''
        timeout = '30'
        if 'timeout' in self.currentTask:
            timeout = self.currentTask['timeout']
        with open(settingsControl1File, 'w') as fd:
            fd.write('''[Settings]
ApplicationName=''' + self.appApplication + '''
Mode=0
TimeRange=''' + timeout + '''
''')
        with open(settingsControl2File, 'w') as fd:
            fd.write('''[Settings]
ApplicationName=''' + self.appApplication + '''
Mode=1
TimeRange=''' + timeout + '''
''')
    
    def _Settings(self):
        '''Настройки'''
        self.appFolder = 'C:\\Work\\xrumer709'
        self.appFolderControl1 = 'C:\\Work\\control1'
        self.appFolderControl2 = 'C:\\Work\\control2'
        self.appApplication = os.path.join(self.appFolder, 'xpymep.exe')
        self.appApplicationControl1 = os.path.join(self.appFolderControl1, 'control.exe')
        self.appApplicationControl2 = os.path.join(self.appFolderControl2, 'control.exe')
        self.appCaption = 'XRumer 7.09 Elite, Copyright BotmasterRu.Com, Support ICQ 876975, Administration e-mail botmaster@bk.ru'
        self.appCaptionControl = 'Control of permanent running'
        self.doneScript = 'C:\\Work\\doorscenter\\doorsagents\\xrumer-done.bat'
        
        '''Создание классов-хелперов'''
        if self.currentTask['type'] == 'XrumerBaseSpam':
            self.helper = XrumerHelperBaseSpam(self)
        elif self.currentTask['type'] == 'SpamTask':
            self.helper = XrumerHelperSpamTask(self)
        elif self.currentTask['type'] == 'XrumerBaseDoors':
            self.helper = XrumerHelperBaseDoors(self)
        elif self.currentTask['type'] == 'XrumerBaseProfiles':
            self.helper = XrumerHelperBaseProfiles(self)
        
        '''Базы'''
        self.appLinksFolder = os.path.join(self.appFolder, 'Links')
        self.baseMainFile = os.path.join(self.appLinksFolder, 'LinksList id%d.txt' % self.currentTask['baseNumberMain'])
        self.baseMainRFile = os.path.join(self.appLinksFolder, 'RLinksList id%d.txt' % self.currentTask['baseNumberMain'])
        self.baseMainZFile = os.path.join(self.appLinksFolder, 'ZLinksList id%d.txt' % self.currentTask['baseNumberMain'])
        self.baseSourceFile = os.path.join(self.appLinksFolder, 'LinksList id%d.txt' % self.currentTask['baseNumberSource'])
        self.baseSourceRFile = os.path.join(self.appLinksFolder, 'RLinksList id%d.txt' % self.currentTask['baseNumberSource'])
        self.baseSourceZFile = os.path.join(self.appLinksFolder, 'ZLinksList id%d.txt' % self.currentTask['baseNumberSource'])
        
        '''Логи'''
        self.projectName = self.helper.GetProjectName()
        self.logFileTemplate = os.path.join(self.appFolder, 'Logs', self.projectName, '%s id%d.txt' % ('%s', self.currentTask['baseNumberMain']))
        self.logSuccess = self.logFileTemplate % 'Success'
        self.logHalfSuccess = self.logFileTemplate % 'Halfsuccess'
        self.logFails = self.logFileTemplate % 'Others'
        self.logProfiles = self.logFileTemplate % 'Profiles'
        self.logRegisteredAccounts = os.path.join(self.appFolder, 'Logs', self.projectName, 'Registered Accounts.txt')
        self.logAnchors = self.logFileTemplate % 'Anchors'
        self.logLastURL = self.logFileTemplate % 'LastURL'
        
    def _CloseApp(self, appCaption):
        '''Закрытие приложения под Windows по заголовку окна'''
        p = win32gui.FindWindow(None, appCaption)
        win32gui.SendMessage(p, 0x10, 0, 0)
        time.sleep(1)
    
    def _CountLinks(self, paramName, logFile, description):
        '''Считаем ссылки'''
        self.currentTask[paramName] = 0
        try:
            self.currentTask[paramName] = kwk8.Kwk8Links(logFile).Count()
        except Exception as error:
            print('Cannot count %s links: %s' % (description, error))
    
    def _ActionOn(self):
        self._Settings()
        '''Удаляем старые логи'''
        self._DeleteLog(self.logSuccess)
        self._DeleteLog(self.logHalfSuccess)
        self._DeleteLog(self.logFails)
        '''Вызываем хэлпер'''
        self.helper.ActionOn()
        '''Удаляем старый RegisteredAccounts.txt'''
        if os.path.isfile(self.logRegisteredAccounts): 
            try:
                os.remove(self.logRegisteredAccounts)
            except Exception as error:
                print('Cannot remove log: %s' % error)
        '''Запуск приложений'''
        self._RunApp(self.appApplication)
        self._RunApp(self.appApplicationControl1)
        self._RunApp(self.appApplicationControl2)
        return True

    def _ActionOff(self):
        self._Settings()
        '''Закрытие приложений'''
        self._CloseApp(self.appCaptionControl)
        self._CloseApp(self.appCaptionControl)
        self._CloseApp(self.appCaption)
        '''Вызываем хэлпер'''
        self.helper.ActionOff()
        '''Выходные параметры'''
        self.currentTask['spamLinksList'] = []
        self._CountLinks('successCount', self.logSuccess, 'success')
        self._CountLinks('halfSuccessCount', self.logHalfSuccess, 'halfsuccess')
        self._CountLinks('failsCount', self.logFails, 'fails')
        self._CountLinks('profilesCount', self.logProfiles, 'profiles')
        self._CountLinks('registeredAccountsCount', self.logRegisteredAccounts, 'registered accounts')
        return True

if __name__ == '__main__':
    agent = XrumerAgent('http://searchpro.name/doorscenter/doorsadmin', 3)
