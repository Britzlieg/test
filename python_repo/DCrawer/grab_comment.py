# encoding:utf-8
__author__ = 'zhijieli'

import re,cookielib,urllib2,threading,thread,Queue,random


url_tpl = 'http://www.yododo.com/area/review/1-01-05-34-01?type=RV-1&pager.offset='
cookiePath = "mycookie.lwp"
headers={
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
    'Host':'www.yododo.com',
    'Connection':'keep-alive'
         }
queue = Queue.Queue()  # 多线程队列

# ------------------------------
# 获取详细评论
def getCommnet(link):
    proxy = urllib2.ProxyHandler({'http': '60.207.228.235:80'})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    req = urllib2.Request(link,None,headers)

    ckjar = cookielib.LWPCookieJar(cookiePath)

    ckproc = urllib2.HTTPCookieProcessor(ckjar)
    opener = urllib2.build_opener(ckproc)

    f = opener.open(req)
    responeData = f.read()

    regex = """<div class="poster-article">([\s\S]*?)</div>"""
    p = re.compile(regex)
    res_comment = p.findall(responeData)

    regex_time = """<span>发表于：(.*)</span>"""
    p_time = re.compile(regex_time)
    res_time = p_time.findall(responeData)

    comment_And_time = []
    comment_And_time.append(res_comment[0])
    comment_And_time.append(res_time[0])

    return comment_And_time

# 匹配景点
# 每一页
def pushItemWithOriginList(res_divComment):
    item_list = []
    for i in range(0,len(res_divComment)):
        item = []
        # 地址，点评
        res_addr = [] # 地点
        str_dianping = "" # 点评
        str_addr = ""
        regex_addr_1 = """<h1 class="ft18 fcgreen">\r\n\s*([\s\S]*?)<span class="dot-.*" title="(.*)">.*</span>\r\n\s*</h1>"""
        regex_addr_2 = """<h1 class="ft18 fcgreen">\r\n\s*([\s\S]*?)</h1>"""
        p_addr_1 = re.compile(regex_addr_1)
        res_addr = p_addr_1.findall(res_divComment[i])
        if(len(res_addr) == 0):
            p_addr_2 = re.compile(regex_addr_2)
            res_addr = p_addr_2.findall(res_divComment[i])
            str_dianping = ""
            str_addr = str(res_addr[0])
        else:
            str_dianping = str(res_addr[0][1])
            str_addr = str(res_addr[0][0])

        item.append(str_addr)
        item.append(str_dianping)

        # 获取连接
        regex_link = """<a class="fcblue" href="(.*)\" target"""
        p_link = re.compile(regex_link)
        res_link = p_link.findall(res_divComment[i])
        str_link = "http://www.yododo.com/" + res_link[0]
        item.append(str_link)

        # 获取时间和正文
        comentAndTime = getCommnet(str_link)
        str_comment = comentAndTime[0]
        str_time = comentAndTime[1]
        item.append(str_comment)
        item.append(str_time)

        # 获取作者
        regex_author = """<div><a href="/user/.*"\starget="_blank">(.*)</a>"""
        p_author = re.compile(regex_author)
        res_author = p_author.findall(res_divComment[i])
        str_author = res_author[0]
        item.append(str_author)

        item_list.append(item)
    return item_list;

def getItemHTMLListWithPage(cur_page):
    # 请求数据，设置代理
    proxy = urllib2.ProxyHandler({'http': '60.207.228.235:80'})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)

    get_url = url_tpl + str(cur_page * 5)
    ckjar = cookielib.LWPCookieJar(cookiePath)
    ckjar.load(ignore_discard=True,ignore_expires=True)  # 又漏了这句
    ckproc = urllib2.HTTPCookieProcessor(ckjar)
    openner = urllib2.build_opener(ckproc)
    req = urllib2.Request(get_url,None,headers)
    f_data = openner.open(req)
    responseData = f_data.read()

    # 匹配每一个点评DIV
    regex_divComment = """<div class="poster-grid2">([\s\S]*?)</span>\r\n\s*</div>\r\n\s*</div>"""
    p_divComment = re.compile(regex_divComment)
    res_divComment = p_divComment.findall(responseData)

    # 需要输入验证码
    if len(res_divComment) == 0:
        print 'http://www.yododo.com/common/verify_code.jsp?big=1'


    return res_divComment

def printList(aList):
    for i in range(0,len(aList)):
        print aList[0][i] + " "
        print "\n"

def pageGrab(page):
    res_divComment = getItemHTMLListWithPage(page)
    page_item_list = pushItemWithOriginList(res_divComment)
    # 插入数据库

    # # 返回数据
    # return page_item_list

def beginWithStartAndEnd(start,end):
    for i in range(start,end+1):
        pageGrab(i)
        threading._sleep(random.random * 3)


# 多线程队列
# class MultiThreadGrap(threading.Thread):
#     def __init__(self,queue):
#         threading.Thread.__init__(self)
#         self.queue = queue
#
#     def run(self):
#         while True:
#             host = self.queue.get()
#
#             self.queue.task_done()


# 创建多线程
# threadNum = 5
# totalPage = 1032
# spilt = totalPage / threadNum
# for t in range(0,threadNum):
#     if t == threadNum - 1:
#         thread.start_new_thread(beginWithStartAndEnd(t * spilt,t*spilt + (totalPage - t*spilt)),"启动线程")
#         print "Page : " + str(t * spilt) + " - " + str(t*spilt + (totalPage - t*spilt))
#     else:
#         thread.start_new_thread(beginWithStartAndEnd(t * spilt,(t+1) * spilt - 1),"启动线程")
#         print "Page : " + str(t * spilt) + " - " + str((t+1) * spilt - 1)

beginWithStartAndEnd(0,50)
