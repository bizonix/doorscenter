# coding=utf8
from __future__ import print_function
import os, sys, re, time, datetime, random, pycurl, cStringIO, ConfigParser
import common

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

class SocialUser(object):
    '''Абстрактный юзер социалки'''
    
    def __init__(self, bot=None):
        '''Инициализация'''
        self.bot = bot
        self._Clear()
        self.usersDict = None
        self.usersFileName = 'users.txt'
    
    def _Print(self, text, end=None):
        '''Выводим текст на консоль'''
        if self.bot:
            self.bot._Print(text, end)
        else:
            print(text, end=end)
    
    def _Clear(self):
        '''Очищаем данные юзера'''
        self.id = ''
        self.email = ''
        self.login = ''
        self.password = ''
        self.proxyHost = ''
        self.proxyPassword = ''

    def _LoadUsersList(self):
        '''Загружаем список юзеров из файла'''
        self.usersDict = {}
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

    def Load(self, login):
        '''Находим данные о юзере в списке юзеров'''
        self._Clear()
        if self.usersDict == None:
            self._LoadUsersList()
        if login not in self.usersDict:
            return False
        data = self.usersDict[login]
        self.login = login
        self.password = data['password']
        self.proxyHost = data['proxyHost']
        self.proxyPassword = data['proxyPassword']
        return True
    
    def Save(self):
        '''Сохраняем данные о юзере'''
        pass


class SocialBot(object):
    '''Абстрактный бот социалки'''
    
    def __init__(self):
        '''Инициализация'''
        self.screenSlot = common.ScreenSlot.Acquire()
        self.user = SocialUser(self)
        self.referer = ''
        self.lastRequestUrl = ''
        self.lastRequestTime = datetime.datetime.now() - datetime.timedelta(0, 43200)
        self.lastResponseHeaders = ''
        self.lastResponseBody = ''
        self.lastResponseSuccess = True
        self.lastPrintEnd = None
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        self.requestTimeoutMin = int(config.get('Bot', 'RequestTimeoutMin'))
        self.requestTimeoutMax = int(config.get('Bot', 'RequestTimeoutMax'))
        self.timeout = 60
    
    def __del__(self):
        '''Деструктор, освобождаем слот'''
        common.ScreenSlot.Release(self.screenSlot)
    
    def _Print(self, text, end=None):
        '''Выводим текст на консоль'''
        printPrefix = 'Thr.%3d : %s : %-20s : %s' % (self.screenSlot + 1, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.user.id, ' ' * self.screenSlot * 4)
        if (self.lastPrintEnd == '') and (text.strip() != '...'):
            text = '... ' + text
        text = printPrefix + text
        common.ThreadSafePrint(text)
        self.lastPrintEnd = end
    
    def _WriteLogFile(self, data):
        '''Пишем data в отдельный файл'''
        if common.LOG_LEVEL <= 0:
            return
        if (common.LOG_LEVEL <= 1) and self.lastResponseSuccess:
            return
        logFileName = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.html'
        if self.user.id != '':
            logFileName = self.user.id + ' ' + logFileName
        else:
            logFileName = '# unknown ' + logFileName
        logFileName = os.path.join(common.LOG_FOLDER, logFileName)
        try:
            open(logFileName, 'w').write(data)
        except Exception as error:
            self._Print('### Error writing to log: %s' % error)
    
    def _SolveCaptcha(self):
        '''При необходимости решаем капчу'''
        pass
    
    def _PrintExtendedErrorInfo(self):
        '''Выводим расширенную информацию о полученной ошибке'''
        pass
    
    def _Request(self, printText, requestType, url, postData=None, checkToken=None, printOk='done', printError='error'):
        '''Выдерживаем таймаут, выводим текст, отправляем запрос, проверям содержимое ответа, выводим текст в зависимости от наличия заданного токена.
        requestType: 'GET', 'GET-X', 'POST', 'POST-X', 'POST-MULTIPART'.'''
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
            headersList.append('Referer: %s' % self.referer)
            if requestType in ['GET-X', 'POST-X']:
                headersList.append('X-Requested-With: XMLHttpRequest')
            
            '''Отправляем запрос'''
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, url)
            if requestType in ['POST', 'POST-X']:
                curl.setopt(pycurl.POST, True)
                curl.setopt(pycurl.POSTFIELDS, postData)
            elif requestType == 'POST-MULTIPART':
                curl.setopt(pycurl.POST, True)
                curl.setopt(pycurl.HTTPPOST, postData)
            curl.setopt(pycurl.HTTPHEADER, headersList)
            curl.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0')
            curl.setopt(pycurl.COOKIEJAR, 'cookie.txt')  # TODO: файл с куками в зависимости от юзера
            curl.setopt(pycurl.COOKIEFILE, 'cookie.txt')
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
            
            '''При необходимости решаем капчу'''
            self._SolveCaptcha()
            
            '''Читаем ответ'''
            if not requestType.endswith('-X'):
                self.referer = url
            self.lastRequestUrl = url
            self.lastResponseHeaders = bufHeaders.getvalue()
            self.lastResponseBody = bufBody.getvalue()
            
            '''Определяем основные ошибки и выводим о них информацию'''
            statusCode = curl.getinfo(pycurl.HTTP_CODE)
            if statusCode not in [200, 302]:
                self._Print('error %d ' % statusCode, '')
            self._PrintExtendedErrorInfo()
            
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
        self._WriteLogFile(url + '\n\n' + self.lastResponseHeaders + '\n' + self.lastResponseBody)
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


if (__name__ == '__main__') and common.DevelopmentMode():
    bot = SocialBot()
    bot.Login('searchxxx')
