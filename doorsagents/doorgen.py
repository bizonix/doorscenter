# coding=utf8
import os, shutil, urllib, ftplib, io, tarfile, agent, common

class DoorgenAgent(agent.BaseAgent):
    ''' Параметры (см. методы GetTaskDetails и SetTaskDetails):
    Входные: keywordsList, templateFolder, doorgenSettings, domain, domainFolder, 
    netLinksList, analyticsId, piwikId, cyclikId, documentRoot, ftpLogin, ftpPassword, ftpPort.
    Выходные: spamLinksList.
    
    В настройках доргена принудительно устанавливаем параметры, см. ниже. Кейворды 
    пишем в файл так:
    keyword1|[domain]|[ftpLogin]|[ftpPassword]|[documentRoot](os.path.join)[domainFolder]|
    
    Параметр domainFolder всегда должен начинаться на прямой слэш.
    
    Минимальное содержимое командного файла cmd.php (для загрузки по FTP в архиве):
    <?php system('tar -zxf bean.tgz'); unlink('bean.tgz'); ?>     
'''
    
    def _Settings(self):
        '''Настройки'''
        self.appFolder = 'c:\\work\\aggress'  # папка с приложением
        self.appSettingsFile = os.path.join(self.appFolder, 'tunings' + os.sep + 'auto.ini')  # настройки 1
        self.appTuningsFile = os.path.join(self.appFolder, 'system' + os.sep + 'seting.ini')  # настройки 2
        self.appLinksPattern1File = os.path.join(self.appFolder, 'links' + os.sep + 'pattern1.txt')  # шаблон ссылок 1
        self.appLinksPattern2File = os.path.join(self.appFolder, 'links' + os.sep + 'pattern2.txt')  # шаблон ссылок 2
        self.appLinksPattern3File = os.path.join(self.appFolder, 'links' + os.sep + 'pattern3.txt')  # шаблон ссылок 3
        self.appMacrosFile = os.path.join(self.appFolder, 'system' + os.sep + 'macrosvalue.txt')  # значения кастомных макросов
        self.appDoorwayFolder = 'doorway\\'  # папка, куда генерится дорвей - относительный путь с конечным слэшем
        self.appTemplatesFolder = os.path.join(self.appFolder, 'pattern')  # папка с шаблонами 
        self.appKeywordsFile = os.path.join(self.appFolder, 'keys' + os.sep + 'keywords.txt')  # файл с кеями 
        self.appNetLinksFile = os.path.join(self.appFolder, 'links' + os.sep + 'netlinks.txt')  # файл со ссылками для перелинковки 
        self.appSpamLinks1File = os.path.join(self.appFolder, 'links' + os.sep + 'alinks.txt')  # файл со сгенерированными ссылками для спама 
        self.appSpamLinks2File = os.path.join(self.appFolder, 'links' + os.sep + 'blinks.txt')  # файл со сгенерированными ссылками для спама 
        self.appSpamLinks3File = os.path.join(self.appFolder, 'links' + os.sep + 'clinks.txt')  # файл со сгенерированными ссылками для спама 
        self.doneScript = 'C:\\Work\\doorscenter\\doorsagents\\doorgen-done.bat'
        self.doorwayUrl = 'http://www.' + self.currentTask['domain'] + self.currentTask['domainFolder']
        self.doorwayFolder = self.appFolder + os.sep + self.appDoorwayFolder + 'door%d' % self._GetCurrentTaskId()
        if not self.doorwayUrl.endswith('/'):
            self.doorwayUrl += '/'
        '''Содержимое файлов настроек'''
        self.appSettingsDict = {'OverturBeforeGen': '0',
            'MyLinkHTML': '1',  # HTML-1, URL-0
            'TypePattern': self.currentTask['templateFolder'],
            'RandomPattern': '0',
            'Redirect': '0',
            'PathSaveDoorway': self.appDoorwayFolder,
            'RUEN': '1',  # RU-1, EN-0
            'UrlDoorway': self.doorwayUrl,
            'SaveCountLinksForSpam': '0',
            'ClearFileLinksBeforeGenerate': '1',
            'LinksForSpam1': '1',
            'LinksForSpam2': '1',
            'LinksForSpam3': '1',
            'SaveLinksForSpam1': self.appSpamLinks1File,
            'SaveLinksForSpam2': self.appSpamLinks2File,
            'SaveLinksForSpam3': self.appSpamLinks3File,
            'TextURL1': '{ADDRESS}{BOSKEYWORD}.html',
            'TextURL2': 'http://{BOSKEYWORD}.{ADDRESS}/',
            'TextURL3': 'http://{ADDRESS}/{BOSKEYWORD}.html',
            'SiteMapLink': '1',
            'InsetBeforeURLLink': '0',
            'TypeLinks': '0',
            'NameSiteMapLink': 'sitemap',
            'InsetBrDoorLinks': '1',
            'TypeMyLinks': '0',
            'InsetBrMyLinks': '1',
            'AutoCountPage': '1',
            'CreatePatternBeforeGenerate': '0',
            'CreateLinksPastGenerate': '1',
            'DownloadPastGenerate': '0',
            'CreateNewFolder': '0',
            'FindFolderForFTP': '0',
            'DownloadFTPThreade': '0',
            'SaveFTPError': '0',
            'PathFileSaveFTPError': '',
            'MaxFTPAttempt': '3',
            'UseManyDoorway': '1',
            'DivideGroupKeywords': '',
            'NoDivideGroupKeywords': '0',
            'UseSelectKeywords': '0',
            'UseDoorwayLink': '0',
            'AutoDownloadKeywords': '1',
            'AutoDownloadKeywordsPath': self.appKeywordsFile,
            'AutoDownloadMyLinks': '1',
            'AutoDownloadMyLinksPath': self.appNetLinksFile,
            'BeginFileExecute': '1',
            'PathFileBeginFileExecute': self.doneScript,
            'DisableDoorgenPastGen': '1',
            'IncludeGenBegin': '1',
            'SendEmailEndGen': '0',
            'SendEmailStopGen': '0',
            'html': 'html',
            'ReplaceBlank': '-',
            'NameLinkIndex': '{CKEYWORD(1)}',
            'NameIndex': 'index',
            'IndexFromKeyword': '0',
            'NamePages': '{BOSKEYWORD}',
            'IgnorePartKeyword': '1',
            'IgnoreAfterLetter': '|',
            'DirPattern': self.appTemplatesFolder,
            'CreateFolderAllDoorway': '1',
            'PatternNameFolder': 'door%d' % self._GetCurrentTaskId(),
            'AddBeforeFolder': '0',
            'AddPastFolder': '0',
            'FolderArchives': '0',
            'DoorwayInArchives': '0',
            'DeleteFilePastGenerate': '0'}
        self.appTuningsDict = {'TuningsINI': 'auto.ini'}
        self.appLinksPattern1Contents = '''<a href="{URL}">{BOSKEYWORD}</a>
'''
        self.appLinksPattern2Contents = '''[URL="{URL}"]{BOSKEYWORD}[/URL]
'''
        self.appLinksPattern3Contents = '''{URL}
'''
        
    def _Upload(self):
        '''Константы'''
        archiveFile = 'bean.tgz'
        commandFile = 'cmd.php'
        '''Создаем архив в памяти'''
        fileObj = io.BytesIO()
        tar = tarfile.open('', 'w:gz', fileobj=fileObj)
        for filelocal in os.listdir(self.doorwayFolder):
            filelocal = os.path.join(self.doorwayFolder, filelocal)
            tar.add(filelocal, arcname=filelocal.replace(self.doorwayFolder, ''))
        tar.close()
        fileObj.seek(0)
        '''Загружаем на FTP'''
        remoteFolder = self.currentTask['documentRoot'] + self.currentTask['domainFolder']
        ftp = ftplib.FTP(self.currentTask['domain'], self.currentTask['ftpLogin'], self.currentTask['ftpPassword'])
        try:
            ftp.mkd(remoteFolder)
        except Exception as error:
            print(error)
        try:
            ftp.sendcmd('SITE CHMOD 02775 ' + remoteFolder)
        except Exception as error:
            print(error)
        try:
            ftp.storbinary('STOR ' + remoteFolder + '/' + archiveFile, fileObj)
        except Exception as error:
            print(error)
        try:
            with open(os.path.join(self.doorwayFolder, commandFile), 'r') as fd:
                ftp.storbinary('STOR ' + remoteFolder + '/' + commandFile, fd)
        except Exception as error:
            print(error)
        ftp.quit()
        '''Дергаем командный урл'''
        try:
            urllib.urlopen(self.doorwayUrl + '/' + commandFile)
        except Exception as error:
            print(error)
        
    def _ActionOn(self):
        self._Settings()
        '''Установка настроек'''
        with open(self.appSettingsFile, 'w') as fd:
            fd.write('\n'.join(common.ModifyIniSettings(self.currentTask['doorgenSettings'], self.appSettingsDict)))
        common.ModifyIniFile(self.appTuningsFile, self.appTuningsDict)
        with open(self.appLinksPattern1File, 'w') as fd:
            fd.write(self.appLinksPattern1Contents)
        with open(self.appLinksPattern2File, 'w') as fd:
            fd.write(self.appLinksPattern2Contents)
        with open(self.appLinksPattern3File, 'w') as fd:
            fd.write(self.appLinksPattern3Contents)
        '''Кейворды и ссылки сетки'''
        with open(self.appKeywordsFile, 'w') as fd:
            fd.write(self.currentTask['keywordsList'][0])
            fd.write('|%s|%s|%s|%s%s|\n' % (self.currentTask['domain'], self.currentTask['ftpLogin'], self.currentTask['ftpPassword'], self.currentTask['documentRoot'], self.currentTask['domainFolder']))
            fd.write('\n'.join(self.currentTask['keywordsList'][1:]))
        with open(self.appNetLinksFile, 'w') as fd:
            fd.write('\n'.join(self.currentTask['netLinksList']))
        '''Запись analyticsId и piwikId - ПОЗИЦИОННЫЕ ПАРАМЕТРЫ '''
        with open(self.appMacrosFile, 'r') as fd:
            lines = fd.readlines()
        if self.currentTask['analyticsId']:
            lines[2] = '%s\n' % self.currentTask['analyticsId']
        if self.currentTask['piwikId']:
            lines[4] = '%d\n' % self.currentTask['piwikId']
        with open(self.appMacrosFile, 'w') as fd:
            fd.writelines(lines)
        '''Запись cyclicId - ПОЗИЦИОННЫЕ ПАРАМЕТРЫ '''
        cyclikConfigFile = os.path.join(self.appTemplatesFolder, self.currentTask['templateFolder'], 'cyclik_config.php') 
        if os.path.isfile(cyclikConfigFile) and self.currentTask['cyclikId']:
            with open(cyclikConfigFile, 'r') as fd:
                lines = fd.readlines()
            lines[4] = ' $id = "%d"; // Client ID\n' % self.currentTask['cyclikId']
            with open(cyclikConfigFile, 'w') as fd:
                fd.writelines(lines)
        '''Запуск приложения'''
        self._RunApp(os.path.join(self.appFolder, 'aggressdoorgen.exe'))
        return True
    
    def _ActionOff(self):
        self._Settings()
        '''Выходные параметры'''
        self.currentTask['doorgenSettings'] = []
        self.currentTask['keywordsList'] = []
        self.currentTask['netLinksList'] = []
        self.currentTask['spamLinksList'] = []
        for line in open(self.appSpamLinks1File, 'r'):
            self.currentTask['spamLinksList'].append(line.strip())
        '''Загружаем на FTP'''
        try:
            self._Upload()
        except Exception as error:
            print('Error: %s' % error)
        '''Удаляем локальную папку'''
        try:
            shutil.rmtree(self.doorwayFolder)
        except Exception as error:
            print('Error: %s' % error)
        return True

