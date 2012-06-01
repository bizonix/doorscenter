# coding=utf8
from __future__ import print_function
import os, sys, re, time, random, pycurl, cStringIO, pickle, base64, argparse
import amazon

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # убираем буферизацию stdout

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
    
    def _GetPage(self, url, postData=None, postDataMultipart=None):
        '''Читаем урл и возвращаем текст'''
        try:
            bufHeaders = cStringIO.StringIO()
            bufBody = cStringIO.StringIO()
            self.lastResponseHeaders = ''
            self.lastResponseBody = ''
            '''Формируем заголовки'''
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
            elif postDataMultipart:
                curl.setopt(pycurl.HTTPPOST, postDataMultipart)
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
            if self.userData['proxyHost'] != '':
                curl.setopt(pycurl.PROXY, self.userData['proxyHost'])
                if self.userData['proxyPassword'] != '':
                    curl.setopt(pycurl.PROXYUSERPWD, self.userData['proxyPassword'])
            curl.perform()
            '''Получаем ответ'''
            self.lastResponseHeaders = bufHeaders.getvalue()
            self.lastResponseBody = bufBody.getvalue()
            self.lastRequestUrl = url
            self._DebugWrite(url + '\n\n' + self.lastResponseHeaders + '\n' + self.lastResponseBody)
        except Exception as error:
            print('### Error: %s' % error)
    
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
    
    def _ScrapeOwnBoards(self):
        '''Получаем список своих досок'''
        pass
    
    def Login(self, userEmail, userPassword, proxyHost='', proxyPassword=''):
        '''Логинимся в пинтерест'''
        if self._LoadUserData(userEmail):
            print('Checking if "%s" is logged in ... ' % self.userData['id'], end='')
            self._GetPage('http://pinterest.com/')
            if self.lastResponseBody.find('Logout') >= 0:
                print('ok')
                self._Timeout()
                self._ScrapeOwnBoards()
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
        self._ScrapeOwnBoards()
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
    
    def AddPin(self, boardId, title, link, imageUrl):
        '''Добавляем на свою доску свой пин'''
        '''print('Finding images for new pin "%s" ... ' % title, end='')
        self._GetPage('http://pinterest.com/pin/create/find_images/?url=%s' % urllib.quote(link))
        self._CheckToken(self.lastResponseBody, '"status": "success"', True)
        self._Timeout()'''
        
        print('Adding new pin "%s" ... ' % title, end='')
        self._GetPage('http://pinterest.com/pin/create/', None, [('board', boardId), ('details', title), ('link', link), ('img_url', imageUrl), ('tags', ''), ('replies', ''), ('peeps_holder', ''), ('buyable', ''), ('csrfmiddlewaretoken', self.userData['token1'])])
        self._CheckToken(self.lastResponseBody, '"status": "success"', True)
        pinId = self._GetToken(self.lastResponseBody, r'"url": "/pin/([^/]*)/"')
        self._Timeout()
        
        print('Viewing posted pin #%s ... ' % pinId, end='')
        self._GetPage('http://pinterest.com/pin/%s/' % pinId)
        print('ok')
        self._Timeout()
    
    def AddPinsAmazon(self, boardId, keywordsList, pinsCountMin, pinsCountMax, department='All'):
        '''Парсим амазон и постим на доску'''
        pinsCount = random.randint(pinsCountMin, pinsCountMax)
        postedItems = []
        amazonObj = amazon.Amazon()
        itemsList = amazonObj.Parse(','.join(keywordsList), pinsCount, department)
        for item in itemsList:
            if item['id'] in postedItems:
                continue
            self.AddPin(boardId, item['title'], item['link'], item['imageUrl'])
            postedItems.append(item['id'])


