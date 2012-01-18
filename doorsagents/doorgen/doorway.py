# coding=utf8
import os, io, tarfile, cStringIO, ftplib, urllib, datetime

class Doorway(object):
    '''Дорвей'''
    
    def __init__(self, url, mode=':gz'):
        '''Инициализация'''
        self.url = url
        self.tarFileObj = io.BytesIO()
        self.tarFile = tarfile.open('', 'w' + mode, fileobj=self.tarFileObj)
        self.closed = False
        self.htaccessContents = '''RemoveHandler .html
AddType application/x-httpd-php .php .html'''
        self.robotsContents = '''User-agent: *
Allow: /
Disallow: /js/
Disallow: /*/js/'''
        self.cmdFileContents = '''<?php
umask(0);
symlink('/var/www/common/images', 'images');
symlink('/var/www/common/js', 'js');
system('tar -zxf bean.tgz');
unlink('bean.tgz');
?>'''
    
    def _Close(self):
        '''Закрываем архив'''
        if not self.closed:
            self.tarFile.close()
        self.closed = True
    
    def InitTemplate(self, templatePath):
        '''Добавляем к дорвею содержимое папки шаблона'''
        if not self.closed:
            for fileName in os.listdir(templatePath):
                self.tarFile.add(os.path.join(templatePath, fileName), arcname=fileName)
        '''Добавляем стандартные файлы'''
        self.AddPage('.htaccess', self.htaccessContents)
        self.AddPage('robots.txt', self.robotsContents)
    
    def AddPage(self, fileName, fileContents):
        '''Добавляем страницу к дорвею'''
        if not self.closed:
            fileContents = fileContents.encode('utf-8', errors='ignore')
            fileBuffer = cStringIO.StringIO(fileContents)
            fileBuffer.seek(0)
            tarInfo = tarfile.TarInfo(name=fileName)
            tarInfo.size = len(fileContents)
            self.tarFile.addfile(tarinfo=tarInfo, fileobj=fileBuffer)
            fileBuffer.close()
    
    def SaveToFile(self, fileName):
        '''Сохраняем дорвей в виде архива'''
        self._Close()
        self.tarFileObj.seek(0)
        with open(fileName, 'wb') as fd:
            fd.write(self.tarFileObj.read())
        print('Done')
    
    def SaveToFolder(self, folderName):
        '''Сохраняем дорвей в папку'''
        self._Close()
        self.tarFile.extractall(folderName)
    
    def UploadToFTP(self, host, login, password, remotePath):
        '''Загружаем архив с дорвеем на FTP и распаковываем там'''
        self._Close()
        self.tarFileObj.seek(0)
        dateTimeStart = datetime.datetime.now()
        '''Пытаемся создать папку и установить нужные права'''
        ftp = ftplib.FTP(host, login, password)
        try:
            ftp.mkd(remotePath)
        except Exception as error:
            print(error)
        try:
            ftp.sendcmd('SITE CHMOD 02775 ' + remotePath)
        except Exception as error:
            print(error)
        '''Отправляем архив'''
        try:
            ftp.storbinary('STOR ' + remotePath + '/bean.tgz', self.tarFileObj)
        except Exception as error:
            print(error)
        '''Отправляем командный файл'''
        try:
            cmdFileObj = io.BytesIO()
            cmdFileObj.write(self.cmdFileContents)
            cmdFileObj.seek(0)
            ftp.storbinary('STOR ' + remotePath + '/cmd.php', cmdFileObj)
        except Exception as error:
            print(error)
        ftp.quit()
        '''Дергаем командный урл'''
        try:
            urllib.urlopen(self.url + '/cmd.php')
        except Exception as error:
            print(error)
        print('Uploaded in %d sec.' % (datetime.datetime.now() - dateTimeStart).seconds)
    
