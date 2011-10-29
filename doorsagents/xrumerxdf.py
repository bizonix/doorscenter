# coding=utf8

import os, shutil

class XrumerTopicLinker(object):
    '''Менеджер перелинковки топиков и профилей'''

    def __init__(self, helper):
        self.helper = helper
        self.agent = self.helper.agent
        self.allFileName = 'total.txt'
        self.anchorsSpamFolder = os.path.join(self.agent.appFolder, 'AnchorsSpam')
        self.anchorsSpamFile = os.path.join(self.anchorsSpamFolder, self.allFileName)
        if not os.path.exists(self.anchorsSpamFile):
            open(self.anchorsSpamFile, 'w').write('')
        self.anchorsDoorsFolder = os.path.join(self.agent.appFolder, 'AnchorsDoors')
        self.anchorsDoorsFile = os.path.join(self.anchorsDoorsFolder, self.allFileName)
        if not os.path.exists(self.anchorsDoorsFile):
            open(self.anchorsDoorsFile, 'w').write('')
        self.anchorsProfilesFolder = os.path.join(self.agent.appFolder, 'AnchorsProfiles')
        self.anchorsProfilesFile = os.path.join(self.anchorsProfilesFolder, self.allFileName)
        if not os.path.exists(self.anchorsProfilesFile):
            open(self.anchorsProfilesFile, 'w').write('')
    
    def GetSpamAnchorsFile(self):
        '''Отдаем файл с анкорами по топикам спама'''
        return self.anchorsSpamFile
    
    def GetDoorsAnchorsFile(self):
        '''Отдаем файл с анкорами по дорам на форумах'''
        return self.anchorsDoorsFile
    
    def GetProfilesFile(self):
        '''Отдаем файл с анкорами по топикам спама'''
        return self.anchorsProfilesFile
    
    def AddSpamAnchorsFile(self):
        '''Копируем новые анкоры в базу'''
        self._AddAnchorsFile(self.agent.logAnchors, self.anchorsSpamFolder)
    
    def AddDoorsAnchorsFile(self):
        '''Копируем новые анкоры в базу'''
        self._AddAnchorsFile(self.agent.logAnchors, self.anchorsDoorsFolder)
    
    def AddProfilesFile(self):
        '''Делаем из профилей анкоры'''
        profileAnchors = self.agent.logProfiles + 'p'
        urls = open(self.agent.logProfiles, 'r').readlines()
        keys = open(self.helper.keywordsFile, 'r').readlines()
        with open(profileAnchors, 'w') as fd:
            for n in range(len(urls)):
                fd.write('[url=%s]%s[/url]\n' % (urls[n].strip(), keys[n].strip()))
        '''Копируем новые профили в базу'''
        self._AddAnchorsFile(profileAnchors, self.anchorsProfilesFolder)
        '''Удаляем временный файл'''
        self.helper._DeleteBase(profileAnchors)

    def _AddAnchorsFile(self, fileName, anchorsFolder):
        '''Копируем файл в папку и объединяем имеющиеся файлы'''
        try:
            shutil.copy(fileName, anchorsFolder)
            with open(os.path.join(anchorsFolder, self.allFileName), 'w') as fd:
                for fileName in os.listdir(anchorsFolder):
                    if fileName != self.allFileName:
                        fd.write(open(os.path.join(anchorsFolder, fileName)).read())
        except Exception as error:
            print('Cannot update anchors: %s' % error)
