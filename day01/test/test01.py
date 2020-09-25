# coding:utf-8
import urllib.request

httpurl = 'http://new.gb.oversea.cnki.net/index/'
httpresponse=urllib.request.urlopen(httpurl)
content =httpresponse.read().decode('utf-8')
file = open('./知网.html',"w",encoding='utf-8')
file.write(content)



