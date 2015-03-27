# encoding:utf-8
__author__ = 'zhijieli'
import urllib2,cookielib,re
import pymysql,threading
import xlwt


url_tpl = "http://www.yododo.com/search/searches.ydd?t=review&keyword=%E6%B7%B1%E5%9C%B3&page="
cookiePath = "cookie.txt"
saveDataPath = "shenzhen.xls"


# 获取总页数
total_page = "1"
first_page_url = url_tpl + "1"
headers={
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
    'Host':'www.yododo.com',
    'Connection':'keep-alive'
         }

# 获取评论
def getCommnet(link):
    req = urllib2.Request(link,None,headers)

    ckjar = cookielib.MozillaCookieJar(cookiePath)

    ckproc = urllib2.HTTPCookieProcessor(ckjar)
    opener = urllib2.build_opener(ckproc)

    f = opener.open(req)
    responeData = f.read()

    regex = """<div class="entryText">([\s\S]*?)</div>"""
    p = re.compile(regex)
    res = p.findall(responeData)
    return res[0]

# 获取连接
def getLink(single_html):
    regex_list4 = """<div class="list4">([\s\S]*?)</div>"""
    p_list4 = re.compile(regex_list4)
    res_list4 = p_list4.findall(single_html)
    # -----
    regex_link_tmp = '<a href="(.*?)"'
    p_link_tmp = re.compile(regex_link_tmp)
    res_link_tmp = p_link_tmp.findall(res_list4[0])
    return res_link_tmp[0]

# 获取发布时间
def getPostTime(single_html):
    regex_time = '<font color="#888888">&nbsp;(.{10})</font>'
    p_time = re.compile(regex_time)
    res_time = p_time.findall(single_html)
    return res_time[0]


# 根据返回的数据获取详细每条的数据
def getItem(html):
    res = []
    regex_item = """<li class="mb30 nopic">([\s\S]*?)</li>"""
    p_item = re.compile(regex_item)
    res_item = p_item.findall(html)
    for i in range(0,len(res_item)):
        item = []
        single_item = res_item[i]
        # addres
        regex_addres = """<font color='red'>(.*)</font>"""
        p_address = re.compile(regex_addres)
        res_address_tmp = p_address.findall(single_item)
        res_address = ''
        if len(res_address_tmp)>0:
            res_address = res_address_tmp[0]

        # author
        regex_author = """作者：<a href="#" target="_blank">(.*)</a>"""
        p_author = re.compile(regex_author)
        res_author_tmp = p_author.findall(single_item)
        res_author = res_author_tmp[0]

        # evaluate
        regex_evaluate = """<span class="review-(.{1})">"""
        p_evaluate = re.compile(regex_evaluate)
        res_evaluate_tmp = p_evaluate.findall(single_item)
        res_evaluate = ''
        if len(res_evaluate_tmp) == 0:
            res_evaluate = "0"  # 没有评价
        elif res_evaluate_tmp[0] == 'g':
            res_evaluate = "3"  # 好评
        elif res_evaluate_tmp[0] == 'm':
            res_evaluate = "2"  # 中评
        elif res_evaluate_tmp[0] == 'b':
            res_evaluate = "1"  # 差评

        # link
        res_link = getLink(single_item)

        #comment
        res_comment = ''
        try:
            res_comment = getCommnet(res_link)
        except:
            regex_tmp_comment = """<span class="partialDisplay">(.*)</span>"""
            p_tmp_comment = re.compile(regex_tmp_comment)
            res_tmp_comment = p_tmp_comment.findall(single_item)
            res_comment = res_tmp_comment[0]


        # posttime
        res_posttime = getPostTime(single_item)

        item.append(res_address)
        item.append(res_author)
        item.append(res_evaluate)
        item.append(res_comment)
        item.append(res_link)
        item.append(res_posttime)

        res.append(item)

    return res

# 插入数据库，有问题，有特殊字符
def insertDataInDB(resdata):

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd=None, db='DCrawer')
    cur = conn.cursor()

    for i in range(0,len(resdata)):
        item = resdata[i]
        address = item[0]
        author = item[1]
        evaluate = item[2]
        comment = item[3]
        link = item[4]
        posttime = item[5]

        sql = 'INSERT INTO d_detail(d_address,d_author,d_evaluate,d_comment,d_link,d_posttime)VALUES(?,?,?,?,?,?)'
        print sql
        cur.execute(sql,("1","1","1","1","1","1"))
    cur.close()
    conn.close()

def insertDataInXLS(resdata):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('深圳旅游情况'.decode('UTF-8'))
    sheet.write(0,0,"城市".decode('UTF-8'))
    sheet.write(0,1,"发布者".decode('UTF-8'))
    sheet.write(0,2,"评价".decode('UTF-8'))
    sheet.write(0,3,"详细评论".decode('UTF-8'))
    sheet.write(0,4,"详细评论链接".decode('UTF-8'))
    sheet.write(0,5,"发布时间".decode('UTF-8'))
    for i in range(0,len(resdata)):
        item = resdata[i]
        address = item[0].decode('UTF-8')
        author = item[1].decode('UTF-8')
        evaluate = item[2].decode('UTF-8')
        comment = item[3].decode('UTF-8')
        link = item[4].decode('UTF-8')
        posttime = item[5].decode('UTF-8')
        sheet.write(i+1,0,address)
        sheet.write(i+1,1,author)
        sheet.write(i+1,2,evaluate)
        sheet.write(i+1,3,comment)
        sheet.write(i+1,4,link)
        sheet.write(i+1,5,posttime)

    wbk.save(saveDataPath)

# 网络 - 首页
req = urllib2.Request(first_page_url,None,headers)
ckjar = cookielib.MozillaCookieJar(cookiePath)
ckjar.load(ignore_discard=True,ignore_expires=True)
ckproc = urllib2.HTTPCookieProcessor(ckjar)
opener = urllib2.build_opener(ckproc)
f = opener.open(req)
responeData = f.read()

# # 文件
# f = open("pageData.txt",'r')
# responeData = f.read()
# f.close()


# --------------
regex = r"pages\((\d{1,5})"
p = re.compile(regex)
res = p.findall(responeData)
total_page = res[0]


# 测试
# pagedata = getItem(responeData)
# insertDataInXLS(pagedata)


# 抓取数据
allPages = int(total_page)+1
pagedata = []
for i in range(1,allPages):
    url = url_tpl + str(i)
    req = urllib2.Request(url,None,headers)
    ckjar = cookielib.MozillaCookieJar(cookiePath)
    ckjar.load(ignore_discard=True,ignore_expires=True)
    ckproc = urllib2.HTTPCookieProcessor(ckjar)
    opener = urllib2.build_opener(ckproc)

    f = opener.open(req)
    responeData = f.read()
    pagedata = pagedata + getItem(responeData)
    print i
    threading._sleep(3.0)
insertDataInXLS(pagedata)
