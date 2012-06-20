# coding=utf8
from __future__ import print_function
import os, time, random, string
import common

'''
Формат файла со списоком юзеров "users.txt": 
user_login:user_password[:proxy_host:proxy_port[:proxy_login:proxy_password]]

Если для юзера не указан прокси, то он будет работать без прокси.
'''

USERDATA_FOLDER = 'userdata'

if not os.path.exists(USERDATA_FOLDER):
    os.makedirs(USERDATA_FOLDER)

class SocialUser(object):
    '''Абстрактный юзер социалки'''
    
    def __init__(self, bot=None):
        '''Инициализация'''
        self.bot = bot
        self.Clear()
    
    def _Print(self, text, end=None):
        '''Выводим текст на консоль'''
        if self.bot:
            self.bot._Print(text, end)
        else:
            print(text, end=end)
    
    def Clear(self):
        '''Очищаем данные юзера'''
        self.id = ''
        self.email = ''
        self.login = ''
        self.password = ''
        self.proxyHost = ''
        self.proxyPassword = ''
        self.cookieFileName = ''
        self.loggedIn = False

    def Load(self, login):
        '''Загружаем данные о юзере из списка юзеров'''
        self.Clear()
        data = usersList.GetUserData(login)
        if data == None:
            return False
        self.login = login
        self.password = data['password']
        self.proxyHost = data['proxyHost']
        self.proxyPassword = data['proxyPassword']
        self.cookieFileName = os.path.join(USERDATA_FOLDER, 'cookie-%s.txt' % self.login)
        self.loggedIn = False
        return True
    
    def Save(self):
        '''Сохраняем данные о юзере'''
        pass
    
    @classmethod
    def GenerateLogin(self):
        '''Генерируем логин'''
        pass  # TODO: реализовать
    
    @classmethod
    def GeneratePassword(self, length=-1):
        '''Генерируем пароль'''
        if length == -1:
            length = random.randint(7, 11)
        return ''.join(random.choice(string.letters + string.digits) for _ in xrange(length))
    
    @classmethod
    def GenerateBirthdate(self, dateStart='1949-01-01', dateEnd='1994-12-31', dateFormat='%Y-%m-%d'):  # TODO: доделать
        '''Генерируем дату рождения'''
        stime = time.mktime(time.strptime(dateStart, dateFormat))
        etime = time.mktime(time.strptime(dateEnd, dateFormat))
        ptime = stime + random.random() * (etime - stime)
        return time.strftime(dateFormat, time.localtime(ptime))


class SocialUsersList(object):
    '''Список юзеров'''
    
    def __init__(self):
        '''Инициализация'''
        self.usersDict = {}
        self.usersFileName = 'users.txt'
        self._LoadUsersList()
    
    def _LoadUsersList(self):
        '''Загружаем список юзеров из файла'''
        self.usersDict = {}
        if not os.path.exists(self.usersFileName):
            return
        for line in open(self.usersFileName).read().splitlines():
            if line.strip() == '':
                continue
            data = (line.strip() + ':' * 6).split(':')
            login = data[0]
            password = data[1]
            proxyHost = data[2] + ':' + data[3]
            if proxyHost == ':':
                proxyHost = ''
            proxyPassword = data[4] + ':' + data[5]
            if proxyPassword == ':':
                proxyPassword = ''
            self.usersDict[login] = {'password': password, 'proxyHost': proxyHost, 'proxyPassword': proxyPassword}
    
    def GetUserData(self, login):
        '''Отдаем данные о юзере по логину'''
        if login in self.usersDict:
            return self.usersDict[login]
    
    def GetLoginsList(self):
        '''Отдаем полный список логинов'''
        return self.usersDict.keys()

usersList = SocialUsersList()


if (__name__ == '__main__') and common.DevelopmentMode():
    pass
