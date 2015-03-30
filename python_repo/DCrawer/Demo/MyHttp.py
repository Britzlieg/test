# encoding:utf-8
__author__ = 'zhijieli'

import random,urllib2

class MyHttp:
    headers={
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
    'Host':'www.yododo.com',
    'Referer':'http://www.yododo.com/area/review/1-01-05-34-01?type=RV-1&pager.offset=0'
         }
    user_cookiePath = "mycookie.lwp"

    def __init__(self,proxylist):
        self.proxylist = proxylist
    def OpenWithURL(self,urlstr):
        # set proxy
        if len(self.proxylist) > 0:
            proxy_item = random.random * 60000 % len(self.proxylist)
            proxy = urllib2.ProxyHandler({'http': proxy_item})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
        # set cookie
        ckjar = cookielib.LWPCookieJar(self.user_cookiePath)
        ckjar.load(ignore_discard=True,ignore_expires=True)  # 又漏了这句
        ckproc = urllib2.HTTPCookieProcessor(ckjar)
        openner = urllib2.build_opener(ckproc)
        req = urllib2.Request(urlstr,None,self.headers)
        responseData = None
        try:
            f_data = openner.open(req)
            responseData = f_data.read()
        except urllib2.HTTPError, e:
            print e.code

        return responseData