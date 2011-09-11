# coding=utf8
import os, shutil, urllib, ftplib, io, tarfile, datetime, agent, common, tplgen

class DoorgenAgent(agent.BaseAgent):
    ''' Параметры (см. методы GetTaskDetails и SetTaskDetails):
    Входные: keywordsList, templateFolder, domain, domainFolder, 
    netLinksList, analyticsId, piwikId, cyclikId, documentRoot, ftpLogin, ftpPassword, ftpPort.
    Выходные: spamLinksList.
    
    Параметр domainFolder всегда должен начинаться на прямой слэш.
    
    Минимальное содержимое командного файла cmd.php (для загрузки по FTP в архиве):
    <?php system('tar -zxf bean.tgz'); unlink('bean.tgz'); ?>     
'''
    
    def _Settings(self, generateTemplate = False):
        '''Настройки'''
        self.appFolder = r'C:\Program Files\Apache Software Foundation\Apache2.2\htdocs\doorgen'  # папка с приложением
        self.appEngine = 'http://test.home/doorgen/engine.php'  # запуск доргена
        self.appJobFile = os.path.join(self.appFolder, 'jobs' + os.sep + 'jobs.txt')  # задания
        self.appMacrosFile = os.path.join(self.appFolder, 'lib' + os.sep + 'custom_macros.php')  # значения кастомных макросов
        self.appTemplatesFolder = os.path.join(self.appFolder, 'templ')  # папка с шаблонами 
        self.appKeywordsFile = os.path.join(self.appFolder, 'keys' + os.sep + 'keywords.txt')  # файл с кеями 
        self.appNetLinksFile = os.path.join(self.appFolder, 'text' + os.sep + 'netlinks.txt')  # файл со ссылками для перелинковки 
        self.appSpamLinksFile = os.path.join(self.appFolder, 'out' + os.sep + 'jobs_ancor_log.txt')  # файл со сгенерированными ссылками для спама 
        self.doorwayUrl = 'http://' + self.currentTask['domain'] + self.currentTask['domainFolder']
        if self.doorwayUrl.endswith('/'):
            self.doorwayUrl = self.doorwayUrl[0:-1]
        self.doorwayFolder = self.appFolder + os.sep + 'out' + os.sep + 'jobs' + os.sep + 'door%d' % self._GetCurrentTaskId()
        self.currentTask['spamLinksList'] = []
        '''Генерация шаблона'''
        if generateTemplate:
            if self.currentTask['templateFolder'].startswith('xgen'):
                tplgen.TemplateGenerator1(self.currentTask['templateFolder'], os.path.join(self.appTemplatesFolder, 'xgen'))
                self.currentTask['templateFolder'] = 'xgen'
        
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
    
    def _CheckStatusCode(self):
        '''Проверить код статуса HTTP у залитого дора'''
        statusCode = urllib.urlopen(self.doorwayUrl).getcode()
        if statusCode != 200:
            raise Exception('Status code = %d' % statusCode)
        
    def _ActionOn(self):
        self._Settings(True)
        '''Кейворды и ссылки сетки'''
        with open(self.appKeywordsFile, 'w') as fd:
            fd.write('\n'.join(self.currentTask['keywordsList']))
        with open(self.appNetLinksFile, 'w') as fd:
            fd.write('\n'.join(self.currentTask['netLinksList']))
        '''Задание'''
        with open(self.appJobFile, 'w') as fd:
            fd.write('1, keywords.txt, %d, 0, %s, %s, door%d' % (len(self.currentTask['keywordsList']), self.currentTask['templateFolder'], self.doorwayUrl, self._GetCurrentTaskId()))
        '''Запись analyticsId и piwikId - ПОЗИЦИОННЫЕ ПАРАМЕТРЫ '''
        with open(self.appMacrosFile, 'r') as fd:
            lines = fd.readlines()
        if self.currentTask['analyticsId']:
            lines[1] = '\t\'{ANALYTICSID}\' => \'%s\',\n' % self.currentTask['analyticsId']
        if self.currentTask['piwikId']:
            lines[3] = '\t\'{PIWIKID}\' => \'%d\',\n' % self.currentTask['piwikId']
        with open(self.appMacrosFile, 'w') as fd:
            fd.writelines(lines)
        '''Запуск приложения'''
        try:
            statusCode = urllib.urlopen(self.appEngine)
        except Exception as error:
            print(error)
        self._Done()
        self._Cron()
        return True
    
    def _ActionOff(self):
        #self._Settings()  # в текущей версии доргена это не нужно
        '''Значения по умолчанию'''
        self.currentTask['keywordsList'] = []
        self.currentTask['netLinksList'] = []
        self.currentTask['spamLinksList'] = []
        '''Выходные параметры'''
        for line in open(self.appSpamLinksFile, 'r'):
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
        '''Удаляем файл со ссылками'''
        try:
            os.unlink(self.appSpamLinksFile)
        except Exception as error:
            print('Error: %s' % error)
        '''Проверяем код статуса (исключние не перехватывается)'''
        self._CheckStatusCode()
        return True

if __name__ == '__main__':
    agent = DoorgenAgent('http://searchpro.name/doorscenter/doorsadmin', 4)
