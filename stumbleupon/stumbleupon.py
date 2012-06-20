# coding=utf8
from __future__ import print_function
import os, sys, random, string, time, urllib, ConfigParser, json
import bot, botuser, captcha, proxy, common

if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

interestsDict = {'Action Movies': 256, 'Alternative News': 16, 'Ancient History': 470, 'Animals': 20, 'Arts': 441, 'Babes': 1675, 'Beer': 361,
    'Bizarre/Oddities': 426, 'Books': 455, 'Business': 61, 'Cars': 68, 'Cell Phones': 153, 'Chaos/Complexity': 74, 'Comedy Movies': 257,
    'Computer Graphics': 100, 'Computers': 93, 'Cult Films': 164, 'Design': 1116, 'Electronic Devices': 140, 'Entrepreneurship': 144,
    'Extreme Sports': 154, 'Facebook': 21534, 'Fine Arts': 166, 'Fitness': 415, 'Food/Cooking': 102, 'Futurism': 175, 'Gadgets': 2014,
    'Graphic Design': 187, 'History': 199, 'Humor': 207, 'Internet': 271, 'Internet Tools': 331, 'Ipod': 422, 'Logic': 238, 'Men\'s Issues': 391,
    'Movies': 255, 'Multimedia': 95, 'Music': 416, 'Mythology': 267, 'Nature': 270, 'Outdoors': 286, 'Painting': 288, 'Philosophy': 301,
    'Photography': 302, 'Photoshop': 1521, 'Psychology': 315, 'Quotes': 1881, 'Restaurants': 332, 'Rock music': 336, 'Science': 343,
    'Science Fiction': 342, 'Self Improvement': 348, 'Sexual Health': 330, 'Space Exploration': 209, 'Sports(General)': 31,
    'Technology': 1526, 'Television': 380, 'Travel': 393, 'UFOs': 395, 'Video Games': 399}


class StumbleUponUser(botuser.SocialUser):
    '''StumbleUpon User'''
    
    def __init__(self, bot=None):
        '''Инициализация'''
        super(StumbleUponUser, self).__init__(bot)


