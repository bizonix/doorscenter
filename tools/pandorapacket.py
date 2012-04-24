# coding=utf8

# ключи|текст|алгоритм|категории|папка на диске|урл дора|шаблон|профиль|ftp server|ftp login|ftp pwd|ftp folder|ключей от|ключей до|плотность от|плотность до
template = '[RANDOM]|[RANDOM]|1|none.txt|public_html/{0}/web|http://www.{0}/|hamptongaystory.co.uk|current.xml|ftp.narod.ru|login|pwd|/public_html/{0}/web|5000|7000|5|7'

domains = '''joemarkdesigns.com
cn-electronic.com
lifeskills-plus.com
willshad.com
chicagobearsfanforum.com
kerrieden.com
nlchessfest.com
ktaiwanita.com
bizoptest.com
mastinesdecuba.com'''

for domain in domains.splitlines():
    if domain.strip() != '':
        print(template.format(domain.strip()))
