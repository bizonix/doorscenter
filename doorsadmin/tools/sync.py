# coding=utf8
import os, glob, shutil

class FolderSync(object):
    '''Синхронизация папок'''
    
    def __init__(self, folderA, folderB):
        '''Инициализация'''
        self.folderA = folderA
        self.folderB = folderB
        self.processedFilesList = []
    
    def _CopyFile(self, fileNameSrc, fileNameDst, baseFileName):
        '''Копируем файл и подавляем исключения'''
        try:
            print('- copying "%s" -> "%s"...' % (fileNameSrc, fileNameDst))
            shutil.copyfile(fileNameSrc, fileNameDst)
            shutil.copystat(fileNameSrc, fileNameDst)
            self.processedFilesList.append(baseFileName)
        except Exception as error:
            print('Error: %s' % error)
        
    def _SyncOneWay(self, folder1, folder2):
        '''Односторонняя синхронизация папок'''
        '''Цикл по первой папке'''
        for fileName1 in glob.glob(os.path.join(folder1, '*.*')):
            baseFileName = os.path.basename(fileName1)
            '''Повторно файлы не обрабатываем'''
            if baseFileName in self.processedFilesList:
                continue
            '''Получаем имя второго файла'''
            fileName2 = os.path.join(folder2, baseFileName)
            '''Копируем по необходимости'''
            if not os.path.exists(fileName2):
                self._CopyFile(fileName1, fileName2, baseFileName)  # копируем файл, отсутствующий во второй папке
            elif (os.stat(fileName1).st_mtime - os.stat(fileName2).st_mtime) > 1:
                self._CopyFile(fileName1, fileName2, baseFileName)  # копируем более новый файл во вторую папку
            else:
                print('- skipped "%s".' % fileName1)
            
    def Sync(self):
        '''Двусторонняя синхронизация папок'''
        print('Sync started.')
        self.processedFilesList = []
        self._SyncOneWay(self.folderA, self.folderB)
        self._SyncOneWay(self.folderB, self.folderA)
        print('Sync finished.')

if __name__ == '__main__':
    sync = FolderSync(r'c:\Work\temp\1', r'c:\Work\temp\2')
    sync.Sync()
