import urllib.request
import os
import re

def get_page(url):
    pass

def find_imgs(url):
    pass

def save_imgs(folder,img_addrs):
    pass

def download_mm(folder='OOXX',pages=10):
    #os.mkdir(folder)
    #os.chdir(folder)
#找到首页图片
    req=urllib.request.Request('http://cd.meituan.com/category/meishi/all/rating?mtt=1.index%2Fdefault%2Fpoi.0.0.is8o3kw6')
    response = urllib.request.urlopen(req)
    html=response.read().decode('utf-8')
    #print(html)
    
    img_addrs = []
    a=html.find('img class="J-webp" src=')
    #while a !=-1:
    print(a)
    b=html.find('.jpg',a,a+70000000)
    img_addrs.append(html[a+24:b+4])


    for each in img_addrs:
        filename=each.split('/')[-1]
        print('图片名称  ：' +filename+'下载成功')

    req1= urllib.request.Request(html[a+24:b+4])
    response1 = urllib.request.urlopen(req1)
    img=response1.read()
    
    with open(filename,'wb') as f:
       f.write(img)

#找店铺消息
    req3=urllib.request.Request('http://cd.meituan.com/shop/60120047?acm=UwunyailsW7569197709646862729.60120047.1&mtt=1.index%2Fdefault%2Fpoi.pz.1.is9v3e3t&cks=23377#bdw')
    response3 = urllib.request.urlopen(req3)
    html3=response3.read().decode('utf-8')

    a6=html3.find('div data-component="bread-nav" class="component-bread-nav')
    b6=html3.find('</div>',a6,a6+2000)
    addr6=html3[a6+19:b6]
    gl=re.findall(r"(>.*</a)",addr6)
    print('店铺归属：  '+str(gl))

    a3=html3.find('span class="title"')
    b3=html3.find('</span',a3,a3+500)
    addr3=html3[a3+19:b3]
    print('店铺名称：  '+addr3)

    a4=html3.find('span class="geo"')
    b4=html3.find('</span',a4,a4+500)
    addr4=html3[a4+19:b4]
    print('店铺地址：  '+addr4)
    
    a5=html3.find('p class=under-title')
    b5=html3.find('</p>',a5,a5+500)
    addr5=html3[a5+20:b5]
    print('店铺电话号码：  '+addr5)
    #正则
    te15=re.findall(r"028-\d\d\d\d\d\d\d\d/\d\d\d\d\d\d\d\d",html3[a5:b5])
    print('店铺电话号码(用正则获取)：  '+str(te15))

    #获取评价
    a7=html3.find('div class="rate-detail" id=')
    b7=html3.find('</div>',a7,a7+5000)
    addr7=html3[a7+19:b7]
    pj1=re.findall(r"(味.*好)",html3)
    pj2=re.findall(r"(环.*)",html3)
    print('评价1：  '+str(pj1))
    print('评价2：  '+str(pj2))
    
if __name__=="__main__":
    download_mm()

