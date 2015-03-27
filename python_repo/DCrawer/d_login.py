# encoding:utf-8
__author__ = 'zhijieli'
# 模拟登陆

import urllib,urllib2,cookielib

login_url = "http://www.yododo.com/user/ajaxLogin.ydd"
lgoin_method = "POST"
cookiePath = "cookie.txt"


data = {'ajaxloginemail':'2390635102@qq.com',
        'ajaxloginpassword':'19920430',
        'ajaxverifycode':'',
        'ajaxRememberMe':'true'
        }

data_encode = urllib.urlencode(data)
headers={'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'}

req = urllib2.Request(login_url,data_encode,headers)
ckjar = cookielib.MozillaCookieJar(cookiePath)

ckproc = urllib2.HTTPCookieProcessor(ckjar)
opener = urllib2.build_opener(ckproc)

f = opener.open(req)

responeData = f.read()

fileWriter = open("loginData.txt","w")
fileWriter.write(responeData)
fileWriter.close()

ckjar.save(cookiePath,ignore_discard=True,ignore_expires=True)

# ckjar2 = cookielib.MozillaCookieJar(cookiePath)
# ckjar2.load(ignore_discard=True,ignore_expires=True)
# ckproc2 = urllib2.HTTPCookieProcessor(ckjar2)
# opener = urllib2.build_opener(ckproc2)