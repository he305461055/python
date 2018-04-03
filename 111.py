from bs4 import BeautifulSoup as bs
import urllib.request
import http.cookiejar
import base64
import re
import json
import hashlib
import rsa
import binascii
import time

import sys

pubkey = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
cj = http.cookiejar.LWPCookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
urllib.request.install_opener(opener)
postdata = {
    'entry': 'weibo',
    'gateway': '1',
    'from': '',
    'savestate': '7',
    'userticket': '1',
    'ssosimplelogin': '1',
    'vsnf': '1',
    # 'vsnval': '',
    'su': '',
    'service': 'miniblog',
    'servertime': '',
    'nonce': '',
    # 'pwencode': 'wsse',
    'pwencode': 'rsa2',
    'sp': '',
    'pagerefer': 'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
    'raskv': '',
    'sr': '1440*900',
    'prelt': '94',
    'encoding': 'UTF-8',
    'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype': 'META'
}


def get_servertime():
    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=dW5kZWZpbmVk&client=ssologin.js(v1.4.18)&_=%d'% int(time.time())
    data = urllib.request.urlopen(url).read()
    json_data = json.loads(re.search(r"\((?P<data>.*)\)",data).group("data"))
    try:
        servertime = str(json_data['servertime'])
        nonce = json_data['nonce']
        rsakv = json_data['rsakv']
        return servertime, nonce, rsakv
    except:
      print('Get severtime error!')
      return None


def get_pwd(pwd, servertime, nonce):
    # pwd1 = hashlib.sha1(pwd).hexdigest()#旧的加密方式，pwencode的值需要为wsse
    # pwd2 = hashlib.sha1(pwd1).hexdigest()
    # pwd3_ = pwd2 + servertime + nonce
    # pwd3 = hashlib.sha1(pwd3_).hexdigest()
    # return passwd
    global pubkey
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)  # 拼接明文js加密文件中得到
    passwd = rsa.encrypt(message, key)  # 加密
    passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
    print(passwd)
    return passwd


def get_user(username):
    username_ = urllib.request.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username


def login():
    username = '你的登录邮箱'
    pwd = '你的密码'
    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    try:
        servertime, nonce, rsakv = get_servertime()
    except:
        return
    global postdata
    postdata['servertime'] = servertime
    postdata['nonce'] = nonce
    postdata['rsakv'] = rsakv
    postdata['su'] = get_user(username)
    postdata['sp'] = get_pwd(pwd, servertime, nonce)
    for i in postdata:
        print(i, ":", postdata[i])  # 可以看提交的哪些数据
    # print postdata["su"]
    #    print postdata["sp"]
    postdata = urllib.request.urlencode(postdata)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
    req = urllib.request(
        url=url,
        data=postdata,
        headers=headers
    )
    result = urllib.request.urlopen(req)
    text = result.read()
    # print len(text)
    # print 30*"*"
    # print text
    # p = re.compile('location\.replace\'(.∗?)\'')#p = re.compile('location\.replace\'(.∗?)\'')
    p = re.compile('location\.replace\"(.∗?)\"')
    login_url = p.findall(text)[0]

    # login_url = p.search(text).group(1)
    print(login_url)
    print(30 * "*")
    try:
        result1 = urllib.request.urlopen(login_url).read()
        fres = open("fres.txt", "w")
        fres.write(result1)
        fres.close()
        #   print len(result1)
        #   print type(result1)
        print(u"登录成功!")  # 是否登录成功还要看result1的内容是否是别的什么，

        query = "深圳禁摩限电"
        page_num = 1
        url = "http://s.weibo.com/weibo/{0}&b=1&nodup=1&page={1}".format(query, page_num)
        # http://s.weibo.com/weibo/深圳禁摩限电&b=1&nodup=1&page=1
        # newurl = "http://baike.baidu.com"+suburl
        req = urllib.request.urlopen(url)
        html = req.read()
        # print html
        #        html = urllib.request.urlopen(url)
        #        req  = urllib.request.urlparse()
        # soup = bs(html)
        f_query1 = open("shenzhenlimitcar_sf.html", "w")
        f_query1.write(html)
        f_query1.close()
    except Exception as e:
        print('Login error!')
        print(e)

if __name__ == "__main__":
    login()