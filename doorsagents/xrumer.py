# coding=utf8
import os, datetime, codecs, kwk8, agent, common#, win32gui

class XrumerAgent(agent.BaseAgent):
    ''' Параметры (см. методы GetTaskDetails и SetTaskDetails):
    Входные: baseNumber, nickName, realName, password, emailAddress, emailPassword, 
    emailLogin, emailPopServer, subject, snippetsFile, spamLinksList.
    Выходные: successCount, halfSuccessCount, failsCount, profilesCount.
    
    Два режима работы: 1 - создание базы R из сырой базы, 2 - спам по базе R.'''
    
    def _Settings(self):
        '''Настройки'''
        # self.appFolder = 'c:\\work\\xrumer7beta5'  # папка с приложением
        self.appFolder = '/home/sasch/workspace/doorscenter/src/doorscenter/test/xrumer'  # папка с приложением
        self.appCaption = 'XRumer 7.0 beta-5, Copyright BotmasterRu.Com, Support ICQ 876975, Admistration e-mail botmaster@bk.ru'
        self.appSettingsFile = os.path.join(self.appFolder, 'xuser.ini')
        self.appScheduleFile = os.path.join(self.appFolder, 'schedule.xml')
        self.doneScript = 'C:\\Work\\doorscenter\\doorsagents\\xrumer-done.bat'
        # self.snippetsFolder = 'C:\\Work\\snippets'
        self.snippetsFolder = '/home/sasch/workspace/doorscenter/src/doorscenter/test/snippets'
        self.snippetsFile = os.path.join(self.snippetsFolder, self.currentTask['snippetsFile'])
        self.projectName = 'Project%d' % self.currentTask['id']
        self.projectFile = os.path.join(self.appFolder, 'Projects', self.projectName + '.xml')
        self.logFileTemplate = os.path.join(self.appFolder, 'Logs', self.projectName, '%s id%d.txt' % ('%s', self.currentTask['baseNumber']))
        self.logSuccess = self.logFileTemplate % 'Success'
        self.logHalfSuccess = self.logFileTemplate % 'Halfsuccess'
        self.logFails = self.logFileTemplate % 'Others'
        self.logProfiles = self.logFileTemplate % 'Profiles'
        
        '''Содержимое файлов настроек'''
        self.appSettingsDictMode1 = {'OnlyRegistering': '0',    # не реализовано
            'RegisteringPlusPosting': '0', 
            'FromRegistered': '1', 
            'AggressiveMode': '0', 
            'CheckForActiveLink': '0', 
            'EditProfileAfterLogin': '1', 
            'UploadAvatars': '0', 
            'EnableRefspam': '0', 
            'BBtoHTML': '1', 
            'PostNewMode': '3',
            'SchedulerEnabled': '1'}
        self.appSettingsDictMode2 = {'OnlyRegistering': '0', 
            'RegisteringPlusPosting': '0', 
            'FromRegistered': '1', 
            'AggressiveMode': '0', 
            'CheckForActiveLink': '0', 
            'EditProfileAfterLogin': '1', 
            'UploadAvatars': '0', 
            'EnableRefspam': '0', 
            'BBtoHTML': '1', 
            'PostNewMode': '3',
            'SchedulerEnabled': '1'}
        
        '''Файл проекта'''
        self.projectFileContents = '''<?xml version="1.0" encoding="UTF-8"?>
<XRumerProject>
  <PrimarySection>
    <ProjectName>%s</ProjectName>
    <NickName>%s</NickName>
    <RealName>%s</RealName>
    <Password>%s</Password>
    <EmailAddress>%s</EmailAddress>
    <EmailPassword>%s</EmailPassword>
    <EmailLogin>%s</EmailLogin>
    <EmailPOP>%s</EmailPOP>
    <Homepage></Homepage>
    <ICQ></ICQ>
    <City>#file_links[C:\Work\lists\cities-en.txt]</City>
    <Country>#file_links[C:\Work\lists\countries-en.txt]</Country>
    <Occupation></Occupation>
    <Interests></Interests>
    <Signature></Signature>
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
    <Subject1>%s</Subject1>
    <Subject2></Subject2>
    <PostText>#file_links[%s,7,S] %s</PostText>
    <Prior></Prior>
    <OnlyPriors>false</OnlyPriors>
  </SecondarySection>
</XRumerProject>
''' % (self.projectName, self.currentTask['nickName'], self.currentTask['realName'], self.currentTask['password'], 
       self.currentTask['emailAddress'], self.currentTask['emailPassword'], self.currentTask['emailLogin'], 
       self.currentTask['emailPopServer'], self.currentTask['subject'], self.snippetsFile, codecs.decode(' '.join(self.currentTask['spamLinksList']), 'cp1251'))
        
        '''Файл расписания. Параметр в Schedule2: 0 - LinksList, 3 - RLinksList.'''
        self.appScheduleFileContents = '''<?xml version="1.0" encoding="UTF-8"?>
<body>
  <Schedule0>
    <PerformedTime></PerformedTime>
    <EventNum>2</EventNum>
    <EventParameter>%s</EventParameter>
    <JobNum>4</JobNum>
    <JobParameter>%s</JobParameter>
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
    <JobParameter>%s</JobParameter>
  </Schedule2>
  <Schedule3>
    <PerformedTime></PerformedTime>
    <EventNum>6</EventNum>
    <EventParameter></EventParameter>
    <JobNum>10</JobNum>
    <JobParameter>%s</JobParameter>
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
    <JobParameter>%s</JobParameter>
  </Schedule6>
</body>
''' % ((datetime.datetime.now() + datetime.timedelta(0, 120)).strftime('%d.%m.%y %H:%M:00'), 
       self.projectName, '%d', self.currentTask['baseNumber'], self.doneScript)
        
    def _CloseApp(self, appCaption):
        '''Закрытие приложения под Windows по заголовку окна'''
        '''p = win32gui.FindWindow(None, appCaption)
        win32gui.SendMessage(p, 0x10, 0, 0)'''
        
    def _ActionOn(self):
        self._Settings()
        '''Установка настроек'''
        with open(self.appScheduleFile, 'w') as fd:
            if self.currentTask['type'] == 'XrumerBaseR':
                fd.write(self.appScheduleFileContents % 0)
                common.ModifyIniFile(self.appSettingsFile, self.appSettingsDictMode1)
            if self.currentTask['type'] == 'SpamTask':
                fd.write(self.appScheduleFileContents % 3)
                common.ModifyIniFile(self.appSettingsFile, self.appSettingsDictMode2)
        with codecs.open(self.projectFile, 'w', 'utf8') as fd:
            fd.write(self.projectFileContents)
        '''Запуск приложения'''
        self._RunApp(os.path.join(self.appFolder, 'xpymep.exe'))
        return True

    def _ActionOff(self):
        self._Settings()
        '''Закрытие приложения'''
        self._CloseApp(self.appCaption)
        '''Выходные параметры'''
        self.currentTask['spamLinksList'] = []
        try:
            self.currentTask['successCount'] = kwk8.Kwk8Links(self.logSuccess, False).Count()
        except Exception:
            self.currentTask['successCount'] = 0
        try:
            self.currentTask['halfSuccessCount'] = kwk8.Kwk8Links(self.logHalfSuccess, False).Count()
        except Exception:
            self.currentTask['halfSuccessCount'] = 0 
        try:
            self.currentTask['failsCount'] = kwk8.Kwk8Links(self.logFails, False).Count()
        except Exception:
            self.currentTask['failsCount'] = 0 
        try:
            self.currentTask['profilesCount'] = kwk8.Kwk8Links(self.logProfiles, False).Count()
        except Exception:
            self.currentTask['profilesCount'] = 0
        return True

if __name__ == '__main__':
    # agent = XrumerAgent('http://searchpro.name/doorscenter/doorsadmin', 3)
    agent = XrumerAgent('http://127.0.0.1:8000/doorsadmin', 3)