class CommandsParser(object):
    '''Парсер командной строки и команд'''
    
    def __init__(self):
        '''Инициализация'''
        self.pinterest = Pinterest(True)
        self.loggedIn = False
    
    def Execute(self, command=None):
        '''Выполняем команды'''
        if not command:
            singleMode = ' '.join(sys.argv).find('--batchfile') < 0
        else:
            singleMode = command.find('--batchfile') < 0
        parser = argparse.ArgumentParser(description='Private Pinterest Bot (c) search 2012')
        parser.add_argument('--email', required=singleMode, help='user\'s email')
        parser.add_argument('--password', required=singleMode, help='user\'s password')
        parser.add_argument('--action', required=singleMode, choices=['follow-users', 'unfollow-users', 'follow-boards', 'like-pins', 'add-pins-amazon'], help='action to execute')
        parser.add_argument('--countmin', required=singleMode, type=int, help='minimal actions count')
        parser.add_argument('--countmax', required=singleMode, type=int, help='maximum actions count')
        parser.add_argument('--keywords', required=singleMode, help='comma-separated keywords for scraping; use "popular" for liking popular pins')
        parser.add_argument('--department', default='All', help='amazon department for searching goods')
        parser.add_argument('--proxy', default='', help='proxy host[:port]')
        parser.add_argument('--proxypwd', default='', help='proxy username:password')
        parser.add_argument('--batchfile', default='', help='commands file name for batch mode')
        if not command:
            args = parser.parse_args()
        else:
            args = parser.parse_args(command.split(' '))
        
        if singleMode:
            '''Одиночная команда'''
            userEmail = args.email
            userPassword = args.password
            action = args.action
            actionsCountMin = args.countmin
            actionsCountMax = args.countmax
            keywordsList = args.keywords.split(',')
            amazonDepartment = args.department
            proxyHost = args.proxy
            proxyPassword = args.proxypwd
            
            '''Логинимся'''
            if not self.loggedIn:
                self.pinterest.Login(userEmail, userPassword, proxyHost, proxyPassword)
                self.loggedIn = True
            
            '''Выполняем команду'''
            if action == 'follow-users':
                self.pinterest.FollowUsers(keywordsList, actionsCountMin, actionsCountMax)
            elif action == 'unfollow-users':
                self.pinterest.UnfollowUsers(actionsCountMin, actionsCountMax)
            elif action == 'follow-boards':
                self.pinterest.FollowBoards(keywordsList, actionsCountMin, actionsCountMax)
            elif action == 'like-pins':
                self.pinterest.LikePins(keywordsList, actionsCountMin, actionsCountMax)
            elif action == 'add-pins-amazon':
                self.pinterest.AddPinsAmazon('', keywordsList, actionsCountMin, actionsCountMax, amazonDepartment)
        else:
            '''Читаем и выполняем команды из файла'''
            batchFileName = args.batchfile
            print('=== Executing commands from "%s" ...' % batchFileName)
            try:
                commandsList = open(batchFileName).read().splitlines()
                for command in commandsList:
                    if command.strip() != '':
                        try:
                            self.Execute(command)
                        except Exception as error:
                            print('### Error: %s' % error)
            except Exception as error:
                print('### Error: %s' % error)
            print('=== Done commands from "%s".' % batchFileName)


'''userEmail = 'alex@altstone.com'
userPassword = 'kernel32'
pinterest = Pinterest(True)
pinterest.Login(userEmail, userPassword)
#pinterest.AddPin('213991488483272763', 'xxx', 'http://www.amazon.com/PDX-FUCK-ME-SILLY-DUDE/dp/B0065M9922', 'http://ecx.images-amazon.com/images/I/41LYc9OfvGL._SL500_AA300_.jpg')
pinterest.AddPinsAmazon('213991488483272763', 'missoni', 3, 'Shoes')
sys.exit()'''

if __name__ == '__main__':
    argsString = '--email=alex@altstone.com --password=kernel32 --action=follow-users --keywords=shoes,gucci --countmin=3 --countmax=5'
    argsString = '--email=alex@altstone.com --password=kernel32 --action=follow-boards --keywords=shoes,gucci --countmin=3 --countmax=5'
    #commands = CommandsParser(argsString)
    commands = CommandsParser()
    commands.Execute()
