# coding=utf8
from __future__ import print_function
import os, sys, re, time, random, pycurl, cStringIO, pickle, base64, argparse

class Pinterest(object):
    '''Private Pinterest Bot'''
    
    def __init__(self, debugEnabled=False):
        '''Инициализация'''
        self._ClearUserData()
        self.lastRequestUrl = 'http://pinterest.com/'
        self.lastResponseHeaders = ''
        self.lastResponseBody = ''
        self.usersDataFolder = 'users'
        self.debugFolder = 'debug'
        self.debugEnabled = debugEnabled
    
    def _DebugWrite(self, data):
        '''Пишем дебаг'''
        if not self.debugEnabled:
            return
        debugFileName = str(int(time.time() * 100)) + '.txt'
        if self.userData['id'] != '':
            debugFileName = self.userData['id'] + '-' + debugFileName
        debugFileName = os.path.join(self.debugFolder, debugFileName)
        try:
            if not os.path.exists(self.debugFolder):
                os.makedirs(self.debugFolder)
            open(debugFileName, 'w').write(data)
        except Exception as error:
            print('### Error: %s' % error)
    
    def _ClearUserData(self):
        '''Очищаем данные юзера'''
        self.userData = {}
        self.userData['email'] = ''
        self.userData['password'] = ''
        self.userData['token1'] = ''
        self.userData['token2'] = ''
        self.userData['id'] = ''
        self.userData['proxyHost'] = ''
        self.userData['proxyPassword'] = ''
    
    def _LoadUserData(self, userEmail):
        '''Загружаем данные о юзере из файла'''
        userFileName = os.path.join(self.usersDataFolder, userEmail + '.txt')
        self._ClearUserData()
        if not os.path.exists(userFileName):
            return False
        try:
            self.userData = pickle.loads(base64.b64decode(open(userFileName).read()))
            return True
        except Exception as error:
            print('### Error: %s' % error)
            return False
    
    def _SaveUserData(self):
        '''Сохраняем данные о юзере в файл'''
        userFileName = os.path.join(self.usersDataFolder, self.userData['email'] + '.txt')
        try:
            if not os.path.exists(self.usersDataFolder):
                os.makedirs(self.usersDataFolder)
            open(userFileName, 'w').write(base64.b64encode(pickle.dumps(self.userData)))
        except Exception as error:
            print('### Error: %s' % error)
    
    def _GetPage(self, url, postData=None):
        '''Читаем урл и возвращаем текст'''
        try:
            bufHeaders = cStringIO.StringIO()
            bufBody = cStringIO.StringIO()
            headersList = []
            headersList.append('Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            headersList.append('Accept-Language: en-us,en;q=0.5')
            headersList.append('Referer: %s' % self.lastRequestUrl)
            if self.userData['token1'] != '' and self.userData['token2'] != '':
                headersList.append('Cookie: csrftoken=%s; _pinterest_sess=%s' % (self.userData['token1'], self.userData['token2']))
                if postData:
                    headersList.append('X-CSRFToken: %s' % self.userData['token1'])
                    headersList.append('X-Requested-With: XMLHttpRequest')
            '''Отправляем запрос'''
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, url)
            if postData:
                curl.setopt(pycurl.POSTFIELDS, postData)
            curl.setopt(pycurl.HTTPHEADER, headersList)
            curl.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0')
            curl.setopt(pycurl.SSL_VERIFYPEER, 0)
            curl.setopt(pycurl.SSL_VERIFYHOST, 0)
            curl.setopt(pycurl.FOLLOWLOCATION, 0)
            curl.setopt(pycurl.MAXREDIRS, 10)
            curl.setopt(pycurl.CONNECTTIMEOUT, 30)
            curl.setopt(pycurl.TIMEOUT, 30)
            curl.setopt(pycurl.HEADERFUNCTION, bufHeaders.write)
            curl.setopt(pycurl.WRITEFUNCTION, bufBody.write)
            #curl.setopt(pycurl.PROXY, random.choice(proxyUrls))
            #curl.setopt(pycurl.PROXYUSERPWD, proxyUser)
            curl.perform()
            '''Получаем ответ'''
            self.lastResponseHeaders = bufHeaders.getvalue()
            self.lastResponseBody = bufBody.getvalue()
            self._DebugWrite(url + '\n\n' + self.lastResponseHeaders + '\n' + self.lastResponseBody)
        except Exception as error:
            print('### Error: %s' % error)
            self.lastResponseBody = ''
        self.lastRequestUrl = url
    
    @classmethod
    def _LoadPage(self, fileName):
        '''Читаем страницу из файла'''
        return open(fileName).read()
    
    @classmethod
    def _Timeout(self):
        '''Выдерживаем случайный таймаут'''
        time.sleep(random.randint(1200, 2500) / 1000)
    
    @classmethod
    def _CheckToken(self, snippet, token, raiseException=False):
        '''Проверям наличие токена'''
        if snippet.find(token) >= 0:
            print('ok')
            return True
        else:
            print('error')
            if raiseException:
                raise Exception('')
            else:
                return False
    
    @classmethod
    def _GetToken(self, snippet, regexp):
        '''Извлекаем токен по регекспу'''
        try:
            return re.findall(regexp, snippet, re.M)[0]
        except Exception as error:
            print('### Error: %s' % error)
            return ''
    
    @classmethod
    def _GetTokensList(self, snippet, regexp):
        '''Извлекаем список токенов по регекспу'''
        try:
            return re.findall(regexp, snippet, re.M)
        except Exception as error:
            print('### Error: %s' % error)
            return []
    
    def Login(self, userEmail, userPassword, proxyHost, proxyPassword):
        '''Логинимся в пинтерест'''
        if self._LoadUserData(userEmail):
            print('Checking if "%s" is logged in ... ' % self.userData['id'], end='')
            self._GetPage('http://pinterest.com/')
            if self.lastResponseBody.find('Logout') >= 0:
                print('ok')
                self._Timeout()
                return
            else:
                print('not logged in')
                self._Timeout()
        
        self._ClearUserData()
        self.userData['email'] = userEmail
        self.userData['password'] = userPassword
        self.userData['proxyHost'] = proxyHost
        self.userData['proxyPassword'] = proxyPassword
        
        print('Logging in "%s" (step 1) ... ' % self.userData['email'], end='')
        self._GetPage('https://pinterest.com/login/?next=%2F')
        self._CheckToken(self.lastResponseBody, 'csrfmiddlewaretoken', True)
        self.userData['token1'] = self._GetToken(self.lastResponseHeaders, "csrftoken=(.*?);")
        self.userData['token2'] = self._GetToken(self.lastResponseHeaders, "_pinterest_sess=(.*?);")
        self._Timeout()
        
        print('Logging in "%s" (step 2) ... ' % self.userData['email'], end='')
        self._GetPage('https://pinterest.com/login/?next=%2Flogin%2F', 'email=%s&password=%s&next=/&csrfmiddlewaretoken=%s' % (self.userData['email'], self.userData['password'], self.userData['token1']))
        self._CheckToken(self.lastResponseHeaders, '_pinterest_sess', True)
        self.userData['token2'] = self._GetToken(self.lastResponseHeaders, "_pinterest_sess=(.*?);")
        self._Timeout()
        
        print('Logging in "%s" (step 3) ... ' % self.userData['email'], end='')
        self._GetPage('http://pinterest.com/')
        self._CheckToken(self.lastResponseBody, 'Logout', True)
        self.userData['id'] = self._GetToken(self.lastResponseBody, '"UserNav">\s*<a href="/(.*?)/"')
        self._Timeout()
        
        self._SaveUserData()
        print('User "%s" logged in successfully' % self.userData['id'])
    
    def _ScrapeUsers(self, keywordsList, pageNum):
        '''Ищем юзеров по заданным кеям на заданной странице'''
        for keyword in keywordsList:
            print('Searching for users by keyword "%s" on page %d ... ' % (keyword, pageNum), end='')
            self._GetPage('http://pinterest.com/search/people/?q=%s&page=%d' % (keyword, pageNum))
            newUsersList = self._GetTokensList(self.lastResponseBody, '"/([a-zA-Z0-9-/]*)/follow/"')
            self.usersList.extend(newUsersList)
            print('%d found' % len(newUsersList))
            self._Timeout()
        self.usersList = list(set(self.usersList))
        random.shuffle(self.usersList)
    
    def FollowUsers(self, keywordsList, followsCountMin, followsCountMax):
        '''Ищем и фолловим юзеров'''
        followsCount = random.randint(followsCountMin, followsCountMax)
        self.usersList = []
        followNum = 1
        pageNum = 1
        
        while followNum <= followsCount:
            if len(self.usersList) == 0:
                self._ScrapeUsers(keywordsList, pageNum)
                pageNum += 1
                if len(self.usersList) == 0:
                    print('Out of users')
                    break
            userId = self.usersList.pop()
            print('Following user "%s" (%d/%d) ... ' % (userId, followNum, followsCount), end='')
            self._GetPage('http://pinterest.com/%s/?d' % userId)
            if self.lastResponseBody.find('Follow') >= 0:
                print('... ', end='')
                self._Timeout()
                self._GetPage('http://pinterest.com/%s/follow/' % userId, '1')
                if self._CheckToken(self.lastResponseBody, '"status": "success"'):
                    followNum += 1
            elif self.lastResponseBody.find('Unfollow') >= 0:
                print('already followed')
            else:
                print('error')
            self._Timeout()
    
    def _ScrapeBoards(self, keywordsList, pageNum):
        '''Ищем доски по заданным кеям на заданной странице'''
        for keyword in keywordsList:
            print('Searching for boards by keyword "%s" on page %d ... ' % (keyword, pageNum), end='')
            self._GetPage('http://pinterest.com/search/boards/?q=%s&page=%d' % (keyword, pageNum))
            newBoardsList = self._GetTokensList(self.lastResponseBody, '"/([a-zA-Z0-9-/]*)/follow/"')
            self.boardsList.extend(newBoardsList)
            print('%d found' % len(newBoardsList))
            self._Timeout()
        self.boardsList = list(set(self.boardsList))
        random.shuffle(self.boardsList)
    
    def FollowBoards(self, keywordsList, followsCountMin, followsCountMax):
        '''Ищем и фолловим доски'''
        followsCount = random.randint(followsCountMin, followsCountMax)
        self.boardsList = []
        followNum = 1
        pageNum = 1
        
        while followNum <= followsCount:
            if len(self.boardsList) == 0:
                self._ScrapeBoards(keywordsList, pageNum)
                pageNum += 1
                if len(self.boardsList) == 0:
                    print('Out of boards')
                    break
            boardId = self.boardsList.pop()
            print('Following board "%s" (%d/%d) ... ' % (boardId, followNum, followsCount), end='')
            self._GetPage('http://pinterest.com/%s/' % boardId)
            if self.lastResponseBody.find('Follow') >= 0:
                print('... ', end='')
                self._Timeout()
                self._GetPage('http://pinterest.com/%s/follow/' % boardId, '1')
                if self._CheckToken(self.lastResponseBody, '"status": "success"'):
                    followNum += 1
            elif self.lastResponseBody.find('Unfollow') >= 0:
                print('already followed')
            else:
                print('error')
            self._Timeout()
    
    def _ScrapePins(self, keywordsList, pageNum):
        '''Ищем пины по заданным кеям на заданной странице'''
        for keyword in keywordsList:
            if keyword == 'popular':
                print('Searching for popular pins on page %d ... ' % pageNum, end='')
                self._GetPage('http://pinterest.com/popular/?lazy=1&page=%d' % pageNum)
            else:
                print('Searching for pins by keyword "%s" on page %d ... ' % (keyword, pageNum), end='')
                self._GetPage('http://pinterest.com/search/?q=%s&page=%d' % (keyword, pageNum))
            newPinsList = self._GetTokensList(self.lastResponseBody, '"/([a-zA-Z0-9-/]*)/follow/"')
            self.pinsList.extend(newPinsList)
            print('%d found' % len(newPinsList))
            self._Timeout()
        self.pinsList = list(set(self.pinsList))
        random.shuffle(self.pinsList)
    
    def LikePins(self, keywordsList, likesCountMin, likesCountMax):
        '''Ищем и фолловим доски'''
        likesCount = random.randint(likesCountMin, likesCountMax)
        self.pinsList = []
        likeNum = 1
        pageNum = 1
        
        while likeNum <= likesCount:
            if len(self.pinsList) == 0:
                self._ScrapePins(keywordsList, pageNum)
                pageNum += 1
                if len(self.pinsList) == 0:
                    print('Out of pins')
                    break
            pinId = self.pinsList.pop()
            print('Liking pin "%s" (%d/%d) ... ' % (pinId, likeNum, likesCount), end='')
            self._GetPage('http://pinterest.com/%s/' % pinId)
            if self.lastResponseBody.find('Like') >= 0:
                print('... ', end='')
                self._Timeout()
                self._GetPage('http://pinterest.com/%s/like/' % pinId, '1')
                if self._CheckToken(self.lastResponseBody, '"status": "success"'):
                    likeNum += 1
            elif self.lastResponseBody.find('Unlike') >= 0:
                print('already liked')
            else:
                print('error')
            self._Timeout()


