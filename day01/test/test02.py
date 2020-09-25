import urllib.request
httpurl='https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png'
httpresponse = urllib.request.urlopen(httpurl)
file = open('./百度LOGO.png','wb')
content = httpresponse.read()
file.write(content)
