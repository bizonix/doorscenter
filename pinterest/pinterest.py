# coding=utf8
from __future__ import print_function
import os, sys, re, time, datetime, random, pycurl, cStringIO, urllib, ConfigParser, yaml
import amazon, common

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

boardCategoriesList = ['architecture','art','cars_motorcycles','design','diy_crafts','education',
    'film_music_books','fitness','food_drink','gardening','geek','hair_beauty','history','holidays','home',
    'humor','kids','mylife','women_apparel','men_apparel','outdoors','people','pets','photography',
    'prints_posters','products','science','sports','technology','travel_places','wedding_events','other']

class PinterestUser(object):
    '''Юзер пинтереста'''
    
    def __init__(self, bot=None):
        '''Инициализация'''
        self.bot = bot
        self.usersFileName = 'users.txt'
        self.usersDict = {}
        self.usersDataFolder = 'userdata'
        self.Clear()
        self._LoadUsers()
    
    def _Print(self, text):
        '''Выводим текст на консоль'''
        if self.bot:
            self.bot._Print(text)
        else:
            print(text)
    
    def _LoadUsers(self):
        '''Загружаем список юзеров из файла'''
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
    
    def Clear(self):
        '''Очищаем данные юзера'''
        self.id = ''  # system, login (id) only
        self.login = ''  # users.txt, login (id) or email
        self.password = ''  # users.txt
        self.proxyHost = ''  # users.txt
        self.proxyPassword = ''  # users.txt
        self.authToken1 = ''  # system
        self.authToken2 = ''  # system
        self.boardsList = []  # system
        self.plannedCommonBoardsList = []  # editable
        self.plannedProfitBoardsList = []  # editable
        self.amazonPostedItemsList = []  # editable
    
    def FindUser(self, login): #TODO: объединить с LoadData
        '''Находим данные о юзере в списке юзеров'''
        self.Clear()
        if login in self.usersDict:
            data = self.usersDict[login]
            self.login = login
            self.password = data['password']
            self.proxyHost = data['proxyHost']
            self.proxyPassword = data['proxyPassword']
            return True
        else:
            self._Print('Username "%s" unknown, please fill its details in "%s"' % (login, self.usersFileName))
            return False
    
    def LoadData(self):
        '''Загружаем дальнейшие данные о юзере из файлов юзера'''
        systemDataFileName = os.path.join(self.usersDataFolder, 'system-%s.txt' % self.login)
        editableDataFileName = os.path.join(self.usersDataFolder, 'editable-%s.txt' % self.login)
        try:
            if not os.path.exists(systemDataFileName):
                return False
            data = yaml.load(open(systemDataFileName).read())
            self.id = data['id']
            self.authToken1 = data['authToken1']
            self.authToken2 = data['authToken2']
            self.boardsList = data['boardsList']
            if os.path.exists(editableDataFileName):
                data = yaml.load(open(editableDataFileName).read())
                if 'plannedCommonBoardsList' in data:
                    self.plannedCommonBoardsList = data['plannedCommonBoardsList']
                if 'plannedProfitBoardsList' in data:
                    self.plannedProfitBoardsList = data['plannedProfitBoardsList']
                if 'amazonPostedItemsList' in data:
                    self.amazonPostedItemsList = data['amazonPostedItemsList']
            return True
        except Exception as error:
            self._Print('### Error loading user data: %s' % error)
            return False
    
    def SaveData(self):
        '''Сохраняем данные о юзере в файлы'''
        systemDataFileName = os.path.join(self.usersDataFolder, 'system-%s.txt' % self.login)
        editableDataFileName = os.path.join(self.usersDataFolder, 'editable-%s.txt' % self.login)
        try:
            if not os.path.exists(self.usersDataFolder):
                os.makedirs(self.usersDataFolder)
            data = {'id': self.id, 'authToken1': self.authToken1, 'authToken2': self.authToken2, 'boardsList': self.boardsList}
            open(systemDataFileName, 'w').write(yaml.dump(data, default_flow_style=False))
            data = {'plannedCommonBoardsList': self.plannedCommonBoardsList, 'plannedProfitBoardsList': self.plannedProfitBoardsList, 'amazonPostedItems': self.amazonPostedItemsList}
            open(editableDataFileName, 'w').write(yaml.dump(data, default_flow_style=False))
        except Exception as error:
            self._Print('### Error saving user data: %s' % error)
    
    @classmethod
    def _SplitBoardName(self, boardName):
        '''Из строки вида "name[:category]" выделяем обе части'''
        if boardName.find(':') >= 0:
            name, _, category = boardName.partition(':')
            return name, category
        else:
            return boardName, ''
    
    def FindBoardByName(self, boardsList):
        '''Находим свою доску по полному или частичному совпадению названия из заданного списка'''
        random.shuffle(boardsList)
        random.shuffle(self.boardsList)
        for boardName in boardsList:
            boardName, _ = self._SplitBoardName(boardName)
            for board in self.boardsList:  # сначала ищем полное совпадение
                if board.name.lower() == boardName.lower():
                    return board
            for board in self.boardsList:  # потом частичное
                if board.name.lower().find(boardName.lower()) >= 0:
                    return board
    
    def FindBoardByCategory(self, category):
        '''Находим свою доску по категории'''
        random.shuffle(self.boardsList)
        for board in self.boardsList:
            if board.category == category:
                return board


