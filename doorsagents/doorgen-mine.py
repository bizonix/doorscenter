# coding=utf8
import os, shutil, urllib, ftplib, io, tarfile, datetime, agent, common, tplgen
import doorgen.doorgen

class DoorgenAgent(agent.BaseAgent):
    ''' Параметры (см. методы GetTaskDetails и SetTaskDetails):
    Входные: keywordsList, keywordsListAdd, templateFolder, domain, domainSub, domainFolder, 
    netLinksList, tdsId, documentRoot, ftpLogin, ftpPassword, ftpPort.
    Выходные: doorLinksList.
    
    Параметр domainFolder всегда должен начинаться на прямой слэш.
    
    Минимальное содержимое командного файла cmd.php (для загрузки по FTP в архиве):
    <?php system('tar -zxf bean.tgz'); unlink('bean.tgz'); ?>     
'''
    
    def _Settings(self, generateTemplate = False):
        '''Настройки'''
        self.appFolder = r'C:\Program Files\Apache Software Foundation\Apache2.2\htdocs\doorgen'  # папка с приложением
        self.appTemplatesFolder = os.path.join(self.appFolder, 'templ')  # папка с шаблонами 
        self.appTextFolder = os.path.join(self.appFolder, 'text')  # папка с текстовыми файлами
        self.appSnippetsFolder = r'C:\Work\snippets'  # папка со сниппетами
        if self.currentTask['domainSub'] == '':
            self.doorwayUrl = 'http://%s%s' % (self.currentTask['domain'], self.currentTask['domainFolder'])
        else:
            self.doorwayUrl = 'http://%s.%s%s' % (self.currentTask['domainSub'], self.currentTask['domain'], self.currentTask['domainFolder'])
        if self.doorwayUrl.endswith('/'):
            self.doorwayUrl = self.doorwayUrl[0:-1]
        if self.currentTask['domainSub'] == '':
            self.remoteFolder = '%s%s' % (self.currentTask['documentRoot'], self.currentTask['domainFolder'])
        else:
            self.remoteFolder = '%s/sub-%s%s' % (self.currentTask['documentRoot'], self.currentTask['domainSub'], self.currentTask['domainFolder'])
        self.currentTask['doorLinksList'] = []
        '''Генерация шаблона'''
        if generateTemplate:
            if self.currentTask['templateFolder'].startswith('xgen'):
                tplgen.TemplateGenerator1(self.currentTask['templateFolder'], os.path.join(self.appTemplatesFolder, 'xgen'))
                self.currentTask['templateFolder'] = 'xgen'
        
    def _CheckStatusCode(self):
        '''Проверить код статуса HTTP у залитого дора'''
        statusCode = urllib.urlopen(self.doorwayUrl).getcode()
        if statusCode != 200:
            raise Exception('Status code = %d' % statusCode)
        
    def _ActionOn(self):
        self._Settings(True)
        '''Запуск приложения'''
        doorgen = doorgen.doorgen.Doorgen(self.appTemplatesFolder, self.appTextFolder, self.appSnippetsFolder)
        doorway = doorgen.Generate(self.currentTask['keywordsList'].extend(self.currentTask['keywordsListAdd']), 
            self.currentTask['netLinksList'], self.currentTask['templateFolder'], 
            len(self.currentTask['keywordsList']), self.doorwayUrl)
        doorway.UploadToFTP(self.currentTask['domain'], self.currentTask['ftpLogin'], self.currentTask['ftpPassword'], 
            self.remoteFolder)
        self._Done()
        self._Cron()
        return True
    
    def _ActionOff(self):
        #self._Settings()  # в текущей версии доргена это не нужно
        '''Значения по умолчанию'''
        self.currentTask['keywordsList'] = []
        self.currentTask['keywordsListAdd'] = []
        self.currentTask['netLinksList'] = []
        self.currentTask['doorLinksList'] = []
        '''Выходные параметры'''
        self.currentTask['doorLinksList'] = doorgen.pageLinksList[:]
        '''Проверяем код статуса (исключение не перехватывается)'''
        self._CheckStatusCode()
        return True

if __name__ == '__main__':
    agent = DoorgenAgent('http://searchpro.name/doorscenter/doorsadmin', 4)
