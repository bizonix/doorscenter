# coding=utf8
from __future__ import print_function
import os, sys, re, time, datetime, random, pycurl, cStringIO, pickle, hmac, base64, hashlib, urllib, ConfigParser
import amazon, common

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

class PinterestBot(object):
    '''Private Pinterest Bot'''
    
    def __init__(self, printPrefix=None):
        '''Инициализация'''
        self.printPrefix = printPrefix
        self.userData = {}
        self._ClearUserData()
        self.lastRequestUrl = 'http://pinterest.com/'
        self.lastRequestTime = datetime.datetime.now() - datetime.timedelta(0, 43200)
        self.lastResponseHeaders = ''
        self.lastResponseBody = ''
        self.lastResponseSuccess = True
        self.lastPrintEnd = None
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        self.requestTimeoutMin = int(config.get('Pinterest', 'RequestTimeoutMin'))
        self.requestTimeoutMax = int(config.get('Pinterest', 'RequestTimeoutMax'))
        self.timeout = 60
        self.usersDataFolder = 'userdata'
        self.boardCategoriesList = ['architecture','art','cars_motorcycles','design','diy_crafts','education',
            'film_music_books','fitness','food_drink','gardening','geek','hair_beauty','history','holidays','home',
            'humor','kids','mylife','women_apparel','men_apparel','outdoors','people','pets','photography',
            'prints_posters','products','science','sports','technology','travel_places','wedding_events','other']
        self.commentsList = []
        if os.path.exists('comments.txt'):
            self.commentsList = open('comments.txt').read().splitlines()
            self.commentsList = [item.strip() for item in self.commentsList if item.strip() != '']
    
    def _License1(self):
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        licenseUserName = config.get('License', 'UserName')
        licenseSecretKey = config.get('License', 'SecretKey')
        sessionKey = str(random.randint(100000000000, 999999999999))
        signature = base64.b64encode(hmac.new(licenseSecretKey, sessionKey, hashlib.sha256).digest())
        self.licenseCheckUrl = 'http://altstone.com/bot.php?' + urllib.urlencode({'username': licenseUserName, 'sessionkey': sessionKey, 'signature': signature})
    
    def _License2(self):
        if (random.randint(0, 99) <= 1) and ((self.licenseCheckUrl == None) or (self.licenseCheckUrl == '')):
            self._Print('### Error #521')
            sys.exit()
    
    def _License3(self):
        try:
            licenseResponse = urllib.urlopen(self.licenseCheckUrl).read()
            if (random.randint(0, 99) <= 1) and (licenseResponse != 'ok'):
                raise Exception('')
        except Exception:
            self._Print('### Error #762')
            sys.exit()
    
    def _Print(self, text, end=None):
        '''Выводим текст на консоль'''
        if self.printPrefix == None:  # однопоточный режим
            common.PrintThreaded(text, end)
            if common.LOG_LEVEL >= 1:
                common.PrintLogThreaded(text, end)
        else:  # многопоточный режим
            if self.lastPrintEnd == '':
                text = '... ' + text
            text = self.printPrefix + text
            common.PrintThreaded(text)  # в многопоточном режиме всегда выводим конец строки
            if common.LOG_LEVEL >= 1:
                common.PrintLogThreaded(text)
        self.lastPrintEnd = end
    
    def _WriteLog(self, data):
        '''Пишем в лог'''
        if common.LOG_LEVEL <= 0:
            return
        if (common.LOG_LEVEL <= 1) and self.lastResponseSuccess:
            return
        logFileName = str(int(time.time() * 100)) + '.txt'
        if self.userData['id'] != '':
            logFileName = self.userData['id'] + '-' + logFileName
        else:
            logFileName = 'unlogged-' + logFileName
        logFileName = os.path.join(common.LOG_FOLDER, logFileName)
        try:
            open(logFileName, 'w').write(data)
        except Exception as error:
            self._Print('### Error: %s' % error)
    
    def _ClearUserData(self):
        '''Очищаем данные юзера'''
        self.userData['id'] = ''
        self.userData['email'] = ''
        self.userData['password'] = ''
        self.userData['token1'] = ''
        self.userData['token2'] = ''
        self.userData['proxyHost'] = ''
        self.userData['proxyPassword'] = ''
        self.userData['amazonPostedItemsList'] = []
    
    def _LoadUserData(self, userEmail):
        '''Загружаем данные о юзере из файла'''
        userFileName = os.path.join(self.usersDataFolder, 'login-%s.txt' % userEmail)
        self._ClearUserData()
        if not os.path.exists(userFileName):
            return False
        try:
            self.userData = pickle.loads(base64.b64decode(open(userFileName).read()))
            return True
        except Exception as error:
            self._Print('### Error: %s' % error)
            return False
    
    def _SaveUserData(self):
        '''Сохраняем данные о юзере в файл'''
        userFileName = os.path.join(self.usersDataFolder, 'login-%s.txt' % self.userData['email'])
        try:
            if not os.path.exists(self.usersDataFolder):
                os.makedirs(self.usersDataFolder)
            open(userFileName, 'w').write(base64.b64encode(pickle.dumps(self.userData)))
        except Exception as error:
            self._Print('### Error: %s' % error)
    
    def _Request(self, printText, requestType, url, postData=None, checkToken=None, printOk='ok', printError='error'):
        '''Выдерживаем таймаут, выводим текст, отправляем запрос, проверям содержимое ответа, выводим текст в зависимости от наличия заданного токена.
        requestType: 'GET', 'GET-X', 'POST', 'POST-MULTIPART'.'''
        self.lastResponseHeaders = ''
        self.lastResponseBody = ''
        bufHeaders = cStringIO.StringIO()
        bufBody = cStringIO.StringIO()
        try:
            '''Выдерживаем случайный таймаут'''
            timeout = random.randint(self.requestTimeoutMin, self.requestTimeoutMax)
            lastRequestTimeDelta = (datetime.datetime.now() - self.lastRequestTime).seconds
            if timeout > lastRequestTimeDelta:
                time.sleep(timeout - lastRequestTimeDelta)
            
            '''Выводим текст'''
            self._Print(printText + ' ... ', '')
            
            '''Формируем заголовки'''
            headersList = []
            headersList.append('Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            headersList.append('Accept-Language: en-us,en;q=0.5')
            headersList.append('Referer: %s' % self.lastRequestUrl)
            if self.userData['token1'] != '' and self.userData['token2'] != '':
                headersList.append('Cookie: csrftoken=%s; _pinterest_sess=%s' % (self.userData['token1'], self.userData['token2']))
                if requestType in ['GET-X', 'POST', 'POST-MULTIPART']:
                    headersList.append('X-CSRFToken: %s' % self.userData['token1'])
                    headersList.append('X-Requested-With: XMLHttpRequest')
            
            '''Отправляем запрос'''
            self._License2()
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, url)
            if requestType == 'POST':
                curl.setopt(pycurl.POST, True)
                curl.setopt(pycurl.POSTFIELDS, postData)
            elif requestType == 'POST-MULTIPART':
                curl.setopt(pycurl.POST, True)
                curl.setopt(pycurl.HTTPPOST, postData)
            curl.setopt(pycurl.HTTPHEADER, headersList)
            curl.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0')
            curl.setopt(pycurl.SSL_VERIFYPEER, 0)
            curl.setopt(pycurl.SSL_VERIFYHOST, 0)
            curl.setopt(pycurl.FOLLOWLOCATION, 0)
            curl.setopt(pycurl.MAXREDIRS, 10)
            curl.setopt(pycurl.CONNECTTIMEOUT, self.timeout)
            curl.setopt(pycurl.TIMEOUT, self.timeout)
            curl.setopt(pycurl.HEADERFUNCTION, bufHeaders.write)
            curl.setopt(pycurl.WRITEFUNCTION, bufBody.write)
            if self.userData['proxyHost'] != '':
                curl.setopt(pycurl.PROXY, self.userData['proxyHost'])
                if self.userData['proxyPassword'] != '':
                    curl.setopt(pycurl.PROXYUSERPWD, self.userData['proxyPassword'])
            self._License3()
            self.lastRequestTime = datetime.datetime.now()
            curl.perform()
            
            '''Читаем ответ'''
            self.lastRequestUrl = url
            self.lastResponseHeaders = bufHeaders.getvalue()
            self.lastResponseBody = bufBody.getvalue()
            
            '''Проверям токен и выводим текст'''
            if checkToken != None:
                self.lastResponseSuccess = self.lastResponseBody.find(checkToken) >= 0
                if not self.lastResponseSuccess:
                    self.lastResponseSuccess = self.lastResponseHeaders.find(checkToken) >= 0
                if self.lastResponseSuccess:
                    if printOk:
                        self._Print(printOk)
                else:
                    if printError:
                        self._Print(printError)
            else:
                self.lastResponseSuccess = True
        except Exception as error:
            self._Print('### Error: %s' % error)
            self.lastResponseSuccess = False
        
        '''Пишем в лог и завершаем'''
        self._WriteLog(url + '\n\n' + self.lastResponseHeaders + '\n' + self.lastResponseBody)
        return self.lastResponseSuccess
    
    @classmethod
    def _LoadPage(self, fileName):
        '''Читаем страницу из файла'''
        return open(fileName).read()
    
    def _GetToken(self, regexp, snippet=None):
        '''Извлекаем токен по регекспу'''
        try:
            if snippet == None:
                snippet = self.lastResponseBody
            return re.findall(regexp, snippet, re.M)[0]
        except Exception as error:
            self._Print('### Error: %s' % error)
            return ''
    
    def _GetTokensList(self, regexp, snippet=None):
        '''Извлекаем список токенов по регекспу'''
        try:
            if snippet == None:
                snippet = self.lastResponseBody
            return re.findall(regexp, snippet, re.M)
        except Exception as error:
            self._Print('### Error: %s' % error)
            return []
    
    def Login(self, userEmail, userPassword, proxyHost='', proxyPassword=''):
        '''Логинимся в пинтерест'''
        self._License1()
        if self._LoadUserData(userEmail):
            if self._Request('Checking if "%s" is logged in' % self.userData['id'], 'GET', 'http://pinterest.com/', None, 'Logout', 'ok', 'not logged in'):
                return True
        self._ClearUserData()
        self.userData['email'] = userEmail
        self.userData['password'] = userPassword
        self.userData['proxyHost'] = proxyHost
        self.userData['proxyPassword'] = proxyPassword
        if self._Request('Logging in with "%s"' % self.userData['email'], 'GET', 'https://pinterest.com/login/?next=%2F', None, 'csrfmiddlewaretoken', None, 'error'):
            self.userData['token1'] = self._GetToken(r'csrftoken=(.*?);', self.lastResponseHeaders)
            self.userData['token2'] = self._GetToken(r'_pinterest_sess=(.*?);', self.lastResponseHeaders)
            if self._Request('', 'POST', 'https://pinterest.com/login/?next=%2Flogin%2F', urllib.urlencode({'email': self.userData['email'], 'password': self.userData['password'], 'next': '/', 'csrfmiddlewaretoken': self.userData['token1']}), '_pinterest_sess', None, 'error'):
                self.userData['token2'] = self._GetToken(r'_pinterest_sess=(.*?);', self.lastResponseHeaders)
                if self._Request('', 'GET', 'http://pinterest.com/', None, 'Logout'):
                    self.userData['id'] = self._GetToken(r'"UserNav">\s*<a href="/(.*?)/"')
                    self._ScrapeOwnBoards()
                    self._SaveUserData()
                    return True
        return False
    
    def _GetUserReport(self):
        '''Получаем отчет по произвольному юзеру. Вызывать после открытия страницы юзера'''
        try:
            userReport = {}
            userReport['followers'] = int(self._GetToken(r'<strong>(\d*)</strong> Follower'))
            userReport['following'] = int(self._GetToken(r'<strong>(\d*)</strong> Following'))
            userReport['boards'] = int(self._GetToken(r'<strong>(\d*)</strong> Board'))
            userReport['pins'] = int(self._GetToken(r'<strong>(\d*)</strong> Pin'))
            userReport['likes'] = int(self._GetToken(r'<strong>(\d*)</strong> Like'))
            return userReport
        except Exception as error:
            self._Print('### Error: %s' % error)
    
    def ShowUserInfo(self):
        '''Выводим отчет по текущему юзеру'''
        if self._Request('Getting info about "%s"' % self.userData['id'], 'GET', 'http://pinterest.com/%s/' % self.userData['id'], None, 'Logout'):
            userReport = self._GetUserReport()
            if userReport:
                self._Print('Followers: %5d. Following: %5d. Boards: %5d. Pins: %5d. Likes: %5d.' % (userReport['followers'], userReport['following'], userReport['boards'], userReport['pins'], userReport['likes']))
    
    def _ScrapeOwnBoards(self):
        '''Получаем список своих досок'''
        if self._Request('Getting user boards info', 'GET', 'http://pinterest.com/%s/' % self.userData['id'], None, 'Logout', None, 'error'):
            self.userData['boardsList'] = []
            boardsItemsList = self._GetTokensList(r'<div class="pin pinBoard" id="board([^"]*)">\s*?<h3 class="serif"><a href="/(.*?)/">([^<]*)</a></h3>')
            for item in boardsItemsList:
                boardId = item[0]
                boardLink = item[1]
                boardName = item[2]
                if self._Request('', 'GET', 'http://pinterest.com/%s/' % boardLink, None, 'Logout', None, 'error'):
                    boardCategory = self._GetToken(r'property="pinterestapp:category" content="([^"]*)"')
                self.userData['boardsList'].append({'id': boardId, 'link': boardLink, 'name': boardName, 'category': boardCategory})
            print('done')
            self._SaveUserData()
    
    @classmethod
    def _SplitBoardName(self, boardName):
        '''Из строки вида "name[:category]" выделяем обе части'''
        if boardName.find(':') >= 0:
            name, _, category = boardName.partition(':')
            return name, category
        else:
            return boardName, ''
    
    def _FindBoardByName(self, boardsList):
        '''Находим свою доску по полному или частичному совпадению названия из заданного списка'''
        random.shuffle(boardsList)
        random.shuffle(self.userData['boardsList'])
        for boardName in boardsList:
            boardName, _ = self._SplitBoardName(boardName)
            for board in self.userData['boardsList']:  # сначала ищем полное совпадение
                if board['name'].lower() == boardName.lower():
                    return board['id']
            for board in self.userData['boardsList']:  # потом частичное
                if board['name'].lower().find(boardName.lower()) >= 0:
                    return board['id']
    
    def _FindBoardByCategory(self, category):
        '''Находим свою доску по категории'''
        random.shuffle(self.userData['boardsList'])
        for board in self.userData['boardsList']:
            if board['category'] == category:
                return board['id']
    
    def _CreateBoard(self, boardName, category=''):
        '''Создаем свою доску'''
        if category == '':
            text = 'Creating new board "%s"' % boardName
        else:
            text = 'Creating new board "%s" in category "%s"' % (boardName, category)
        if self._FindBoardByName([boardName]) == None:
            if (category != '') and (category not in self.boardCategoriesList):
                self._Print('incorrect category, ignoring', end='')
                category = ''
            if category == '':
                result = self._Request(text, 'POST', 'http://pinterest.com/board/create/', urllib.urlencode({'name': boardName}), '"status": "success"')
            else:
                result = self._Request(text, 'POST', 'http://pinterest.com/board/create/', urllib.urlencode({'name': boardName, 'category': category}), '"status": "success"')
            if result:
                boardId = self._GetToken(r'"id": "([^"]*)"')
                boardLink = self._GetToken(r'"url": "/(.*?)/"')
                self.userData['boardsList'].append({'id': boardId, 'link': boardLink, 'name': boardName, 'category': category})
        else:
            self._Print('already exists, skipped')
    
    def _FindOrCreateBoard(self, boardsList):
        '''Находим или создаем доску'''
        boardId = self._FindBoardByName(boardsList)
        if not boardId:
            boardName = random.choice(boardsList)
            boardName, category = self._SplitBoardName(boardName)
            boardId = self._CreateBoard(boardName, category)
        return boardId
    
    def _ScrapeUsersByKeywords(self, keywordsList, pageNum):
        '''Ищем юзеров по заданным кеям на заданной странице'''
        usersList = []
        for keyword in keywordsList:
            if self._Request('Searching for users by keyword "%s" on page %d' % (keyword, pageNum), 'GET', 'http://pinterest.com/search/people/?q=%s&page=%d' % (keyword, pageNum), None, 'Logout', None, 'error'):
                newUsersList = self._GetTokensList(r'"/([a-zA-Z0-9-/]*)/follow/"')
                self._Print('%d found' % len(newUsersList))
                usersList.extend(newUsersList)
        usersList = list(set(usersList))
        random.shuffle(usersList)
        return usersList
    
    def _ScrapeBoardsByKeywords(self, keywordsList, pageNum):
        '''Ищем доски по заданным кеям на заданной странице'''
        boardsList = []
        for keyword in keywordsList:
            if self._Request('Searching for boards by keyword "%s" on page %d' % (keyword, pageNum), 'GET', 'http://pinterest.com/search/boards/?q=%s&page=%d' % (keyword, pageNum), None, 'Logout', None, 'error'):
                newBoardsList = self._GetTokensList(r'"/([a-zA-Z0-9-/]*)/follow/"')
                self._Print('%d found' % len(newBoardsList))
                boardsList.extend(newBoardsList)
        boardsList = list(set(boardsList))
        random.shuffle(boardsList)
        return boardsList
    
    def _ScrapePinsByKeywords(self, keywordsList, pageNum):
        '''Ищем пины по заданным кеям на заданной странице'''
        pinsList = []
        for keyword in keywordsList:
            if self._Request('Searching for pins by keyword "%s" on page %d' % (keyword, pageNum), 'GET', 'http://pinterest.com/search/?q=%s&page=%d' % (keyword, pageNum), None, 'Logout', None, 'error'):
                newPinsList = self._GetTokensList(r'"/pin/([0-9]*)/"')
                self._Print('%d found' % len(newPinsList))
                pinsList.extend(newPinsList)
        pinsList = list(set(pinsList))
        random.shuffle(pinsList)
        return pinsList
    
    def _ScrapeUsersByCategory(self, category, pageNum):
        '''Ищем юзеров по категории на заданной странице'''
        usersList = []
        if self._Request('Searching for users in category "%s" on page %d' % (category, pageNum), 'GET', 'http://pinterest.com/all/?category=%s&lazy=1&page=%d' % (category, pageNum), None, 'Logout', None, 'error'):
            usersList = self._GetTokensList(r'<a href="/(.*?)/">.*?</a> onto <a href="/.*?/">')
            self._Print('%d found' % len(usersList))
            random.shuffle(usersList)
        return usersList
    
    def _ScrapeBoardsByCategory(self, category, pageNum):
        '''Ищем борды по категории на заданной странице'''
        boardsList = []
        if self._Request('Searching for boards in category "%s" on page %d' % (category, pageNum), 'GET', 'http://pinterest.com/all/?category=%s&lazy=1&page=%d' % (category, pageNum), None, 'Logout', None, 'error'):
            boardsList = self._GetTokensList(r'<a href="/.*?/">.*?</a> onto <a href="/(.*?)/">')
            self._Print('%d found' % len(boardsList))
            random.shuffle(boardsList)
        return boardsList
    
    def _ScrapePinsByCategory(self, category, pageNum):
        '''Ищем пины по категории на заданной странице'''
        pinsList = []
        if self._Request('Searching for pins in category "%s" on page %d' % (category, pageNum), 'GET', 'http://pinterest.com/all/?category=%s&lazy=1&page=%d' % (category, pageNum), None, 'Logout', None, 'error'):
            pinsList = self._GetTokensList(r'"/pin/([0-9]*)/"')
            self._Print('%d found' % len(pinsList))
            random.shuffle(pinsList)
        return pinsList
    
    def _ScrapePinsPopular(self, pageNum):
        '''Ищем популярные пины на заданной странице'''
        pinsList = []
        if self._Request('Searching for popular pins on page %d' % pageNum, 'GET', 'http://pinterest.com/popular/?lazy=1&page=%d' % pageNum, None, 'Logout', None, 'error'):
            pinsList = self._GetTokensList(r'"/pin/([0-9]*)/"')
            self._Print('%d found' % len(pinsList))
            random.shuffle(pinsList)
        return pinsList
    
    def FollowUsers(self, keywordsList, category, actionsCountMin, actionsCountMax):
        '''Ищем и фолловим юзеров'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        usersList = []
        actionNum = 1
        pageNum = 1
        
        while actionNum <= actionsCount:
            if len(usersList) == 0:
                if category == '':
                    usersList = self._ScrapeUsersByKeywords(keywordsList, pageNum)
                else:
                    usersList = self._ScrapeUsersByCategory(category, pageNum)
                if len(usersList) == 0:
                    self._Print('Out of users')
                    break
                pageNum += 1
            userId = usersList.pop(0)
            if self._Request('Following user "%s" (%d/%d)' % (userId, actionNum, actionsCount), 'GET', 'http://pinterest.com/%s/?d' % userId, None, 'Follow', None, None):
                userReport = self._GetUserReport()
                if userReport:
                    if userReport['followers'] >= userReport['following']:
                        if self._Request('', 'POST', 'http://pinterest.com/%s/follow/' % userId, '', '"status": "success"'):
                            actionNum += 1
                    else:
                        self._Print('followers less than following, skipped')
                else:
                    self._Print('error')
            elif self.lastResponseBody.find('Unfollow') >= 0:
                self._Print('already followed, skipped')
            else:
                self._Print('error')
    
    def UnfollowUsers(self, actionsCountMin, actionsCountMax):
        '''Анфолловим юзеров'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        if self._Request('Getting followers list', 'GET', 'http://pinterest.com/%s/following/' % self.userData['id'], None, 'Logout'):
            usersList = self._GetTokensList(r'"/([a-zA-Z0-9-/]*)/follow/">\s*?Unfollow')
            random.shuffle(usersList)
            actionNum = 1
        
            #TODO: анфолловить только не взаимных
            while actionNum <= actionsCount:
                userId = usersList.pop(0)
                if self._Request('Unfollowing user "%s" (%d/%d)' % (userId, actionNum, actionsCount), 'GET', 'http://pinterest.com/%s/?d' % userId, None, 'Follow', None, None):
                    userReport = self._GetUserReport()
                    if userReport:
                        if userReport['followers'] < userReport['following']:
                            if self._Request('', 'POST', 'http://pinterest.com/%s/follow/' % userId, urllib.urlencode({'unfollow': '1'}), '"status": "success"'):
                                actionNum += 1
                        else:
                            self._Print('followers greater than following, skipped')
                    else:
                        self._Print('error')
    
    def FollowBoards(self, keywordsList, category, actionsCountMin, actionsCountMax):
        '''Ищем и фолловим доски'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        boardsList = []
        actionNum = 1
        pageNum = 1
        
        while actionNum <= actionsCount:
            if len(boardsList) == 0:
                if category == '':
                    boardsList = self._ScrapeBoardsByKeywords(keywordsList, pageNum)
                else:
                    boardsList = self._ScrapeBoardsByCategory(category, pageNum)
                if len(boardsList) == 0:
                    self._Print('Out of boards')
                    break
                pageNum += 1
            boardId = boardsList.pop(0)
            if self._Request('Following board "%s" (%d/%d)' % (boardId, actionNum, actionsCount), 'GET', 'http://pinterest.com/%s/' % boardId, None, 'Follow', None, None):
                if self._Request('', 'POST', 'http://pinterest.com/%s/follow/' % boardId, '', '"status": "success"'):
                    actionNum += 1
            elif self.lastResponseBody.find('Unfollow') >= 0:
                self._Print('already followed')
            else:
                self._Print('error')
    
    def _LikePin(self, pinId):
        '''Лайкаем заданный пин'''
        return self._Request('', 'POST', 'http://pinterest.com/pin/%s/like/' % pinId, '', '"status": "success"')
    
    def _RepostPin(self, pinId, boardsList):
        '''Репостим заданный пин'''
        if self._Request('', 'GET-X', 'http://pinterest.com/pin/%s/repindata/' % pinId, None, '"status": "success"', None, 'error'):
            pinDescription = self._GetToken(r'"details": "([^"]*)"')
            boardId = self._FindOrCreateBoard(boardsList)
            return self._Request('', 'POST', 'http://pinterest.com/pin/%s/repin/' % pinId, urllib.urlencode({'board': boardId, 'id': pinId, 'tags': '', 'replies': '', 'details': pinDescription, 'buyable': '', 'csrfmiddlewaretoken': self.userData['token1']}), '"status": "success"')
        else:
            return False
    
    def _CommentPin(self, pinId):
        '''Комментим заданный пин'''
        comment = random.choice(self.commentsList)
        return self._Request('', 'POST', 'http://pinterest.com/pin/%s/comment/' % pinId, urllib.urlencode({'text': comment, 'replies': '', 'path': '/pin/%s/' % pinId}), '"status": "success"')
    
    def _ActionPins(self, action, actionPrint, keywordsList, category, actionsCountMin, actionsCountMax, boardsList=None):
        '''Действия с пинами'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        pinsList = []
        actionNum = 1
        pageNum = 1
        
        while actionNum <= actionsCount:
            if len(pinsList) == 0:
                if category == '':
                    pinsList = self._ScrapePinsByKeywords(keywordsList, pageNum)
                elif category != 'popular':
                    pinsList = self._ScrapePinsByCategory(category, pageNum)
                else:
                    pinsList = self._ScrapePinsPopular(pageNum)
                if len(pinsList) == 0:
                    self._Print('Out of pins')
                    break
                pageNum += 1
            pinId = pinsList.pop(0)
            if self._Request('%s pin "%s" (%d/%d)' % (actionPrint, pinId, actionNum, actionsCount), 'GET', 'http://pinterest.com/pin/%s/' % pinId, None, 'Pinned', None, 'error'):
                result = False
                if action == 'like':
                    result = self._LikePin(pinId)
                elif action == 'repost':
                    result = self._RepostPin(pinId, boardsList)
                elif action == 'comment':
                    result = self._CommentPin(pinId)
                if result:
                    actionNum += 1
    
    def LikePins(self, keywordsList, category, actionsCountMin, actionsCountMax):
        '''Лайкаем пины'''
        self._ActionPins('like', 'Liking', keywordsList, category, actionsCountMin, actionsCountMax)
        
    def RepostPins(self, keywordsList, category, actionsCountMin, actionsCountMax, boardsList):
        '''Репиним'''
        self._ActionPins('repost', 'Reposting', keywordsList, category, actionsCountMin, actionsCountMax, boardsList)
    
    def CommentPins(self, keywordsList, category, actionsCountMin, actionsCountMax):
        '''Комментируем пины'''
        if len(self.commentsList) > 0:
            self._ActionPins('comment', 'Commenting', keywordsList, category, actionsCountMin, actionsCountMax)
        else:
            print('No comments in the list, commenting skipped')
    
    def _AddPin(self, boardId, title, link, imageUrl, addText=''):
        '''Добавляем на свою доску свой пин'''
        if self._Request('Adding pin "%s"%s' % (title, addText), 'GET-X', 'http://pinterest.com/pin/create/find_images/?' + urllib.urlencode({'url': link.replace('http://', 'http%3A//')}), None, '"status": "success"', None, 'error'):
            if self._Request('', 'POST-MULTIPART', 'http://pinterest.com/pin/create/', [('board', boardId), ('details', title), ('link', link), ('img_url', imageUrl), ('tags', ''), ('replies', ''), ('peeps_holder', ''), ('buyable', ''), ('csrfmiddlewaretoken', self.userData['token1'])], '"status": "success"', None, 'error'):
                pinId = self._GetToken(r'"url": "/pin/([^/]*)/"')
                return self._Request('', 'GET', 'http://pinterest.com/pin/%s/' % pinId, None, 'Logout')
        return False
    
    def PostFromAmazon(self, keywordsList, actionsCountMin, actionsCountMax, boardsList, department='All'):
        '''Парсим амазон и постим на доску'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        itemsList = []
        actionNum = 1
        pageNum = 1
        
        '''Читаем данные о запощенных товарах'''
        amazonDataFileName = os.path.join(self.usersDataFolder, 'amazon-%s.txt' % self.userData['email'])
        amazonPostedItemsList = []
        if os.path.exists(amazonDataFileName):
            amazonPostedItemsList = open(amazonDataFileName).read().splitlines()
        
        '''Постим'''
        amazonObj = amazon.Amazon(self.printPrefix)
        while actionNum <= actionsCount:
            if len(itemsList) == 0:
                self._Print('Searching for Amazon goods by keywords "%s" in "%s" ... ' % (','.join(keywordsList), department), end='')
                itemsList = amazonObj.Parse(keywordsList, pageNum, department)
                self._Print('%d found' % len(itemsList))
                pageNum += 1
                if len(itemsList) == 0:
                    self._Print('Out of items')
                    break
            item = itemsList.pop(0)
            if item['id'] not in amazonPostedItemsList:
                boardId = self._FindOrCreateBoard(boardsList)
                if self._AddPin(boardId, item['title'], item['link'], item['imageUrl'], ' (%d/%d)' % (actionNum, actionsCount)):
                    amazonPostedItemsList.append(item['id'])
                    open(amazonDataFileName, 'w').write('\n'.join(amazonPostedItemsList))
                    actionNum += 1

if __name__ == '__main__':
    bot = PinterestBot()
    bot.Login('alex@altstone.com', 'kernel32')
    bot.UnfollowUsers(1, 1)
