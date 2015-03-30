# encoding:utf-8
__author__ = 'zhijieli'

# 尝试使用chrome的数据，用edit this cookie 这个插件

import urllib,urllib2,cookielib

login_url = "http://www.yododo.com/user/ajaxLogin.ydd"
lgoin_method = "POST"
cookiePath = "mycookie.lwp"


data = {'ajaxloginemail':'2390635102@qq.com',
        'ajaxloginpassword':'19920430',
        'ajaxverifycode':'',
        'ajaxRememberMe':'true'
        }

data_encode = urllib.urlencode(data)
headers={'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'}

req = urllib2.Request(login_url,data_encode,headers)
ckjar = cookielib.LWPCookieJar(cookiePath)

ckproc = urllib2.HTTPCookieProcessor(ckjar)
opener = urllib2.build_opener(ckproc)

f = opener.open(req)

responeData = f.read()


ckjar.save(cookiePath,ignore_discard=True,ignore_expires=True)