if __name__ == '__main__':
    agent = DoorgenAgent('http://searchpro.name/doorscenter/doorsadmin', 1)

'''Описание жестко устанавливаемых параметров доргена:
    страница "Генерация":
        парсить перед генерацией - нет
        разместить на страницах ссылки - html
        шаблон - [папка]
        наугад - нет
        редирект - нет
        сохранить - doorway\
        язык - русский
    страница "Макросы":
        piwikid - ...
        cyclikid - ...
    страница "Ссылки для спама":
        адрес дорвея - ...
        вид ссылок - ...
        сохранять от - нет
        очищать если существует - да
        [три вида ссылок] - да, вид и адрес
    страница "Настройки" - "Ссылки":
        {LINKS}:
            сделать карту дорвея - да
            вставить до адреса ссылки - нет
            все ссылки - да
            название карты дорвея - карта сайта
            вставить <br> после ссылок - да
        {MYLINKS}:
            все ссылки - да (???)
            вставить <br> после ссылок - да
    страница "Настройки" - "Автоматика":
        автоматически выставлять количество страниц - да
        генерировать новый шаблон - нет
        автоматическое создание ссылок после генерации - да
        закачать по FTP после генерации - да
        ... (???)
        формат заданий для FTP - host, login, pass, dir
        множественное создание дорвеев использовать - да
        разделитель групп - пустое поле
        на кейворд по дору - нет
        подбор кейвордов - все нет
        перелинковка доров - нет
        загружать при включении кейворды - да, [файл]
        загружать при включении текст - нет
        загружать при включении редирект - нет
        загружать при включении ссылки - да, [файл]
        запускать файл после генерации - [адрес скрипта с флагом "done"]
        выключать дорген после генерации - да
        включать генерацию при включении - да
        отчеты на email - все пусто и нет
    страница "Настройки" - "Разное":
        расширения страниц - html
        замена пробела - -
        назвать ссылку на главную страницу - {CKEYWORD(1)}
        название главной страницы - index
        по кейворду - нет
        названия других страниц - {BOSKEYWORD}
        proxy - пусто, нет
        текст из файлов - нет
        игнорировать часть кейворда - да
        после символа - |
        папка с шаблонами - [папка]
        создавать папку для каждого дорвея - да
        назвать папку - [id задания]
'''
