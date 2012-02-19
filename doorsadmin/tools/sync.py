# coding=utf8
import os, glob, shutil, sys

class FolderSync(object):
    '''Синхронизация папок'''
    
    def __init__(self, folderA, folderB, fileMask):
        '''Инициализация'''
        self.folderA = folderA
        self.folderB = folderB
        self.fileMask = fileMask
        self.processedFilesList = []
    
    def _CopyFile(self, fileNameSrc, fileNameDst):
        '''Копируем файл и подавляем исключения'''
        try:
            print('- copying "%s" -> "%s"...' % (fileNameSrc, fileNameDst))
            shutil.copyfile(fileNameSrc, fileNameDst)
            shutil.copystat(fileNameSrc, fileNameDst)
        except Exception as error:
            print('Error: %s' % error)
        
    def _SyncOneWay(self, folder1, folder2):
        '''Односторонняя синхронизация папок'''
        '''Цикл по первой папке'''
        for fileName1 in glob.glob(os.path.join(folder1, self.fileMask)):
            '''Получаем имя файла из второй папки'''
            baseFileName = os.path.basename(fileName1)
            fileName2 = os.path.join(folder2, baseFileName)
            '''Не обрабатываем каталоги и повторные файлы'''
            if os.path.isdir(fileName1) or os.path.isdir(fileName2):
                continue
            if baseFileName in self.processedFilesList:
                continue
            '''Копируем по необходимости'''
            if not os.path.exists(fileName2):
                self._CopyFile(fileName1, fileName2)  # копируем файл, отсутствующий во второй папке
                self.processedFilesList.append(baseFileName)
            elif (os.stat(fileName1).st_mtime - os.stat(fileName2).st_mtime) > 1:
                self._CopyFile(fileName1, fileName2)  # копируем более новый файл во вторую папку
                self.processedFilesList.append(baseFileName)
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
    sync = FolderSync(sys.argv[1], sys.argv[2], sys.argv[3])
    sync.Sync()
