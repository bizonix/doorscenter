# coding=utf8
from __future__ import print_function
import os, sys, re, time, datetime, random, pycurl, cStringIO, pickle, hmac, base64, hashlib, urllib
import amazon

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

class PinterestBot(object):
    '''Private Pinterest Bot'''
    
    def __init__(self, debugEnabled=False):
        '''Инициализация'''
        self.userData = {}
        self._ClearUserData()
        self.lastRequestUrl = 'http://pinterest.com/'
        self.lastRequestTime = datetime.datetime.now()
        self.lastResponseHeaders = ''
        self.lastResponseBody = ''
        self.timeout = 60
        self.usersDataFolder = 'users'
        self.debugFolder = 'debug'
        self.debugEnabled = debugEnabled
        self.boardCategoriesList = ['architecture','art','cars_motorcycles','design','diy_crafts','education',
            'film_music_books','fitness','food_drink','gardening','geek','hair_beauty','history','holidays','home',
            'humor','kids','mylife','women_apparel','men_apparel','outdoors','people','pets','photography',
            'prints_posters','products','science','sports','technology','travel_places','wedding_events','other']
    
    def _License1(self):
        dataList = open('license.ini').read().splitlines()
        licenseUserName = dataList[0]
        licenseSecretKey = dataList[1]
        sessionKey = str(random.randint(100000000000, 999999999999))
        signature = base64.b64encode(hmac.new(licenseSecretKey, sessionKey, hashlib.sha256).digest())
        self.licenseCheckUrl = 'http://altstone.com/bot.php?' + urllib.urlencode({'username': licenseUserName, 'sessionkey': sessionKey, 'signature': signature})
    
    def _License2(self):
        if (random.randint(0, 99) <= 1) and ((self.licenseCheckUrl == None) or (self.licenseCheckUrl == '')):
            print('### Error #521')
            sys.exit()

    def _License3(self):
        try:
            licenseResponse = urllib.urlopen(self.licenseCheckUrl).read()
            if (random.randint(0, 99) <= 1) and (licenseResponse != 'ok'):
                raise Exception('')
        except Exception:
            print('### Error #762')
            sys.exit()

    def _Debug(self, data):
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
        self.userData['id'] = ''
        self.userData['email'] = ''
        self.userData['password'] = ''
        self.userData['token1'] = ''
        self.userData['token2'] = ''
        self.userData['proxyHost'] = ''
        self.userData['proxyPassword'] = ''
        self.userData['amazonPostedItemsList'] = []
        self.userBoardsDist = {}
    
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
    
    def _Request(self, url, postData=None, postDataMultipart=None):
        '''Читаем урл'''
        try:
            bufHeaders = cStringIO.StringIO()
            bufBody = cStringIO.StringIO()
            self.lastResponseHeaders = ''
            self.lastResponseBody = ''
            
            '''Выдерживаем случайный таймаут'''
            timeout = random.randint(2, 5)
            lastRequestTimeDelta = (datetime.datetime.now() - self.lastRequestTime).seconds
            if timeout > lastRequestTimeDelta:
                time.sleep(timeout - lastRequestTimeDelta)
            
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
            self._License2()
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
            self._Debug(url + '\n\n' + self.lastResponseHeaders + '\n' + self.lastResponseBody)
        except Exception as error:
            print('### Error: %s' % error)
    
    @classmethod
    def _LoadPage(self, fileName):
        '''Читаем страницу из файла'''
        return open(fileName).read()
    
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
    
    def Login(self, userEmail, userPassword, proxyHost='', proxyPassword=''):
        '''Логинимся в пинтерест'''
        self._License1()
        if self._LoadUserData(userEmail):
            print('Checking if "%s" is logged in ... ' % self.userData['id'], end='')
            self._Request('http://pinterest.com/')
            if self.lastResponseBody.find('Logout') >= 0:
                print('ok')
                self._ScrapeOwnBoards()
                return
            else:
                print('not logged in')
        
        self._ClearUserData()
        self.userData['email'] = userEmail
        self.userData['password'] = userPassword
        self.userData['proxyHost'] = proxyHost
        self.userData['proxyPassword'] = proxyPassword
        
        print('Logging in "%s" (step 1) ... ' % self.userData['email'], end='')
        self._Request('https://pinterest.com/login/?next=%2F')
        self._CheckToken(self.lastResponseBody, 'csrfmiddlewaretoken', True)
        self.userData['token1'] = self._GetToken(self.lastResponseHeaders, "csrftoken=(.*?);")
        self.userData['token2'] = self._GetToken(self.lastResponseHeaders, "_pinterest_sess=(.*?);")
        
        print('Logging in "%s" (step 2) ... ' % self.userData['email'], end='')
        self._Request('https://pinterest.com/login/?next=%2Flogin%2F', 'email=%s&password=%s&next=/&csrfmiddlewaretoken=%s' % (self.userData['email'], self.userData['password'], self.userData['token1']))
        self._CheckToken(self.lastResponseHeaders, '_pinterest_sess', True)
        self.userData['token2'] = self._GetToken(self.lastResponseHeaders, "_pinterest_sess=(.*?);")
        
        print('Logging in "%s" (step 3) ... ' % self.userData['email'], end='')
        self._Request('http://pinterest.com/')
        self._CheckToken(self.lastResponseBody, 'Logout', True)
        self.userData['id'] = self._GetToken(self.lastResponseBody, '"UserNav">\s*<a href="/(.*?)/"')
        
        self._SaveUserData()
        self._ScrapeOwnBoards()
        print('User "%s" logged in successfully' % self.userData['id'])
    
    def UserReport(self):
        '''Отчет по юзеру'''
        pass
    
    def _ScrapeOwnBoards(self):
        '''Получаем список своих досок'''
        self.userBoardsDist = {}
        html = self.lastResponseBody
        html = html[html.find('class="BoardList"'):]
        html = html[:html.find('class="CreateBoard"')]
        idsList = self._GetTokensList(html, r'data="([^"]*)"')
        namesList = self._GetTokensList(html, r'<span>([^<]*)<')
        for n in range(len(idsList)):
            self.userBoardsDist[idsList[n]] = namesList[n]
    
    def _GetOwnBoard(self, keyword):
        '''Находим свою доску по кейворду'''
        boardsIds = self.userBoardsDist.keys()
        random.shuffle(boardsIds)
        for boardId in boardsIds:  # сначала ищем полное совпадение
            if self.userBoardsDist[boardId].lower() == keyword.lower():
                return boardId
        for boardId in boardsIds:  # потом частичное
            if self.userBoardsDist[boardId].lower().find(keyword.lower()) >= 0:
                return boardId
    
    def _CreateOwnBoard(self, boardName, category=''):
        '''Создаем свою доску'''
        if category == '':
            print('Creating new board "%s" ... ' % boardName, end='')
        else:
            print('Creating new board "%s" in category "%s" ... ' % (boardName, category), end='')
        if self._GetOwnBoard(boardName) == None:
            if (category != '') and (category not in self.boardCategoriesList):
                print('incorrect category, ignoring ... ')
                category = ''
            if category == '':
                self._Request('http://pinterest.com/board/create/', 'name=%s' % boardName)
            else:
                self._Request('http://pinterest.com/board/create/', 'name=%s&category=%s' % (boardName, category))
            self._CheckToken(self.lastResponseBody, '"status": "success"')
            boardId = self._GetToken(self.lastResponseBody, r'"id": "([^"]*)"')
            self.userBoardsDist[boardId] = boardName
        else:
            print('already exists, skipped')
    
    def _GetOrCreateOwnBoard(self, keyword, boardName, category=''):
        '''Находим или создаем доску'''
        boardId = self._GetOwnBoard(keyword)
        if not boardId:
            boardId = self._CreateOwnBoard(boardName, category)
        return boardId
    
    def _ScrapeUsers(self, keywordsList, pageNum):
        '''Ищем юзеров по заданным кеям на заданной странице'''
        for keyword in keywordsList:
            print('Searching for users by keyword "%s" on page %d ... ' % (keyword, pageNum), end='')
            self._Request('http://pinterest.com/search/people/?q=%s&page=%d' % (keyword, pageNum))
            newUsersList = self._GetTokensList(self.lastResponseBody, r'"/([a-zA-Z0-9-/]*)/follow/"')
            self.usersList.extend(newUsersList)
            print('%d found' % len(newUsersList))
        self.usersList = list(set(self.usersList))
        random.shuffle(self.usersList)
    
    def FollowUsers(self, keywordsList, actionsCountMin, actionsCountMax):
        '''Ищем и фолловим юзеров'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        self.usersList = []
        actionNum = 1
        pageNum = 1
        
        while actionNum <= actionsCount:
            if len(self.usersList) == 0:
                self._ScrapeUsers(keywordsList, pageNum)
                pageNum += 1
                if len(self.usersList) == 0:
                    print('Out of users')
                    break
            userId = self.usersList.pop()
            print('Following user "%s" (%d/%d) ... ' % (userId, actionNum, actionsCount), end='')
            self._Request('http://pinterest.com/%s/?d' % userId)
            if self.lastResponseBody.find('Follow') >= 0:
                print('... ', end='')
                self._Request('http://pinterest.com/%s/follow/' % userId, '1')
                if self._CheckToken(self.lastResponseBody, '"status": "success"'):
                    actionNum += 1
            elif self.lastResponseBody.find('Unfollow') >= 0:
                print('already followed')
            else:
                print('error')
    
    def UnfollowUsers(self, actionsCountMin, actionsCountMax):
        '''Анфолловим юзеров'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        self._Request('http://pinterest.com/%s/following/' % self.userData['id'])
        usersList = self._GetTokensList(self.lastResponseBody, r'"/([a-zA-Z0-9-/]*)/follow/">\s*?Unfollow')
        random.shuffle(usersList)
        actionNum = 1
    
        while actionNum <= actionsCount:
            userId = usersList.pop()
            print('Unfollowing user "%s" (%d/%d) ... ' % (userId, actionNum, actionsCount), end='')
            self._Request('http://pinterest.com/%s/follow/' % userId, 'unfollow=1')
            if self._CheckToken(self.lastResponseBody, '"status": "success"'):
                actionNum += 1
    
    def _ScrapeBoards(self, keywordsList, pageNum):
        '''Ищем доски по заданным кеям на заданной странице'''
        for keyword in keywordsList:
            print('Searching for boards by keyword "%s" on page %d ... ' % (keyword, pageNum), end='')
            self._Request('http://pinterest.com/search/boards/?q=%s&page=%d' % (keyword, pageNum))
            newBoardsList = self._GetTokensList(self.lastResponseBody, r'"/([a-zA-Z0-9-/]*)/follow/"')
            self.boardsList.extend(newBoardsList)
            print('%d found' % len(newBoardsList))
        self.boardsList = list(set(self.boardsList))
        random.shuffle(self.boardsList)
    
    def FollowBoards(self, keywordsList, actionsCountMin, actionsCountMax):
        '''Ищем и фолловим доски'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        self.boardsList = []
        actionNum = 1
        pageNum = 1
        
        while actionNum <= actionsCount:
            if len(self.boardsList) == 0:
                self._ScrapeBoards(keywordsList, pageNum)
                pageNum += 1
                if len(self.boardsList) == 0:
                    print('Out of boards')
                    break
            boardId = self.boardsList.pop()
            print('Following board "%s" (%d/%d) ... ' % (boardId, actionNum, actionsCount), end='')
            self._Request('http://pinterest.com/%s/' % boardId)
            if self.lastResponseBody.find('Follow') >= 0:
                print('... ', end='')
                self._Request('http://pinterest.com/%s/follow/' % boardId, '1')
                if self._CheckToken(self.lastResponseBody, '"status": "success"'):
                    actionNum += 1
            elif self.lastResponseBody.find('Unfollow') >= 0:
                print('already followed')
            else:
                print('error')
    
    def _ScrapePins(self, keywordsList, pageNum):
        '''Ищем пины по заданным кеям на заданной странице'''
        for keyword in keywordsList:
            if keyword == 'popular':
                print('Searching for popular pins on page %d ... ' % pageNum, end='')
                self._Request('http://pinterest.com/popular/?lazy=1&page=%d' % pageNum)
            else:
                print('Searching for pins by keyword "%s" on page %d ... ' % (keyword, pageNum), end='')
                self._Request('http://pinterest.com/search/?q=%s&page=%d' % (keyword, pageNum))
            newPinsList = self._GetTokensList(self.lastResponseBody, r'"/pin/([0-9]*)/"')
            self.pinsList.extend(newPinsList)
            print('%d found' % len(newPinsList))
        self.pinsList = list(set(self.pinsList))
        random.shuffle(self.pinsList)
    
    def LikePins(self, keywordsList, actionsCountMin, actionsCountMax):
        '''Лайкаем пины'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        self.pinsList = []
        actionNum = 1
        pageNum = 1
        
        while actionNum <= actionsCount:
            if len(self.pinsList) == 0:
                self._ScrapePins(keywordsList, pageNum)
                pageNum += 1
                if len(self.pinsList) == 0:
                    print('Out of pins')
                    break
            pinId = self.pinsList.pop()
            print('Liking pin "%s" (%d/%d) ... ' % (pinId, actionNum, actionsCount), end='')
            self._Request('http://pinterest.com/pin/%s/like/' % pinId, '1')
            if self._CheckToken(self.lastResponseBody, '"status": "success"'):
                actionNum += 1
    
    def RepostPins(self, keywordsList, actionsCountMin, actionsCountMax, boardsList):
        '''Репиним'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        'http://pinterest.com/pin/80361174570370064/repindata/'
        'http://pinterest.com/pin/80361174570370064/repin/'
        'board=213991488483272763&id=80361174570370064&tags=&replies=&details=777&buyable=&csrfmiddlewaretoken=610ec4d125a48e9769b591a0cfd049f6'
        pass
    
    def CommentPins(self, keywordsList, actionsCountMin, actionsCountMax):
        '''Комментируем пины'''
        pass
    
    def AddPin(self, boardId, title, link, imageUrl):
        '''Добавляем на свою доску свой пин'''
        '''print('Finding images for new pin "%s" ... ' % title, end='')
        self._Request('http://pinterest.com/pin/create/find_images/?' + urllib.urlencode({'url': link}))
        self._CheckToken(self.lastResponseBody, '"status": "success"', True)'''
        
        print('Adding new pin "%s" ... ' % title, end='')
        self._Request('http://pinterest.com/pin/create/', None, [('board', boardId), ('details', title), ('link', link), ('img_url', imageUrl), ('tags', ''), ('replies', ''), ('peeps_holder', ''), ('buyable', ''), ('csrfmiddlewaretoken', self.userData['token1'])])
        self._CheckToken(self.lastResponseBody, '"status": "success"', True)
        pinId = self._GetToken(self.lastResponseBody, r'"url": "/pin/([^/]*)/"')
        
        print('Viewing posted pin #%s ... ' % pinId, end='')
        self._Request('http://pinterest.com/pin/%s/' % pinId)
        print('ok')
    
    def AddPinsAmazon(self, keywordsList, actionsCountMin, actionsCountMax, boardsList, department='All'):
        '''Парсим амазон и постим на доску'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        amazonObj = amazon.Amazon()
        itemsList = amazonObj.Parse(','.join(keywordsList), actionsCount, department)
        for item in itemsList:
            if item['id'] in self.userData['amazonPostedItemsList']:
                continue
            self.AddPin(boardId, item['title'], item['link'], item['imageUrl'])
            self.userData['amazonPostedItemsList'].append(item['id'])
        pass


if __name__ == '__main__':
    userEmail = 'alex@altstone.com'
    userPassword = 'kernel32'
    bot = PinterestBot(True)
    bot.Login(userEmail, userPassword)
    bot.pinsList = []
    bot.LikePins(['popular'], 1, 1)
    #bot.AddPin('213991488483272763', 'xxx', 'http://www.amazon.com/PDX-FUCK-ME-SILLY-DUDE/dp/B0065M9922', 'http://ecx.images-amazon.com/images/I/41LYc9OfvGL._SL500_AA300_.jpg')
    #bot.AddPinsAmazon('213991488483272763', 'missoni', 3, 'Shoes')
