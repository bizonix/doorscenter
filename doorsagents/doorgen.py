# coding=utf8
import os, sys, agent

class DoorgenAgent(agent.BaseAgent):
    ''' Параметры (см. методы GetTaskDetails и SetTaskDetails):
    Входные: settings, templateFolder, keywordsList, domain, domainFolder, 
    netLinksList, documentRoot, ftpLogin, ftpPassword, ftpPort.
    Выходные: spamLinksList.
    
    В настройках доргена принудительно устанавливаем параметры, см. ниже. Кейворды 
    пишем в файл так:
    keyword1|[domain]|[ftpLogin]|[ftpPassword]|[documentRoot](os.path.join)[domainFolder]|
'''
    
    def _Settings(self):
        '''Настройки'''
        # self.appFolder = 'c:/work/aggress'  # папка с приложением
        self.appFolder = '/home/sasch/workspace/doorscenter/src/doorscenter/test/doorgen'  # папка с приложением
        self.appSettingsFile = os.path.join(self.appFolder, 'tunings/auto.ini')  # настройки 1
        self.appTuningsFile = os.path.join(self.appFolder, 'system/seting.ini')  # настройки 2
        self.appLinksPattern1File = os.path.join(self.appFolder, 'links/pattern1.txt')  # шаблон ссылок 1
        self.appLinksPattern2File = os.path.join(self.appFolder, 'links/pattern2.txt')  # шаблон ссылок 2
        self.appLinksPattern3File = os.path.join(self.appFolder, 'links/pattern3.txt')  # шаблон ссылок 3
        self.appDoorwayFolder = os.path.join(self.appFolder, 'doorway/')  # папка, куда генерится дорвей - с конечным слэшем
        self.appTemplatesFolder = os.path.join(self.appFolder, 'pattern')  # папка с шаблонами 
        self.appKeywordsFile = os.path.join(self.appFolder, 'keys/keywords.txt')  # файл с кеями 
        self.appNetLinksFile = os.path.join(self.appFolder, 'links/netlinks.txt')  # файл со ссылками для перелинковки 
        self.appSpamLinks1File = os.path.join(self.appFolder, 'links/alinks.txt')  # файл со сгенерированными ссылками для спама 
        self.appSpamLinks2File = os.path.join(self.appFolder, 'links/blinks.txt')  # файл со сгенерированными ссылками для спама 
        self.appSpamLinks3File = os.path.join(self.appFolder, 'links/clinks.txt')  # файл со сгенерированными ссылками для спама 
        '''Содержимое файлов настроек'''
        self.appSettingsDict = {'OverturBeforeGen': '0',
            'MyLinkHTML': '0',  # HTML-1, URL-0
            'TypePattern': self.currentTask['templateFolder'],
            'RandomPattern': '0',
            'Redirect': '0',
            'PathSaveDoorway': self.appDoorwayFolder,
            'RUEN': '1',  # RU-1, EN-0
            'UrlDoorway': 'http://www.' + self.currentTask['domain'] + self.currentTask['domainFolder'],
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
            'DownloadPastGenerate': '1',
            'CreateNewFolder': '0',
            'FindFolderForFTP': '0',
            'DownloadFTPThreade': '1',
            'SaveFTPError': '0',
            'PathFileSaveFTPError': '',
            'MaxFTPAttempt': '3',
            'UseManyDoorway': '1',
            'DivideGroupKeywords': '',
            'NoDivideGroupKeywords': '0',
            'UseSelectKeywords': '0',
            'UseDoorwayLink': '0',
            'AutoDownloadKeywords': '0',
            'AutoDownloadKeywordsPath': self.appKeywordsFile,
            'AutoDownloadMyLinks': '0',
            'AutoDownloadMyLinksPath': self.appNetLinksFile,
            'BeginFileExecute': '0',
            'PathFileBeginFileExecute': sys.executable + ' ' + os.path.abspath(__file__) + ' done',
            'DisableDoorgenPastGen': '0',
            'IncludeGenBegin': '0',
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
        
        self.appTuningsFileContent = '''[General]
Account=forester
TuningsINI=auto.ini
Left=238
Top=80
'''
        self.appLinksPattern1Content = '''<a href="{URL}">{BOSKEYWORD}</a>
'''
        self.appLinksPattern2Content = '''[URL="{URL}"]{BOSKEYWORD}[/URL]
'''
        self.appLinksPattern3Content = '''{URL}
'''
        
    def _ActionOn(self):
        print('Starting task #%s' % self._GetCurrentTaskId())
        self._Settings()
        with open(self.appSettingsFile, 'w') as fd:
            for line in self.currentTask['settings']:
                if line.find('=') >= 0:
                    key, _, value = line.partition('=')
                    if key in self.appSettingsDict:
                        value = self.appSettingsDict[key]
                    line = key + '=' + value
                fd.write(line + '\n')
        with open(self.appTuningsFile, 'w') as fd: 
            fd.write(self.appTuningsFileContent)
        with open(self.appLinksPattern1File, 'w') as fd:
            fd.write(self.appLinksPattern1Content)
        with open(self.appLinksPattern2File, 'w') as fd:
            fd.write(self.appLinksPattern2Content)
        with open(self.appLinksPattern3File, 'w') as fd:
            fd.write(self.appLinksPattern3Content)
        with open(self.appKeywordsFile, 'w') as fd:
            fd.write(self.currentTask['keywordsList'][0])
            fd.write('|%s|%s|%s|%s%s|\n' % (self.currentTask['domain'], self.currentTask['ftpLogin'], self.currentTask['ftpPassword'], self.currentTask['documentRoot'], self.currentTask['domainFolder']))
            fd.write('\n'.join(self.currentTask['keywordsList'])[1:])
        with open(self.appNetLinksFile, 'w') as fd:
            fd.write('\n'.join(self.currentTask['netLinksList']))
        self._RunApp(os.path.join(self.appFolder, 'aggressdoorgen.exe'))
        return True
    
    def _ActionOff(self):
        print('Ending task #%s' % self._GetCurrentTaskId())
        self._Settings()
        self.currentTask['settings'] = ''
        self.currentTask['keywordsList'] = ''
        self.currentTask['netLinksList'] = ''
        self.currentTask['spamLinksList'] = []
        for line in open(self.appSpamLinks1File, 'r'):
            self.currentTask['spamLinksList'].append(line.strip())
        return True

if __name__ == '__main__':
    agent = DoorgenAgent('http://127.0.0.1:8000/doorsadmin', 1)

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
