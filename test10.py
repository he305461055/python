'''
import json
import requests
import urllib.request
import re

prodata=[1,2,3]

r = requests.get("http://192.168.10.242:5000/v1.0/meituanshop?url,CBD")
mydata=r.text
print(mydata)
#aa=urllib.request.urlopen("http://192.168.10.242:5000/v1.0/meituanshop?url,CBD")
#print(aa.read())
for i in json.loads(mydata)["data"]:
    print(i['CBD'])

mypage = re.findall('"data":(.*?])}', mydata)
print(mypage)
'''

from PIL import Image,ImageEnhance,ImageFilter,ImageGrab
import pytesser3
import sys

im=Image.open('C:/Users/Administrator/Desktop/text/captcha (1).png')
print(im)
print(im.format)
print(im.size)
print(im.mode)
#im.show()
print(pytesser3.image_file_to_string('C:/Users/Administrator/Desktop/1.png'))

# 二值化

threshold = 140

table = []

for i in range(256):
    if i !=threshold:
        table.append(0)
    else:
        table.append(1)

rep = {'O': '0',
       'I': '1', 'L': '1',
       'Z': '2',
       'S': '8'
       };

def getverify1(name):
    # 打开图片
    im = Image.open(name)
    # 转化到灰度图
    imgry = im.convert('L')
    # 保存图像
    imgry.save('g' + name.split('/')[-1])
    # 二值化，采用阈值分割法，threshold为分割点
    out = imgry.point(table, '1')
    out.save('b' + name.split('/')[-1])
    # 识别
    text = pytesser3.image_to_string(out)
    # 识别对吗
    text = text.strip()
    text = text.upper();
    for r in rep:
        text = text.replace(r, rep[r])
        # out.save(text+'.jpg')
    print(text)
    return text

getverify1('C:/Users/Administrator/Desktop/1.png')