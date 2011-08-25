# coding=utf8
#from django.db.models import Q
from sapeadmin.models import Site, YandexUpdate, Donor, Article
import urllib, re, datetime, MySQLdb, hashlib, os, sys

def CronDaily():
    '''Функция вызывается по расписанию'''
    CheckYandexUpdates()

def CronHourly():
    '''Функция вызывается по расписанию'''
    CheckBotVisits()

def Helper():
    '''Запуск из командной строки'''
    ImportArticles('alexborisov.net', 'alexbori_altston', 'M7u3VUX)}TDZ', 'alexbori_vpwebgrabber', '/home/sasch/temp/articles')

def ImportArticles(host, user, password, database, localFolder):
    '''Импорт статей из граббера'''
    try:
        db = MySQLdb.connect(host=host, user=user, passwd=password, db=database, use_unicode=False, charset='utf8')
        try:
            cursor = db.cursor()
            try:
                '''Получаем количество статей'''
                count = 0
                cursor.execute('select count(*) from `text`')
                row = cursor.fetchone()
                count = row[0]
                print('Total articles: %d' % count)
                '''Загружаем статьи'''
                part = 100
                for n in range(count / part + 1):
                    print('Article #%d ...' % (n * part + 1))
                    cursor.execute('select b.`url` as donorurl, a.`url`, a.`title`, a.`content` from `text` a inner join `project` b on (a.`idproject`=b.`id`) limit %d, %d' % (n * part, part))
                    for row in cursor.fetchall():
                        try:
                            '''Получаем данные статьи'''
                            donorUrl = row[0]
                            url = row[1]
                            title = row[2]
                            text = row[3]
                            md5 = hashlib.md5()
                            md5.update(text)
                            fileDigest = md5.hexdigest()
                            fileName = os.path.join(localFolder, fileDigest + '.txt')
                            '''Ищем или добавляем донора'''
                            try:
                                donor, _ = Donor.objects.get_or_create(url=donorUrl)
                            except Exception as error:
                                print('Error adding a donor: %s' % error)
                                sys.exit(0)
                            '''Добавляем статью в базу'''
                            try:
                                article = Article.objects.create(donor=donor,
                                                                 url=url,
                                                                 title=title,
                                                                 fileName=fileName,
                                                                 fileDigest=fileDigest)
                                article.save()
                            except Exception as error:
                                pass
                            '''Сохраняем статью в файл'''
                            try:
                                fd = open(fileName, 'w')
                                fd.write(text)
                                fd.close()
                            except Exception as error:
                                print('Error writing an article to file: %s' % error)
                        except Exception as error:
                            print('Error getting an article: %s' % error)
            except Exception as error:
                print('Error in ImportArticles: %s' %  error)
            cursor.close()
        except Exception as error:
            print('Error in ImportArticles: %s' %  error)
        db.close()
    except Exception as error:
        print('Error in ImportArticles: %s' %  error)

def CheckBotVisits():
    '''Проверка захода ботов'''
    for site in Site.objects.filter(state='spam-indexed').order_by('pk').all():
        fd = urllib.urlopen('%sbots.php' % site.url)
        visitsCount = 0
        try:
            visitsCount = int(re.search(r'<b>(\d*)</b>', fd.read(), re.MULTILINE).group(1))
        except Exception:
            pass
        fd.close()
        site.botsVisitsCount = visitsCount
        if (site.botsVisitsDate == None) and (float(visitsCount) / site.pagesCount >= 0.85):
            site.botsVisitsDate = datetime.datetime.now()
        if visitsCount >= site.pagesCount:
            site.state = 'bot-visited'
        site.save()

def CheckYandexUpdates():
    '''Парсинг апдейтов яндекса'''
    fd = urllib.urlopen('http://tools.promosite.ru/updates/')
    update = ''
    try:
        update = re.search(u'Текстовый апдейт: выложен индекс по (.*)<br>', fd.read().decode('cp1251'), re.UNICODE).group(1)
    except Exception:
        pass
    fd.close()
    update = update.replace(u' января ', '.01.')
    update = update.replace(u' февраля ', '.02.')
    update = update.replace(u' марта ', '.03.')
    update = update.replace(u' апреля ', '.04.')
    update = update.replace(u' мая ', '.05.')
    update = update.replace(u' июня ', '.06.')
    update = update.replace(u' июля ', '.07.')
    update = update.replace(u' августа ', '.08.')
    update = update.replace(u' сентября ', '.09.')
    update = update.replace(u' октября ', '.10.')
    update = update.replace(u' ноября ', '.11.')
    update = update.replace(u' декабря ', '.12.')
    if len(update) == 9:
        update = '0' + update
    update = update[6:10] + '-' + update[3:5] + '-' + update[0:2]
    try:
        YandexUpdate.objects.create(dateUpdate=datetime.datetime.now(), dateIndex=update).save()
    except Exception:
        pass