class PinterestBoard(object):
    '''Доска пинтереста'''
    
    def __init__(self, idn, link, name, category=''):
        '''Инициализация'''
        self.id = idn
        self.link = link
        self.name = name
        self.category = category


class PlannedCommonBoard(object):
    '''Доска общей тематики, пополнение которой поставлено в расписание'''
    
    def __init__(self, name, category, keywordsList=[]):
        '''Инициализация'''
        self.name = name
        self.category = category
        self.keywordsList = keywordsList  # по каким кейвордам репостить на доску. можно не указывать для репоста по категории
    
    def GetKeywords(self):
        '''Возвращаем кейворды одной строкой'''
        return ','.join(self.keywordsList)


class PlannedProfitBoard(object):
    '''Доска с продвигаемыми товарами, пополнение которой поставлено в расписание'''
    
    def __init__(self, name, category, keywordsList, department, sourcesList=['pinterest', 'amazon']):
        '''Инициализация'''
        self.name = name
        self.category = category
        self.keywordsList = keywordsList  # по каким кейвордам репостить на доску с пинтереста и/или амазона, см. sourcesList
        self.department = department  # какой раздел амазона парсить
        self.sourcesList = sourcesList  # откуда репостить на доску. список с возможными значениями: "pinterest", "amazon"
    
    def GetKeywords(self):
        '''Возвращаем кейворды одной строкой'''
        return ','.join(self.keywordsList)


