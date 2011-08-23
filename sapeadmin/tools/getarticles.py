# coding=utf8
import MySQLdb, random, codecs, hashlib, os

host = 'alexborisov.net'
user = 'alexbori_altston'
password = 'M7u3VUX)}TDZ'
database = 'alexbori_vpwebgrabber'
#localFolder = '/home/sasch/temp/articles'
localFolder = r'D:\Miscellaneous\Lodger6\articles'

results = ''
try:
    db = MySQLdb.connect(host=host, user=user, passwd=password, db=database, use_unicode=False, charset='utf8')
    try:
        count = 0
        cursor = db.cursor()
        try:
            '''Get quantity'''
            cursor.execute('select count(*) from `text`')
            row = cursor.fetchone()
            count = row[0]
            '''Get articles'''
            for n in range(count / 100 + 1):
                cursor.execute('select b.`url` as donorurl, a.`url`, a.`title`, a.`content` from `text` a left join `project` b on (a.`idproject`=b.`id`) limit %d, 100' % (n * 100))
                for row in cursor.fetchall():
                    donorurl = row[0]
                    url = row[1]
                    title = row[2]
                    contents = row[3]
                    md5 = hashlib.md5()
                    md5.update(contents)
                    digest = md5.hexdigest()
                    fileName = os.path.join(localFolder, digest + '.txt')
                    if not os.path.exists(fileName):
                        fd = codecs.open(fileName, 'w', 'cp1251')
                        fd.write(contents)
                        fd.close()
                print(n)
                break
        except Exception as error:
            results = error
        cursor.close()
    except Exception as error:
        results = error
    db.close()
except Exception as error:
    results = error
print(str(results))
