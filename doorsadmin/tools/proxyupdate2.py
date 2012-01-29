# coding=utf8
import os, urllib2

proxyListUrlsDist = {'proxy-all.txt':'http://proxylist.fineproxy.ru/all.txt', 'proxy-anonymous.txt':'http://proxylist.fineproxy.ru/anon_and_elite.txt'}

for fileName, url in proxyListUrlsDist.items():
    proxyListStr = urllib2.urlopen(url).read()
    fileName = os.path.join(os.path.dirname(__file__), fileName)
    open(fileName, 'w').write(proxyListStr)
