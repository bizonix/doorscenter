# coding=utf8
from __future__ import print_function
import os, sys, re, time, datetime, random, pycurl, cStringIO, pickle, hmac, base64, hashlib, urllib
import amazon, common

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

DEBUG_MODE = True

class PinterestBot(object):
    '''Private Pinterest Bot'''
    
    def __init__(self, printPrefix=None):
        '''Инициализация'''
        self.printPrefix = printPrefix
        self.userData = {}
        self._ClearUserData()
        self.lastRequestUrl = 'http://pinterest.com/'
        self.lastRequestTime = datetime.datetime.now()
        self.lastResponseHeaders = ''
        self.lastResponseBody = ''
        self.timeout = 60
        self.lastPrintEnd = None
        self.usersDataFolder = 'users'
        self.debugFolder = 'debug'
        self.boardCategoriesList = ['architecture','art','cars_motorcycles','design','diy_crafts','education',
            'film_music_books','fitness','food_drink','gardening','geek','hair_beauty','history','holidays','home',
            'humor','kids','mylife','women_apparel','men_apparel','outdoors','people','pets','photography',
            'prints_posters','products','science','sports','technology','travel_places','wedding_events','other']
        self.commentsList = open('comments.txt').read().splitlines()
        self.commentsList = [item.strip() for item in self.commentsList if item.strip() != '']
    
    def _License1(self):
        dataList = open('license.ini').read().splitlines()
        licenseUserName = dataList[0]
        licenseSecretKey = dataList[1]
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
        if self.printPrefix != None:
            text = self.printPrefix + text
            end = None  # в многопоточном режиме всегда выводим конец строки
        common.PrintThreaded(text, end)
        self.lastPrintEnd = end
    
    def _Debug(self, data):
        '''Пишем дебаг'''
        if not DEBUG_MODE:
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
            self._Print('### Error: %s' % error)
            return False
    
    def _SaveUserData(self):
        '''Сохраняем данные о юзере в файл'''
        userFileName = os.path.join(self.usersDataFolder, self.userData['email'] + '.txt')
        try:
            if not os.path.exists(self.usersDataFolder):
                os.makedirs(self.usersDataFolder)
            open(userFileName, 'w').write(base64.b64encode(pickle.dumps(self.userData)))
        except Exception as error:
            self._Print('### Error: %s' % error)
    
    def _Request(self, text, url, postData=None, postDataMultipart=None):
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
            
            '''Выводим текст'''
            self._Print(text + ' ... ', '')
            
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
            self._Print('### Error: %s' % error)
    
    @classmethod
    def _LoadPage(self, fileName):
        '''Читаем страницу из файла'''
        return open(fileName).read()
    
    def _CheckToken(self, snippet, token):
        '''Проверям наличие токена'''
        result = snippet.find(token) >= 0
        self._Print('ok' if result else 'error')
        return result
    
    def _GetToken(self, snippet, regexp):
        '''Извлекаем токен по регекспу'''
        try:
            return re.findall(regexp, snippet, re.M)[0]
        except Exception as error:
            self._Print('### Error: %s' % error)
            return ''
    
    def _GetTokensList(self, snippet, regexp):
        '''Извлекаем список токенов по регекспу'''
        try:
            return re.findall(regexp, snippet, re.M)
        except Exception as error:
            self._Print('### Error: %s' % error)
            return []
    
    def Login(self, userEmail, userPassword, proxyHost='', proxyPassword=''):
        '''Логинимся в пинтерест'''
        self._License1()
        if self._LoadUserData(userEmail):
            self._Request('Checking if "%s" is logged in' % self.userData['id'], 'http://pinterest.com/')
            if self.lastResponseBody.find('Logout') >= 0:
                self._Print('ok')
                self._ScrapeOwnBoards()
                return True
            else:
                self._Print('not logged in')
        
        self._ClearUserData()
        self.userData['email'] = userEmail
        self.userData['password'] = userPassword
        self.userData['proxyHost'] = proxyHost
        self.userData['proxyPassword'] = proxyPassword
        
        self._Request('Logging in "%s" (step 1)' % self.userData['email'], 'https://pinterest.com/login/?next=%2F')
        if not self._CheckToken(self.lastResponseBody, 'csrfmiddlewaretoken'):
            return False
        self.userData['token1'] = self._GetToken(self.lastResponseHeaders, "csrftoken=(.*?);")
        self.userData['token2'] = self._GetToken(self.lastResponseHeaders, "_pinterest_sess=(.*?);")
        
        self._Request('Logging in "%s" (step 2)' % self.userData['email'], 'https://pinterest.com/login/?next=%2Flogin%2F', urllib.urlencode({'email': self.userData['email'], 'password': self.userData['password'], 'next': '/', 'csrfmiddlewaretoken': self.userData['token1']}))
        if not self._CheckToken(self.lastResponseHeaders, '_pinterest_sess'):
            return False
        self.userData['token2'] = self._GetToken(self.lastResponseHeaders, "_pinterest_sess=(.*?);")
        
        self._Request('Logging in "%s" (step 3)' % self.userData['email'], 'http://pinterest.com/')
        if not self._CheckToken(self.lastResponseBody, 'Logout'):
            return False
        self.userData['id'] = self._GetToken(self.lastResponseBody, '"UserNav">\s*<a href="/(.*?)/"')
        
        self._SaveUserData()
        self._ScrapeOwnBoards()
        self._Print('User "%s" logged in successfully' % self.userData['id'])
        return True
    
    def _GetUserReport(self, userId):
        '''Получаем отчет по произвольному юзеру'''
        self._Request('Getting info about "%s"' % userId, 'http://pinterest.com/%s/' % userId)
        if self._CheckToken(self.lastResponseBody, 'Logout'):
            userReport = {}
            try:
                userReport['followers'] = int(self._GetToken(self.lastResponseBody, r'<strong>(\d*)</strong> Followers'))
                userReport['following'] = int(self._GetToken(self.lastResponseBody, r'<strong>(\d*)</strong> Following'))
                userReport['boards'] = int(self._GetToken(self.lastResponseBody, r'<strong>(\d*)</strong> Boards'))
                userReport['pins'] = int(self._GetToken(self.lastResponseBody, r'<strong>(\d*)</strong> Pins'))
                userReport['likes'] = int(self._GetToken(self.lastResponseBody, r'<strong>(\d*)</strong> Likes'))
            except Exception as error:
                self._Print('### Error: %s' % error)
                userReport = None
            return userReport
    
    def Report(self):
        '''Выводим отчет по текущему юзеру'''
        userReport = self._GetUserReport(self.userData['id'])
        if userReport:
            self._Print('Followers: %5d. Following: %5d. Boards: %5d. Pins: %5d. Likes: %5d.' % (userReport['followers'], userReport['following'], userReport['boards'], userReport['pins'], userReport['likes']))
    
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
    
    def _GetOwnBoard(self, keywordsList):
        '''Находим свою доску по кейворду'''
        boardsIds = self.userBoardsDist.keys()
        random.shuffle(boardsIds)
        random.shuffle(keywordsList)
        for keyword in keywordsList:
            for boardId in boardsIds:  # сначала ищем полное совпадение
                if self.userBoardsDist[boardId].lower() == keyword.lower():
                    return boardId
            for boardId in boardsIds:  # потом частичное
                if self.userBoardsDist[boardId].lower().find(keyword.lower()) >= 0:
                    return boardId
    
    def _CreateOwnBoard(self, boardName, category=''):
        '''Создаем свою доску'''
        if category == '':
            text = 'Creating new board "%s"' % boardName
        else:
            text = 'Creating new board "%s" in category "%s"' % (boardName, category)
        if self._GetOwnBoard(boardName) == None:
            if (category != '') and (category not in self.boardCategoriesList):
                self._Print('incorrect category, ignoring')
                category = ''
            if category == '':
                self._Request(text, 'http://pinterest.com/board/create/', urllib.urlencode({'name': boardName}))
            else:
                self._Request(text, 'http://pinterest.com/board/create/', urllib.urlencode({'name': boardName, 'category': category}))
            if self._CheckToken(self.lastResponseBody, '"status": "success"'):
                boardId = self._GetToken(self.lastResponseBody, r'"id": "([^"]*)"')
                self.userBoardsDist[boardId] = boardName
        else:
            self._Print('already exists, skipped')
    
    def _GetOrCreateOwnBoard(self, keywordsList, boardName, category=''):
        '''Находим или создаем доску'''
        boardId = self._GetOwnBoard(keywordsList)
        if not boardId:
            boardId = self._CreateOwnBoard(boardName, category)
        return boardId
    
    def _ScrapeUsers(self, keywordsList, pageNum):
        '''Ищем юзеров по заданным кеям на заданной странице'''
        for keyword in keywordsList:
            self._Request('Searching for users by keyword "%s" on page %d' % (keyword, pageNum), 'http://pinterest.com/search/people/?q=%s&page=%d' % (keyword, pageNum))
            newUsersList = self._GetTokensList(self.lastResponseBody, r'"/([a-zA-Z0-9-/]*)/follow/"')
            self.usersList.extend(newUsersList)
            self._Print('%d found' % len(newUsersList))
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
                    self._Print('Out of users')
                    break
            userId = self.usersList.pop()
            self._Request('Following user "%s" (%d/%d)' % (userId, actionNum, actionsCount), 'http://pinterest.com/%s/?d' % userId)
            if self.lastResponseBody.find('Follow') >= 0:
                self._Request('', 'http://pinterest.com/%s/follow/' % userId, '1')
                if self._CheckToken(self.lastResponseBody, '"status": "success"'):
                    actionNum += 1
            elif self.lastResponseBody.find('Unfollow') >= 0:
                self._Print('already followed')
            else:
                self._Print('error')
    
    def UnfollowUsers(self, actionsCountMin, actionsCountMax):
        '''Анфолловим юзеров'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        self._Request('Getting followers list', 'http://pinterest.com/%s/following/' % self.userData['id'])
        usersList = self._GetTokensList(self.lastResponseBody, r'"/([a-zA-Z0-9-/]*)/follow/">\s*?Unfollow')
        random.shuffle(usersList)
        actionNum = 1
    
        while actionNum <= actionsCount:
            userId = usersList.pop()
            self._Request('Unfollowing user "%s" (%d/%d)' % (userId, actionNum, actionsCount), 'http://pinterest.com/%s/follow/' % userId, urllib.urlencode({'unfollow': '1'}))
            if self._CheckToken(self.lastResponseBody, '"status": "success"'):
                actionNum += 1
    
    def _ScrapeBoards(self, keywordsList, pageNum):
        '''Ищем доски по заданным кеям на заданной странице'''
        for keyword in keywordsList:
            self._Request('Searching for boards by keyword "%s" on page %d' % (keyword, pageNum), 'http://pinterest.com/search/boards/?q=%s&page=%d' % (keyword, pageNum))
            newBoardsList = self._GetTokensList(self.lastResponseBody, r'"/([a-zA-Z0-9-/]*)/follow/"')
            self.boardsList.extend(newBoardsList)
            self._Print('%d found' % len(newBoardsList))
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
                    self._Print('Out of boards')
                    break
            boardId = self.boardsList.pop()
            self._Request('Following board "%s" (%d/%d)' % (boardId, actionNum, actionsCount), 'http://pinterest.com/%s/' % boardId)
            if self.lastResponseBody.find('Follow') >= 0:
                self._Request('', 'http://pinterest.com/%s/follow/' % boardId, '1')
                if self._CheckToken(self.lastResponseBody, '"status": "success"'):
                    actionNum += 1
            elif self.lastResponseBody.find('Unfollow') >= 0:
                self._Print('already followed')
            else:
                self._Print('error')
    
    def _ScrapePins(self, keywordsList, pageNum):
        '''Ищем пины по заданным кеям на заданной странице'''
        for keyword in keywordsList:
            if keyword == 'popular':
                self._Request('Searching for popular pins on page %d' % pageNum, 'http://pinterest.com/popular/?lazy=1&page=%d' % pageNum)
            else:
                self._Request('Searching for pins by keyword "%s" on page %d' % (keyword, pageNum), 'http://pinterest.com/search/?q=%s&page=%d' % (keyword, pageNum))
            newPinsList = self._GetTokensList(self.lastResponseBody, r'"/pin/([0-9]*)/"')
            self.pinsList.extend(newPinsList)
            self._Print('%d found' % len(newPinsList))
        self.pinsList = list(set(self.pinsList))
        random.shuffle(self.pinsList)
    
    def _LikePin(self, pinId):
        '''Лайкаем заданный пин'''
        self._Request('', 'http://pinterest.com/pin/%s/like/' % pinId, '1')
        return self._CheckToken(self.lastResponseBody, '"status": "success"')
    
    def _RepostPin(self, pinId, boardsList):
        '''Репостим заданный пин'''
        self._Request('', 'http://pinterest.com/pin/%s/repindata/' % pinId, '1')
        if self.lastResponseBody.find('"status": "success"') >= 0:
            pinDescription = self._GetToken(self.lastResponseBody, r'"details": "([^"]*)"')
            boardId = self._GetOwnBoard(boardsList)
            self._Request('', 'http://pinterest.com/pin/%s/repin/' % pinId, urllib.urlencode({'board': boardId, 'id': pinId, 'tags': '', 'replies': '', 'details': pinDescription, 'buyable': '', 'csrfmiddlewaretoken': self.userData['token1']}))
            return self._CheckToken(self.lastResponseBody, '"status": "success"')
        else:
            self._Print('error')
            return False
    
    def _CommentPin(self, pinId):
        '''Комментим заданный пин'''
        comment = random.choice(self.commentsList)
        self._Request('', 'http://pinterest.com/pin/%s/comment/' % pinId, urllib.urlencode({'text': comment, 'replies': '', 'path': '/pin/%s/' % pinId}))
        return self._CheckToken(self.lastResponseBody, '"status": "success"')
    
    def _ActionPins(self, action, actionPrint, keywordsList, actionsCountMin, actionsCountMax, boardsList=None):
        '''Действия с пинами'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        self.pinsList = []
        actionNum = 1
        pageNum = 1
        
        while actionNum <= actionsCount:
            if len(self.pinsList) == 0:
                self._ScrapePins(keywordsList, pageNum)
                pageNum += 1
                if len(self.pinsList) == 0:
                    self._Print('Out of pins')
                    break
            pinId = self.pinsList.pop()
            self._Request('%s pin "%s" (%d/%d)' % (actionPrint, pinId, actionNum, actionsCount), 'http://pinterest.com/pin/%s/' % pinId)
            if self.lastResponseBody.find('Pinned') >= 0:
                result = False
                if action == 'like':
                    result = self._LikePin(pinId)
                elif action == 'repost':
                    result = self._RepostPin(pinId, boardsList)
                elif action == 'comment':
                    result = self._CommentPin(pinId)
                if result:
                    actionNum += 1
            else:
                self._Print('error')
    
    def LikePins(self, keywordsList, actionsCountMin, actionsCountMax):
        '''Лайкаем пины'''
        self._ActionPins('like', 'Liking', keywordsList, actionsCountMin, actionsCountMax)
        
    def RepostPins(self, keywordsList, actionsCountMin, actionsCountMax, boardsList):
        '''Репиним'''
        self._ActionPins('repost', 'Reposting', keywordsList, actionsCountMin, actionsCountMax, boardsList)
    
    def CommentPins(self, keywordsList, actionsCountMin, actionsCountMax):
        '''Комментируем пины'''
        self._ActionPins('comment', 'Commenting', keywordsList, actionsCountMin, actionsCountMax)
    
    def AddPin(self, boardId, title, link, imageUrl):
        '''Добавляем на свою доску свой пин'''
        '''self._Request('Finding images for new pin "%s"' % title, 'http://pinterest.com/pin/create/find_images/?' + urllib.urlencode({'url': link}))
        if not self._CheckToken(self.lastResponseBody, '"status": "success"', True):
            return'''
        
        self._Request('Adding new pin "%s"' % title, 'http://pinterest.com/pin/create/', None, [('board', boardId), ('details', title), ('link', link), ('img_url', imageUrl), ('tags', ''), ('replies', ''), ('peeps_holder', ''), ('buyable', ''), ('csrfmiddlewaretoken', self.userData['token1'])])
        if not self._CheckToken(self.lastResponseBody, '"status": "success"', True):
            return
        pinId = self._GetToken(self.lastResponseBody, r'"url": "/pin/([^/]*)/"')
        
        self._Request('Viewing posted pin #%s' % pinId, 'http://pinterest.com/pin/%s/' % pinId)
        self._Print('ok')
    
    def AddPinsAmazon(self, keywordsList, actionsCountMin, actionsCountMax, boardsList, department='All'):
        '''Парсим амазон и постим на доску'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        amazonObj = amazon.Amazon(self.printPrefix)
        itemsList = amazonObj.Parse(','.join(keywordsList), actionsCount, department)
        for item in itemsList:
            if item['id'] in self.userData['amazonPostedItemsList']:
                continue
            self.AddPin(boardId, item['title'], item['link'], item['imageUrl'])
            self.userData['amazonPostedItemsList'].append(item['id'])
        pass


if __name__ == '__main__':
    bot = PinterestBot()
    bot.Login('alex@altstone.com', 'kernel32')
    #bot.Report()
    #bot.LikePins(['popular'], 1, 1)
    #bot.RepostPins(['popular'], 1, 1, ['home'])
    bot.CommentPins(['popular'], 1, 1)
    #bot.AddPin('213991488483272763', 'xxx', 'http://www.amazon.com/PDX-FUCK-ME-SILLY-DUDE/dp/B0065M9922', 'http://ecx.images-amazon.com/images/I/41LYc9OfvGL._SL500_AA300_.jpg')
    #bot.AddPinsAmazon('213991488483272763', 'missoni', 3, 'Shoes')
