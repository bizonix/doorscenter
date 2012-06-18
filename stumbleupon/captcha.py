# coding=utf8
import re, urllib, ConfigParser
import common, deathbycaptcha

config = ConfigParser.RawConfigParser()
config.read('config.ini')
captchaService = config.get('Captcha', 'Service').lower()
captchaLogin = config.get('Captcha', 'Login')
captchaPassword = config.get('Captcha', 'Password')

def GetRecaptcha(publicKey):
    '''Запрашиваем картинку рекапчи, возвращаем url картинки и challenge'''
    requestUrl = 'http://www.google.com/recaptcha/api/challenge?' + urllib.urlencode({'k': publicKey, 'ajax': '1', 'lang': 'en'})
    response = urllib.urlopen(requestUrl).read()
    challenge = re.findall(r'challenge : \'([^\']*)\'', response, re.U)[0]
    imageUrl = 'http://www.google.com/recaptcha/api/image?' + urllib.urlencode({'c': challenge})
    return imageUrl, challenge

def SolveCaptcha(imageUrl):
    '''Решаем капчу, возвращаем текст и id капчи'''
    if captchaService == 'DeathByCaptcha'.lower():
        client = deathbycaptcha.HttpClient(captchaLogin, captchaPassword)
        try:
            captcha = client.decode(urllib.urlopen(imageUrl), deathbycaptcha.DEFAULT_TIMEOUT)
            return str(captcha['text']), captcha['captcha']
        except Exception as error:
            raise Exception('Failed solving captcha: %s' % error)
    else:
        raise Exception('Unknown captcha service')

def ReportCaptcha(captchaId):
    '''Сообщаем о неверном решении'''
    if captchaService == 'DeathByCaptcha'.lower():
        client = deathbycaptcha.HttpClient(captchaLogin, captchaPassword)
        try:
            client.report(captchaId)
        except Exception as error:
            raise Exception('Failed reporting captcha: %s' % error)
    else:
        raise Exception('Unknown captcha service')


if (__name__ == '__main__') and common.DevelopmentMode():
    imageUrl, challenge = GetRecaptcha('6LdYxc8SAAAAAHyLKDUP3jgHt11fSDW_WBwSPPdF')
    print(imageUrl, challenge)
    captchaText, captchaId = SolveCaptcha(imageUrl)
    print(captchaText, captchaId)
    #print(ReportCaptcha(captchaId))