class CommandsParser(object):
    '''Парсер командной строки'''
    
    def __init__(self):
        '''Инициализация'''
        self.parser = argparse.ArgumentParser(description='Private Pinterest Bot (c) search 2012')
        self.parser.add_argument('--email', required=True, help='user\'s email')
        self.parser.add_argument('--password', required=True, help='user\'s password')
        self.parser.add_argument('--action', choices=['follow-users', 'follow-boards', 'like-pins'], required=True, help='action to execute')
        self.parser.add_argument('--keywords', required=True, help='comma-separated keywords for scraping; use "popular" for liking popular pins')
        self.parser.add_argument('--countmin', type=int, required=True, help='minimal actions count')
        self.parser.add_argument('--countmax', type=int, required=True, help='maximum actions count')
        self.parser.add_argument('--proxy', default='', help='proxy host[:port]')
        self.parser.add_argument('--proxypwd', default='', help='proxy username:password')
    
    def Execute(self, commandString=None):
        '''Выполняем команды'''
        if commandString:
            args = self.parser.parse_args(commandString.split(' '))
        else:
            args = self.parser.parse_args()
        userEmail = args.email
        userPassword = args.password
        action = args.action
        actionsCountMin = args.countmin
        actionsCountMax = args.countmax
        keywordsList = args.keywords.split(',')
        proxyHost = args.proxy
        proxyPassword = args.proxypwd
        
        pinterest = Pinterest(True)
        pinterest.Login(userEmail, userPassword, proxyHost, proxyPassword)
        if action == 'follow-users':
            pinterest.FollowUsers(keywordsList, actionsCountMin, actionsCountMax)
        elif action == 'follow-boards':
            pinterest.FollowBoards(keywordsList, actionsCountMin, actionsCountMax)
        elif action == 'like-pins':
            pinterest.LikePins(keywordsList, actionsCountMin, actionsCountMax)


argsString = '--email=alex@altstone.com --password=kernel32 --action=follow-users --keywords=shoes,gucci --countmin=3 --countmax=5'
argsString = '--email=alex@altstone.com --password=kernel32 --action=follow-boards --keywords=shoes,gucci --countmin=3 --countmax=5'
commands = CommandsParser()
if len(sys.argv) > 1:
    commands.Execute()
else:
    commands.Execute(argsString)