class StumbleUponBot(bot.SocialBot):
    '''StumbleUpon Bot'''
    
    def __init__(self):
        '''Инициализация'''
        super(StumbleUponBot, self).__init__()
        self.user = StumbleUponUser(self)
        self.recaptchaPublicKey = '6LfUNgAAAAAAAIb7Hs8kxh2HR-J77fb0dVT5PYxy'
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        self.accountCreationGenderRatio = float(config.get('StumbleUpon', 'AccountCreationGenderRatio'))
        self.accountCreationMainInterests = config.get('StumbleUpon', 'AccountCreationMainInterests')
    
    def _PrintExtendedErrorInfo(self):
        '''Выводим расширенную информацию о полученной ошибке'''
        if self.lastResponseBody.find('"_success":false') >= 0:
            errorText = ''
            jsonObj = json.loads(self.lastResponseBody)
            for item in jsonObj['_reason']:
                errorText += str(item['message']) + ' '
            errorText = errorText.strip()
            if errorText != '':
                self._Print('%s ' % errorText, '')
    
    def _NeedLogin(self, userLogin):
        '''Проверяем, залогинены ли в социалку'''
        return not self._Request('Checking if "%s" is logged in' % self.user.login, 'GET', 'http://www.stumbleupon.com/', None, 'Location: /home', 'yes', 'no')
    
    def _MakeLogin(self, userLogin):
        '''Логинимся. В качестве логина можно задавать ник или email'''
        if not self._Request('Logging in with "%s"' % self.user.login, 'GET', 'https://www.stumbleupon.com/login', None, 'Sign In', None, 'error opening the login page'):
            return False
        tokenLogin = self._GetToken(r'id="token" value="([^"]*)"')
        dataLogin = {'_output': 'Json', 'user': self.user.login, 'pass': self.user.password, 'remember': 'true', 'nativeSubmit': '0', '_action': 'auth', '_token': tokenLogin, '_method': 'create'}
        if not self._Request('', 'POST-X', 'https://www.stumbleupon.com/login', urllib.urlencode(dataLogin), '"_success":true', None, 'error logging in'):
            return False
        return self._Request('', 'GET', 'http://www.stumbleupon.com/home', None, 'Hi,', 'done', 'error opening the home page')
    
    def _CreateAccount(self, email, username, password, gender, birthdate, interestsList, proxyHost='', proxyPassword=''):
        '''Регаем аккаунт. Gender: 1 - man, 2 - woman. Birthday: YYYY-MM-DD.'''
        self._Logout()
        self.user.proxyHost = proxyHost
        self.user.proxyPassword = proxyPassword
        if not self._Request('Creating account', 'GET', 'http://www.stumbleupon.com/', None, 'Join for Free', None, 'error opening the main page'):
            return False
        '''Открываем страницу регистрации'''
        if not self._Request('', 'GET', 'https://www.stumbleupon.com/signup', None, 'Get Started', None, 'error opening the signup page'):
            return False
        tokenSignup = self._GetToken(r'"tokenSignup":"([^"]*)"')
        tokenEmail = self._GetToken(r'"tokenEmail":"([^"]*)"')
        tokenNick = self._GetToken(r'"tokenNick":"([^"]*)"')
        tokenPassword = self._GetToken(r'"tokenPassword":"([^"]*)"')
        '''Проверяем email, username и password'''
        dataEmail = {'_output': 'Json', 'email': email, 'signup': 'true', '_action': 'pageEmailCheck', '_token': tokenEmail, '_method': 'update'}
        if not self._Request('', 'POST-X', 'https://www.stumbleupon.com/signup/emailCheck', urllib.urlencode(dataEmail), '"_success":true', None, 'error checking email'):
            return False
        dataNick = {'_output': 'Json', 'username': username, '_action': 'pageNickCheck', '_token': tokenNick, '_method': 'update'}
        if not self._Request('', 'POST-X', 'https://www.stumbleupon.com/signup/nickCheck', urllib.urlencode(dataNick), '"_success":true', None, 'error checking username'):
            return False
        dataPassword = {'_output': 'Json', 'password': password, 'username': username, 'email': email, '_action': 'pagePasswordCheck', '_token': tokenPassword, '_method': 'update'}
        if not self._Request('', 'POST-X', 'https://www.stumbleupon.com/signup/passwordCheck', urllib.urlencode(dataPassword), '"_success":true', None, 'error checking password'):
            return False
        '''Запрашиваем, решаем и проверяем капчу'''
        while True:
            imageUrl, challenge = captcha.GetRecaptcha(self.recaptchaPublicKey)
            captchaText, captchaId = captcha.SolveCaptcha(imageUrl)
            dataCaptcha = {'_output': 'Json', '_action': 'processCaptcha', 'recaptcha_challenge_field': challenge, 'recaptcha_response_field': captchaText, '_token': tokenSignup, '_method': 'update'}
            if self._Request('', 'POST-X', 'https://www.stumbleupon.com/signup', urllib.urlencode(dataCaptcha), '"_success":true', None, 'error solving captcha, trying again ... '):
                break
            captcha.ReportCaptcha(captchaId)
        '''Регистрируемся'''
        dataSignup = {'_output': 'Json', 'email': email, 'username': username, 'password': password, 'gender': gender, 'date-hack': 'true', 'bmonth': int(birthdate[5:7]), 'bday': int(birthdate[8:]), 'byear': int(birthdate[:4]), 'findfriends': 'true', 'access_token': '', '_token': tokenSignup, '_action': 'page', 'nativeSubmit': '0', '_method': 'update'}
        if not self._Request('', 'POST-X', 'https://www.stumbleupon.com/signup', urllib.urlencode(dataSignup), '"_success":true', None, 'error registering'):
            return False
        '''Открываем страницу с интересами и выбираем их'''
        self._Request('', 'GET', 'https://www.stumbleupon.com/signup/choose-interests')
        tokenInterests = self._GetToken(r'id="token" value="([^"]*)"')
        dataInterests = {'displayed_interests[]': interestsDict.values(), 'interests[]': interestsList, '_action': 'submitInterests', '_token': tokenInterests}
        if not self._Request('', 'POST', 'https://www.stumbleupon.com/signup/choose-interests', urllib.urlencode(dataInterests, True), 'Location: /signup/tour', None, 'error setting interests'):  # note the True
            return False
        '''Открываем страницу с туром'''
        return self._Request('', 'GET', 'https://www.stumbleupon.com/signup/tour', None, 'Click "Stumble!" to get started', 'done', 'error opening the tour page')
    
    def CreateAccount(self, email, outputFileName):  #  TODO: выводить результат на консоль
        '''Генерируем параметры, создаем аккаунт и пишем результат в файл'''
        self._Logout()  # создаем аккаунт без каких-либо кук
        username = StumbleUponUser().GenerateLogin()
        password = StumbleUponUser().GeneratePassword()
        gender = 1 if random.random() < self.accountCreationGenderRatio else 2
        birthdate = StumbleUponUser().GenerateBirthdate()
        interestsList = random.sample(interestsDict.values(), random.randint(3, 7))  # TODO: добавлять обязательные
        proxyHost, proxyPassword = proxy.AcquireRandom()
        if self._CreateAccount(email, username, password, gender, birthdate, interestsList, proxyHost, proxyPassword):
            line = username + ':' + password
            if proxyHost != '':
                line += ':' + proxyHost
                if proxyPassword != '':
                    line += ':' + proxyPassword
            common.threadLock.acquire()
            open(outputFileName, 'a').write(line + '\n')
            common.threadLock.release()
    
    def _UserFollowAction(self, userLogin, action):
        '''Фолловим заданного юзера'''
        if not self._Request('%sing user "%s"' % (action.title(), userLogin), 'GET', 'http://www.stumbleupon.com/stumbler/%s' % userLogin, None, 'follow', None, 'error opening the user\'s page'):
            return False
        userId = self._GetToken(r'userid=(\d*)')
        tokenFollow = self._GetToken(r'","stumbler":"([^"]*)"')
        dataFollow = {'_output': 'Json', 'userid': userId, '_token': tokenFollow}
        if action == 'follow':
            dataFollow.update({'status': 'follow', '_method': 'create'})
        elif action == 'unfollow':
            dataFollow.update({'status': 'unfollow', '_method': 'update'})
        return self._Request('', 'POST-X', 'http://www.stumbleupon.com/follow/stumbler', urllib.urlencode(dataFollow), '"_success":true')
    
    def FollowUser(self, userLoginWho, userLoginWhom):
        '''Фолловим заданного юзера'''
        self._Login(userLoginWho)
        return self._UserFollowAction(userLoginWhom, 'follow')
    
    def UnfollowUser(self, userLoginWho, userLoginWhom):
        '''Анфолловим заданного юзера'''
        self._Login(userLoginWho)
        return self._UserFollowAction(userLoginWhom, 'unfollow')
    
    def Like(self, userLogin, pageUrl):
        '''Лайкаем'''
        self._Login(userLogin)
        pass  # TODO: реализовать


''' ... it should have account creation, follow mode and stumble mass like mode ... '''

if (__name__ == '__main__') and common.DevelopmentMode():
    bot = StumbleUponBot()
    #bot._CreateAccount('sasch5@altstone.com', 'searchxxx5', 'kernel32', 1, '1977-06-25')
    bot._Login('searchxxx5')
    #bot.UnfollowUser('ChrisMonty')
