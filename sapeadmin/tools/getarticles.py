# coding=utf8
import MySQLdb, random, codecs

host = 'alexborisov.net'
user = 'alexbori_altston'
password = 'M7u3VUX)}TDZ'
database = 'alexbori_vpwebgrabber'
localFolder = '/home/sasch/temp/articles'

results = ''
try:
    db = MySQLdb.connect(host=host, user=user, passwd=password, db=database)
    try:
        cursor = db.cursor()
        try:
            cursor.execute('select `url`, `title`, `content` from `text` limit 0,3')
            for row in cursor.fetchall():
                url = row[0]
                title = row[1]
                contents = row[2]
                fileName = '%s/%d.txt' % (localFolder, random.randint(1000000,9999999))
                fd = codecs.open(fileName, 'w', 'cp1251')
                fd.write(contents)
                fd.close()
                print('%s: %s' % ('', fileName))
        except Exception as error:
            results = error
        cursor.close()
    except Exception as error:
        results = error
    db.close()
except Exception as error:
    results = error
print(str(results))