class PinterestBot(object):
    '''Private Pinterest Bot'''
    
    def __init__(self, printPrefix=None):
        '''Инициализация'''
        self.printPrefix = printPrefix
        self.user = PinterestUser(self)
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
        self.maxFailsCount = int(config.get('Pinterest', 'MaxFailsCount'))
        self.timeout = 60
        self.commentsList = []
        if os.path.exists('comments.txt'):
            self.commentsList = open('comments.txt').read().splitlines()
            self.commentsList = [item.strip() for item in self.commentsList if item.strip() != '']
    
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
        if self.user.id != '':
            logFileName = self.user.id + '-' + logFileName
        else:
            logFileName = 'unlogged-' + logFileName
        logFileName = os.path.join(common.LOG_FOLDER, logFileName)
        try:
            open(logFileName, 'w').write(data)
        except Exception as error:
            self._Print('### Error writing to log: %s' % error)
    
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
            if printText != '':
                self._Print(printText + ' ... ', '')
            else:
                self._Print('... ', '')
            
            '''Формируем заголовки'''
            headersList = []
            headersList.append('Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            headersList.append('Accept-Language: en-us,en;q=0.5')
            headersList.append('Referer: %s' % self.lastRequestUrl)
            if self.user.authToken1 != '' and self.user.authToken2 != '':
                headersList.append('Cookie: csrftoken=%s; _pinterest_sess=%s' % (self.user.authToken1, self.user.authToken2))
                if requestType in ['GET-X', 'POST', 'POST-MULTIPART']:
                    headersList.append('X-CSRFToken: %s' % self.user.authToken1)
                    headersList.append('X-Requested-With: XMLHttpRequest')
            
            '''Отправляем запрос'''
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
            if self.user.proxyHost != '':
                curl.setopt(pycurl.PROXY, self.user.proxyHost)
                if self.user.proxyPassword != '':
                    curl.setopt(pycurl.PROXYUSERPWD, self.user.proxyPassword)
            self.lastRequestTime = datetime.datetime.now()  # второй раз
            curl.perform()
            self.lastRequestTime = datetime.datetime.now()  # второй раз
            
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
            self._Print('### Error sending request: %s' % error)
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
            self._Print('### Error getting token: %s' % error)
            return ''
    
    def _GetTokensList(self, regexp, snippet=None):
        '''Извлекаем список токенов по регекспу'''
        try:
            if snippet == None:
                snippet = self.lastResponseBody
            return re.findall(regexp, snippet, re.M)
        except Exception as error:
            self._Print('### Error getting tokens list: %s' % error)
            return []
    
    def Login(self, userLogin):
        '''Логинимся в пинтерест'''
        if self.user.FindUser(userLogin):
            if self.user.LoadData():
                if self._Request('Checking if "%s" is logged in' % self.user.login, 'GET', 'http://pinterest.com/', None, 'Logout', 'ok', 'not logged in'):
                    return True
            if self._Request('Logging in with "%s"' % self.user.login, 'GET', 'https://pinterest.com/login/?next=%2F', None, 'csrfmiddlewaretoken', None, 'error'):
                self.user.authToken1 = self._GetToken(r'csrftoken=(.*?);', self.lastResponseHeaders)
                self.user.authToken2 = self._GetToken(r'_pinterest_sess=(.*?);', self.lastResponseHeaders)
                if self._Request('', 'POST', 'https://pinterest.com/login/?next=%2Flogin%2F', urllib.urlencode({'email': self.user.login, 'password': self.user.password, 'next': '/', 'csrfmiddlewaretoken': self.user.authToken1}), '_pinterest_sess', None, 'error'):
                    self.user.authToken2 = self._GetToken(r'_pinterest_sess=(.*?);', self.lastResponseHeaders)
                    if self._Request('', 'GET', 'http://pinterest.com/', None, 'Logout'):
                        self.user.id = self._GetToken(r'"UserNav">\s*<a href="/(.*?)/"')
                        self.user.SaveData()
                        self._ScrapeOwnBoards()
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
            self._Print('### Error getting user report: %s' % error)
    
    def ShowUserInfo(self):
        '''Выводим отчет по текущему юзеру'''
        if self._Request('Getting info about "%s"' % self.user.id, 'GET', 'http://pinterest.com/%s/' % self.user.id, None, 'Logout'):
            userReport = self._GetUserReport()
            if userReport:
                self._Print('Followers: %5d. Following: %5d. Boards: %5d. Pins: %5d. Likes: %5d.' % (userReport['followers'], userReport['following'], userReport['boards'], userReport['pins'], userReport['likes']))
    
    def _ScrapeOwnBoards(self):
        '''Получаем список своих досок'''
        if self._Request('Getting user boards info', 'GET', 'http://pinterest.com/%s/' % self.user.id, None, 'Logout', None, 'error'):
            self.user.boardsList = []
            boardsItemsList = self._GetTokensList(r'<div class="pin pinBoard" id="board([^"]*)">\s*?<h3 class="serif"><a href="/(.*?)/">([^<]*)</a></h3>')
            for item in boardsItemsList:
                boardId = item[0]
                boardLink = item[1]
                boardName = item[2]
                if self._Request('', 'GET', 'http://pinterest.com/%s/' % boardLink, None, 'Logout', None, 'error'):
                    boardCategory = self._GetToken(r'property="pinterestapp:category" content="([^"]*)"')
                    board = PinterestBoard(boardId, boardLink, boardName, boardCategory)
                    self.user.boardsList.append(board)
            self.user.SaveData()
            self._Print('done')
    
    def _CreateBoard(self, boardName, category=''):
        '''Создаем свою доску'''
        if category == '':
            text = 'Creating new board "%s"' % boardName
        else:
            text = 'Creating new board "%s" in category "%s"' % (boardName, category)
        if self.user.FindBoardByName([boardName]) == None:
            if (category != '') and (category not in boardCategoriesList):
                self._Print('incorrect category, ignoring', end='')
                category = ''
            if category == '':
                result = self._Request(text, 'POST', 'http://pinterest.com/board/create/', urllib.urlencode({'name': boardName}), '"status": "success"')
            else:
                result = self._Request(text, 'POST', 'http://pinterest.com/board/create/', urllib.urlencode({'name': boardName, 'category': category}), '"status": "success"')
            if result:
                boardId = self._GetToken(r'"id": "([^"]*)"')
                boardLink = self._GetToken(r'"url": "/(.*?)/"')
                board = PinterestBoard(boardId, boardLink, boardName, category)
                self.user.boardsList.append(board)
                self.user.SaveData()
        else:
            self._Print('already exists, skipped')
    
    def _FindOrCreateBoard(self, boardsList):
        '''Находим или создаем доску'''
        board = self.user.FindBoardByName(boardsList)
        if not board:
            boardName = random.choice(boardsList)
            boardName, category = self.user._SplitBoardName(boardName)
            board = self._CreateBoard(boardName, category)
        return board
    
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
    
    def FollowUsers(self, keywordsList, category, actionsCount):
        '''Ищем и фолловим юзеров'''
        usersList = []
        actionNum = 1
        failsCount = 0
        pageNum = 1
        
        while (actionNum <= actionsCount) and (failsCount < self.maxFailsCount):
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
                            failsCount += 1
                    else:
                        self._Print('followers less than following, skipped')
                else:
                    self._Print('error')
            elif self.lastResponseBody.find('Unfollow') >= 0:
                self._Print('already followed, skipped')
            else:
                self._Print('error')
        if failsCount >= self.maxFailsCount:
            self._Print('action cancelled, max fails count exceeded')
    
    def UnfollowUsers(self, actionsCount):
        '''Анфолловим юзеров'''
        if self._Request('Getting followers list', 'GET', 'http://pinterest.com/%s/following/' % self.user.id, None, 'Logout'):
            usersList = self._GetTokensList(r'"/([a-zA-Z0-9-/]*)/follow/">\s*?Unfollow')
            random.shuffle(usersList)
            actionNum = 1
            failsCount = 0
            
            #TODO: анфолловить только не взаимных
            while (actionNum <= actionsCount) and (failsCount < self.maxFailsCount):
                userId = usersList.pop(0)
                if self._Request('Unfollowing user "%s" (%d/%d)' % (userId, actionNum, actionsCount), 'GET', 'http://pinterest.com/%s/?d' % userId, None, 'Follow', None, None):
                    userReport = self._GetUserReport()
                    if userReport:
                        if userReport['followers'] < userReport['following']:
                            if self._Request('', 'POST', 'http://pinterest.com/%s/follow/' % userId, urllib.urlencode({'unfollow': '1'}), '"status": "success"'):
                                actionNum += 1
                            else:
                                failsCount += 1
                        else:
                            self._Print('followers greater than following, skipped')
                    else:
                        self._Print('error')
            if failsCount >= self.maxFailsCount:
                self._Print('action cancelled, max fails count exceeded')
    
    def FollowBoards(self, keywordsList, category, actionsCount):
        '''Ищем и фолловим доски'''
        boardsList = []
        actionNum = 1
        failsCount = 0
        pageNum = 1
        
        while (actionNum <= actionsCount) and (failsCount < self.maxFailsCount):
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
                else:
                    failsCount += 1
            elif self.lastResponseBody.find('Unfollow') >= 0:
                self._Print('already followed')
            else:
                self._Print('error')
        if failsCount >= self.maxFailsCount:
            self._Print('action cancelled, max fails count exceeded')
    
    def _LikePin(self, pinId):
        '''Лайкаем заданный пин'''
        return self._Request('', 'POST', 'http://pinterest.com/pin/%s/like/' % pinId, '', '"status": "success"')
    
    def _RepostPin(self, pinId, board):
        '''Репостим заданный пин'''
        if self._Request('', 'GET-X', 'http://pinterest.com/pin/%s/repindata/' % pinId, None, '"status": "success"', None, 'error'):
            pinDescription = self._GetToken(r'"details": "([^"]*)"')
            return self._Request('', 'POST', 'http://pinterest.com/pin/%s/repin/' % pinId, urllib.urlencode({'board': board.id, 'id': pinId, 'tags': '', 'replies': '', 'details': pinDescription, 'buyable': '', 'csrfmiddlewaretoken': self.user.authToken1}), '"status": "success"')
        else:
            return False
    
    def _CommentPin(self, pinId):
        '''Комментим заданный пин'''
        comment = random.choice(self.commentsList)
        return self._Request('', 'POST', 'http://pinterest.com/pin/%s/comment/' % pinId, urllib.urlencode({'text': comment, 'replies': '', 'path': '/pin/%s/' % pinId}), '"status": "success"')
    
    def _ActionPins(self, action, actionPrint, keywordsList, category, actionsCount, board=None):
        '''Действия с пинами'''
        pinsList = []
        actionNum = 1
        failsCount = 0
        pageNum = 1
        
        while (actionNum <= actionsCount) and (failsCount < self.maxFailsCount):
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
                    result = self._RepostPin(pinId, board)
                elif action == 'comment':
                    result = self._CommentPin(pinId)
                if result:
                    actionNum += 1
                else:
                    failsCount += 1
        if failsCount >= self.maxFailsCount:
            self._Print('action cancelled, max fails count exceeded')
    
    def LikePins(self, keywordsList, category, actionsCount):
        '''Лайкаем пины'''
        self._ActionPins('like', 'Liking', keywordsList, category, actionsCount)
        
    def RepostPins(self, keywordsList, category, actionsCount, boardsList):
        '''Репиним'''
        board = self._FindOrCreateBoard(boardsList)
        self._ActionPins('repost', 'Reposting to "%s"' % board.name, keywordsList, category, actionsCount, board)
    
    def CommentPins(self, keywordsList, category, actionsCount):
        '''Комментируем пины'''
        if len(self.commentsList) > 0:
            self._ActionPins('comment', 'Commenting', keywordsList, category, actionsCount)
        else:
            self._Print('No comments in the list, commenting skipped')
    
    def _AddPin(self, board, title, link, imageUrl, addText=''):
        '''Добавляем на свою доску свой пин'''
        if self._Request('Adding pin "%s" to board "%s"%s' % (title, board.name, addText), 'GET-X', 'http://pinterest.com/pin/create/find_images/?' + urllib.urlencode({'url': link.replace('http://', 'http%3A//')}), None, '"status": "success"', None, 'error'):
            if self._Request('', 'POST-MULTIPART', 'http://pinterest.com/pin/create/', [('board', board.id), ('details', title), ('link', link), ('img_url', imageUrl), ('tags', ''), ('replies', ''), ('peeps_holder', ''), ('buyable', ''), ('csrfmiddlewaretoken', self.user.authToken1)], '"status": "success"', None, 'error'):
                pinId = self._GetToken(r'"url": "/pin/([^/]*)/"')
                return self._Request('', 'GET', 'http://pinterest.com/pin/%s/' % pinId, None, 'Logout')
        return False
    
    def PostFromAmazon(self, keywordsList, actionsCount, boardsList, department='All'):
        '''Парсим амазон и постим на доску'''
        itemsList = []
        actionNum = 1
        failsCount = 0
        pageNum = 1
        
        '''Постим'''
        amazonObj = amazon.Amazon(self.printPrefix)
        while (actionNum <= actionsCount) and (failsCount < self.maxFailsCount):
            if len(itemsList) == 0:
                self._Print('Searching for Amazon goods by keywords "%s" in "%s" ... ' % (','.join(keywordsList), department), end='')
                itemsList = amazonObj.Parse(keywordsList, pageNum, department)
                self._Print('%d found' % len(itemsList))
                pageNum += 1
                if len(itemsList) == 0:
                    self._Print('Out of items')
                    break
            item = itemsList.pop(0)
            if item['id'] not in self.user.amazonPostedItemsList:
                board = self._FindOrCreateBoard(boardsList)
                if self._AddPin(board, item['title'], item['link'], item['imageUrl'], ' (%d/%d)' % (actionNum, actionsCount)):
                    self.user.amazonPostedItemsList.append(item['id'])
                    self.user.SaveData()
                    actionNum += 1
                else:
                    failsCount += 1
        if failsCount >= self.maxFailsCount:
            self._Print('action cancelled, max fails count exceeded')


if (__name__ == '__main__') and common.DevelopmentMode():
    bot = PinterestBot()
    bot.Login('searchxxx')
