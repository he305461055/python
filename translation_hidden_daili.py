import urllib.request
import random

url='http://www.whatismyip.com.tw'

iplist = ['60.194.100.51:80','61.162.223.41:9797','61.174.10.22:8080']

proxy_support = urllib.request.ProxyHandler({'http':random.choice(iplist)})

opener = urllib.request.build_opener(proxy_support)

opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')]
urllib.request.install_opener(opener)

response=urllib.request.urlopen(url)
html=response.read().decode('utf-8')

print(html)

