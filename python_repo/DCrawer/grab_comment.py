# encoding:utf-8
__author__ = 'zhijieli'

import re,cookielib,urllib2

url_tpl = 'http://www.yododo.com/area/review/1-01-05-34-01?type=RV-1&pager.offset='
cookiePath = "cookie.txt"
headers={
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
    'Host':'www.yododo.com',
    'Connection':'keep-alive'
         }
# ------------------------------
# 请求数据
get_url = url_tpl + "0"
ckjar = cookielib.MozillaCookieJar(cookiePath)
ckproc = urllib2.HTTPCookieProcessor(ckjar)
openner = urllib2.build_opener(ckproc)
req = urllib2.Request(get_url,None,headers)
f_data = openner.open(req)
responseData = f_data.read()

# 匹配每一个点评DIV
regex_divComment = """<div class="poster-grid2">([\s\S]*?)</span>\r\n\s*</div>\r\n\s*</div>"""
p_divComment = re.compile(regex_divComment)
res_divComment = p_divComment.findall(responseData)
print res_divComment[1]