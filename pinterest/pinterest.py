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
        self.usersDataFolder = 'userdata'
        self.debugFolder = 'debug'
        self.boardCategoriesList = ['architecture','art','cars_motorcycles','design','diy_crafts','education',
            'film_music_books','fitness','food_drink','gardening','geek','hair_beauty','history','holidays','home',
            'humor','kids','mylife','women_apparel','men_apparel','outdoors','people','pets','photography',
            'prints_posters','products','science','sports','technology','travel_places','wedding_events','other']
        self.commentsList = []
        if os.path.exists('comments.txt'):
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
    
    def _Request(self, printText, url, postData=None, postDataMultipart=None, checkToken=None, printOk='ok', printError='error'):
        '''Выдерживаем таймаут, выводим текст, отправляем запрос, проверям содержимое ответа, выводим текст в зависимости от наличия заданного токена'''
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
            self._Print(printText + ' ... ', '')
            
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
            
            '''Проверям токен и выводим текст'''
            if checkToken != None:
                result = self.lastResponseBody.find(checkToken) >= 0
                if not result:
                    result = self.lastResponseHeaders.find(checkToken) >= 0
                if result:
                    if printOk:
                        self._Print(printOk)
                else:
                    if printError:
                        self._Print(printError)
            else:
                result = True
            return result
        except Exception as error:
            self._Print('### Error: %s' % error)
            return False
    
    @classmethod
    def _LoadPage(self, fileName):
        '''Читаем страницу из файла'''
        return open(fileName).read()
    
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
            if self._Request('Checking if "%s" is logged in' % self.userData['id'], 'http://pinterest.com/', None, None, 'Logout', 'ok', 'not logged in'):
                self._ScrapeOwnBoards()
                return True
        self._ClearUserData()
        self.userData['email'] = userEmail
        self.userData['password'] = userPassword
        self.userData['proxyHost'] = proxyHost
        self.userData['proxyPassword'] = proxyPassword
        if self._Request('Logging in "%s"' % self.userData['email'], 'https://pinterest.com/login/?next=%2F', None, None, 'csrfmiddlewaretoken'):
            self.userData['token1'] = self._GetToken(self.lastResponseHeaders, "csrftoken=(.*?);")
            self.userData['token2'] = self._GetToken(self.lastResponseHeaders, "_pinterest_sess=(.*?);")
            if self._Request('', 'https://pinterest.com/login/?next=%2Flogin%2F', urllib.urlencode({'email': self.userData['email'], 'password': self.userData['password'], 'next': '/', 'csrfmiddlewaretoken': self.userData['token1']}), None, None, '_pinterest_sess'):
                self.userData['token2'] = self._GetToken(self.lastResponseHeaders, "_pinterest_sess=(.*?);")
                if self._Request('', 'http://pinterest.com/', None, None, 'Logout'):
                    self.userData['id'] = self._GetToken(self.lastResponseBody, '"UserNav">\s*<a href="/(.*?)/"')
                    self._SaveUserData()
                    self._ScrapeOwnBoards()
                    return True
        return False
    
    def _GetUserReport(self, userId):
        '''Получаем отчет по произвольному юзеру'''
        if self._Request('Getting info about "%s"' % userId, 'http://pinterest.com/%s/' % userId, None, None, 'Logout'):
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
    
    def _FindBoard(self, boardsList):
        '''Находим свою доску по кейворду'''
        boardsIds = self.userBoardsDist.keys()
        random.shuffle(boardsIds)
        random.shuffle(boardsList)
        for boardName in boardsList:
            for boardId in boardsIds:  # сначала ищем полное совпадение
                if self.userBoardsDist[boardId].lower() == boardName.lower():
                    return boardId
            for boardId in boardsIds:  # потом частичное
                if self.userBoardsDist[boardId].lower().find(boardName.lower()) >= 0:
                    return boardId
    
    def _CreateBoard(self, boardName, category=''):
        '''Создаем свою доску'''
        if category == '':
            text = 'Creating new board "%s"' % boardName
        else:
            text = 'Creating new board "%s" in category "%s"' % (boardName, category)
        if self._FindBoard([boardName]) == None:
            if (category != '') and (category not in self.boardCategoriesList):
                self._Print('incorrect category, ignoring')
                category = ''
            if category == '':
                result = self._Request(text, 'http://pinterest.com/board/create/', urllib.urlencode({'name': boardName}), None, '"status": "success"')
            else:
                result = self._Request(text, 'http://pinterest.com/board/create/', urllib.urlencode({'name': boardName, 'category': category}), None, '"status": "success"')
            if result:
                boardId = self._GetToken(self.lastResponseBody, r'"id": "([^"]*)"')
                self.userBoardsDist[boardId] = boardName
        else:
            self._Print('already exists, skipped')
    
    def _FindOrCreateBoard(self, boardsList, category=''):
        '''Находим или создаем доску'''
        boardId = self._FindBoard(boardsList)
        if not boardId:
            boardName = random.choice(boardsList)
            boardId = self._CreateBoard(boardName, category)
        return boardId
    
    def _ScrapeUsers(self, keywordsList, pageNum):
        '''Ищем юзеров по заданным кеям на заданной странице'''
        for keyword in keywordsList:
            if self._Request('Searching for users by keyword "%s" on page %d' % (keyword, pageNum), 'http://pinterest.com/search/people/?q=%s&page=%d' % (keyword, pageNum), None, None, 'Logout', None, 'error'):
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
            userId = self.usersList.pop(0)
            if self._Request('Following user "%s" (%d/%d)' % (userId, actionNum, actionsCount), 'http://pinterest.com/%s/?d' % userId, None, None, 'Follow', None, None):
                if self._Request('', 'http://pinterest.com/%s/follow/' % userId, '1', None, '"status": "success"'):
                    actionNum += 1
            elif self.lastResponseBody.find('Unfollow') >= 0:
                self._Print('already followed')
            else:
                self._Print('error')
    
    def UnfollowUsers(self, actionsCountMin, actionsCountMax):
        '''Анфолловим юзеров'''
        actionsCount = random.randint(actionsCountMin, actionsCountMax)
        if self._Request('Getting followers list', 'http://pinterest.com/%s/following/' % self.userData['id'], None, None, 'Logout'):
            usersList = self._GetTokensList(self.lastResponseBody, r'"/([a-zA-Z0-9-/]*)/follow/">\s*?Unfollow')
            random.shuffle(usersList)
            actionNum = 1
        
            while actionNum <= actionsCount:
                userId = usersList.pop(0)
                if self._Request('Unfollowing user "%s" (%d/%d)' % (userId, actionNum, actionsCount), 'http://pinterest.com/%s/follow/' % userId, urllib.urlencode({'unfollow': '1'}), None, '"status": "success"'):
                    actionNum += 1
    
    def _ScrapeBoards(self, keywordsList, pageNum):
        '''Ищем доски по заданным кеям на заданной странице'''
        for keyword in keywordsList:
            if self._Request('Searching for boards by keyword "%s" on page %d' % (keyword, pageNum), 'http://pinterest.com/search/boards/?q=%s&page=%d' % (keyword, pageNum), None, None, 'Logout', None, 'error'):
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
            boardId = self.boardsList.pop(0)
            if self._Request('Following board "%s" (%d/%d)' % (boardId, actionNum, actionsCount), 'http://pinterest.com/%s/' % boardId, None, None, 'Follow', None, None):
                if self._Request('', 'http://pinterest.com/%s/follow/' % boardId, '1', None, '"status": "success"'):
                    actionNum += 1
            elif self.lastResponseBody.find('Unfollow') >= 0:
                self._Print('already followed')
            else:
                self._Print('error')
    
    def _ScrapePins(self, keywordsList, pageNum):
        '''Ищем пины по заданным кеям на заданной странице'''
        for keyword in keywordsList:
            if keyword == 'popular':
                result = self._Request('Searching for popular pins on page %d' % pageNum, 'http://pinterest.com/popular/?lazy=1&page=%d' % pageNum, None, None, 'Logout', None, 'error')
            else:
                result = self._Request('Searching for pins by keyword "%s" on page %d' % (keyword, pageNum), 'http://pinterest.com/search/?q=%s&page=%d' % (keyword, pageNum), None, None, 'Logout', None, 'error')
            if result:
                newPinsList = self._GetTokensList(self.lastResponseBody, r'"/pin/([0-9]*)/"')
                self.pinsList.extend(newPinsList)
                self._Print('%d found' % len(newPinsList))
        self.pinsList = list(set(self.pinsList))
        random.shuffle(self.pinsList)
    
    def _LikePin(self, pinId):
        '''Лайкаем заданный пин'''
        return self._Request('', 'http://pinterest.com/pin/%s/like/' % pinId, '1', None, '"status": "success"')
    
    def _RepostPin(self, pinId, boardsList):
        '''Репостим заданный пин'''
        if self._Request('', 'http://pinterest.com/pin/%s/repindata/' % pinId, '1', None, '"status": "success"', None, 'error'):
            pinDescription = self._GetToken(self.lastResponseBody, r'"details": "([^"]*)"')
            boardId = self._FindOrCreateBoard(boardsList)
            return self._Request('', 'http://pinterest.com/pin/%s/repin/' % pinId, urllib.urlencode({'board': boardId, 'id': pinId, 'tags': '', 'replies': '', 'details': pinDescription, 'buyable': '', 'csrfmiddlewaretoken': self.userData['token1']}), None, '"status": "success"')
        else:
            return False
    
    def _CommentPin(self, pinId):
        '''Комментим заданный пин'''
        comment = random.choice(self.commentsList)
        return self._Request('', 'http://pinterest.com/pin/%s/comment/' % pinId, urllib.urlencode({'text': comment, 'replies': '', 'path': '/pin/%s/' % pinId}), None, '"status": "success"')
    
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
            pinId = self.pinsList.pop(0)
            if self._Request('%s pin "%s" (%d/%d)' % (actionPrint, pinId, actionNum, actionsCount), 'http://pinterest.com/pin/%s/' % pinId, None, None, 'Pinned', None, 'error'):
                result = False
                if action == 'like':
                    result = self._LikePin(pinId)
                elif action == 'repost':
                    result = self._RepostPin(pinId, boardsList)
                elif action == 'comment':
                    result = self._CommentPin(pinId)
                if result:
                    actionNum += 1
    
    def LikePins(self, keywordsList, actionsCountMin, actionsCountMax):
        '''Лайкаем пины'''
        self._ActionPins('like', 'Liking', keywordsList, actionsCountMin, actionsCountMax)
        
    def RepostPins(self, keywordsList, actionsCountMin, actionsCountMax, boardsList):
        '''Репиним'''
        self._ActionPins('repost', 'Reposting', keywordsList, actionsCountMin, actionsCountMax, boardsList)
    
    def CommentPins(self, keywordsList, actionsCountMin, actionsCountMax):
        '''Комментируем пины'''
        if len(self.commentsList) > 0:
            self._ActionPins('comment', 'Commenting', keywordsList, actionsCountMin, actionsCountMax)
        else:
            print('No comments in the list, skipping commenting')
    
    def _AddPin(self, boardId, title, link, imageUrl, addText=''):
        '''Добавляем на свою доску свой пин'''
        if self._Request('Adding new pin "%s"%s' % (title, addText), 'http://pinterest.com/pin/create/find_images/?' + urllib.urlencode({'url': link.replace('http://', 'http%3A//')}), '1', None, '"status": "success"', None, 'error'):
            if self._Request('', 'http://pinterest.com/pin/create/', None, [('board', boardId), ('details', title), ('link', link), ('img_url', imageUrl), ('tags', ''), ('replies', ''), ('peeps_holder', ''), ('buyable', ''), ('csrfmiddlewaretoken', self.userData['token1'])], '"status": "success"', None, 'error'):
                pinId = self._GetToken(self.lastResponseBody, r'"url": "/pin/([^/]*)/"')
                return self._Request('', 'http://pinterest.com/pin/%s/' % pinId, None, None, 'Logout')
        return False
    
    def AddPinsAmazon(self, keywordsList, actionsCountMin, actionsCountMax, boardsList, department='All'):
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
                itemsList = amazonObj.Parse(keywordsList, pageNum, department)
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
    #bot.Report()
    #bot.LikePins(['popular'], 1, 1)
    #bot.RepostPins(['popular'], 1, 1, ['home'])
    #bot.CommentPins(['popular'], 1, 1)
    #bot._AddPin('213991488483272763', 'xxx', 'http://www.amazon.com/PDX-FUCK-ME-SILLY-DUDE/dp/B0065M9922', 'http://ecx.images-amazon.com/images/I/41LYc9OfvGL._SL500_AA300_.jpg')
    bot.AddPinsAmazon(['missoni'], 2, 3, ['All the Random'], 'Shoes')
