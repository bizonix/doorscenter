# coding=utf8
import os, shutil, urllib, ftplib, io, tarfile, datetime, agent, common, tplgen

class DoorgenAgent(agent.BaseAgent):
    ''' Параметры (см. методы GetTaskDetails и SetTaskDetails):
    Входные: keywordsList, templateFolder, domain, domainFolder, 
    netLinksList, analyticsId, piwikId, cyclikId, documentRoot, ftpLogin, ftpPassword, ftpPort.
    Выходные: spamLinksList.
    
    В настройках доргена принудительно устанавливаем параметры, см. ниже. Кейворды 
    пишем в файл так:
    keyword1|[domain]|[ftpLogin]|[ftpPassword]|[documentRoot](os.path.join)[domainFolder]|
    
    Параметр domainFolder всегда должен начинаться на прямой слэш.
    
    Минимальное содержимое командного файла cmd.php (для загрузки по FTP в архиве):
    <?php system('tar -zxf bean.tgz'); unlink('bean.tgz'); ?>     
'''
    
    def _Settings(self, generateTemplate = False):
        '''Настройки'''
        self.appFolder = 'D:\\Miscellaneous\\Lodger6\\aggress'  # папка с приложением
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
        self.doneScript = 'D:\\Miscellaneous\\Lodger6\\workspace\\doorscenter\\src\\doorscenter\\doorsagents\\doorgen-done.bat'
        self.doorwayUrl = 'http://' + self.currentTask['domain'] + self.currentTask['domainFolder']
        self.doorwayFolder = self.appFolder + os.sep + self.appDoorwayFolder + 'door%d' % self._GetCurrentTaskId()
        if not self.doorwayUrl.endswith('/'):
            self.doorwayUrl += '/'
        '''Генерация шаблона'''
        if generateTemplate:
            if self.currentTask['templateFolder'].startswith('xgen'):
                tplgen.TemplateGenerator1(self.currentTask['templateFolder'], os.path.join(self.appTemplatesFolder, 'xgen'))
                self.currentTask['templateFolder'] = 'xgen'
        '''Содержимое файлов настроек'''
        self.appSettingsDict = {'OverturBeforeGen': '0',
            'MyLinkHTML': '1',  # HTML-1, URL-0
            'TypePattern': self.currentTask['templateFolder'],
            'RandomPattern': '0',
            'Redirect': '0',
            'PathSaveDoorway': self.appDoorwayFolder,
            'RUEN': '0',  # RU-1, EN-0
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
        
    def _CreateXmlSitemap(self):
        '''Генерация карты XML'''
        with open(os.path.join(self.doorwayFolder, 'sitemap.xml'), 'w') as fd:
            fd.write('''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
''')
            for link in open(self.appSpamLinks3File, 'r'):
                fd.write('''   <url>
      <loc>%s</loc>
      <lastmod>%s</lastmod>
      <changefreq>weekly</changefreq>
      <priority>0.5</priority>
   </url>
''' % (link.strip(), datetime.date.today().strftime('%Y-%m-%d')))
            fd.write('''</urlset>
''')
        
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
        if self.currentTask['domainFolder'] != '/':
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
    
    def _CheckStatusCode(self):
        '''Проверить код статуса HTTP у залитого дора'''
        statusCode = urllib.urlopen(self.doorwayUrl).getcode()
        if statusCode != 200:
            raise Exception('Status code = %d' % statusCode)
        
    def _ActionOn(self):
        self._Settings(True)
        '''Установка настроек'''
        with open(self.appSettingsFile) as fd:
            settings = fd.readlines()
        with open(self.appSettingsFile, 'w') as fd:
            fd.write('\n'.join(common.ModifyIniSettings(settings, self.appSettingsDict)))
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
        '''Запись piwikId - ПОЗИЦИОННЫЙ ПАРАМЕТР '''
        with open(self.appMacrosFile, 'r') as fd:
            lines = fd.readlines()
        if self.currentTask['piwikId']:
            lines[2] = '%d\n' % self.currentTask['piwikId']
        with open(self.appMacrosFile, 'w') as fd:
            fd.writelines(lines)
        '''Запуск приложения'''
        self._RunApp(os.path.join(self.appFolder, 'aggressdoorgen.exe'))
        return True
    
    def _ActionOff(self):
        self._Settings()
        '''Значения по умолчанию'''
        self.currentTask['keywordsList'] = []
        self.currentTask['keywordsListAdd'] = []
        self.currentTask['netLinksList'] = []
        self.currentTask['spamLinksList'] = []
        '''Выходные параметры'''
        for line in open(self.appSpamLinks1File, 'r'):
            self.currentTask['spamLinksList'].append(line.strip())
        '''Создаем сайтмап'''
        try:
            self._CreateXmlSitemap()
        except Exception as error:
            print('Error: %s' % error)
        '''Загружаем на FTP'''
        try:
            self._Upload()
        except Exception as error:
            print('Error: %s' % error)
        '''Удаляем локальную папку'''
        try:
            #shutil.rmtree(self.doorwayFolder)
            pass
        except Exception as error:
            print('Error: %s' % error)
        '''Проверяем код статуса (исключение не перехватывается)'''
        self._CheckStatusCode()
        return True

if __name__ == '__main__':
    agent = DoorgenAgent('http://searchpro.name/doorscenter/doorsadmin', 1)
