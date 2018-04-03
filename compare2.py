# -*- coding: utf-8 -*-

import os
import difflib
import codecs
import re

file1 = open('C:/Users/Administrator/Desktop/ywy.txt',encoding='utf-8')
#file2 = open('F:\\compare\\spider1.txt',encoding='utf-8')
file2 = open('C:/Users/Administrator/Desktop/shop_detail.txt',encoding='utf-8')
lines1 = file1.readlines()
lines2 = file2.readlines()
list_ratio_end=[]
list_number=[] #计算匹配的上的个数 0.5

count3=0
count4=0
count5=0

for line1 in lines1:
    list_ratio=[]
    for line2 in lines2:
        seq = difflib.SequenceMatcher(None, line1.split('[}')[2].replace('\n',''),line2.split('[}')[6].replace('\n','')  )#ywy的每一行跟爬取的第一行比较
        ratio = seq.ratio()
        list_ratio.append(round(ratio,4))
        #list_ratio.append(ratio)
    #print (list_ratio)
    #print (len(list_ratio)) #长度为：2057
    #print (max(list_ratio)) #返回最大值
    if max(list_ratio)>0.5:
        count5=count5+1
    if max(list_ratio)>0.3:
        count3=count3+1
    if max(list_ratio)>0.4:
        count4=count4+1
    list_ratio_end.append(list_ratio.index(max(list_ratio)))
    #print (list_ratio.index(max(list_ratio))) # 返回最大值的下标
    #print (list_ratio[list_ratio.index(max(list_ratio))])
#print('count3',count3) #1193
#print('count4',count4) #1071
#print('count5',count5) #880
#大约需要5分钟
list_ratio_end_1=[]
list_ratio_end_1= [i+1 for i in list_ratio_end]
print (list_ratio_end_1)
#在数据保存出来
#file=open('F:\\compare\\data.txt','w')
#file.write(str(list_ratio_end_1))
#file.close()

#根据 list_ratio_end 取出地址的值

list_addr=[]
#print(lines1[690]) #锦江区点将台东街89号上行汇锦
#for i in range(len(list_ratio_end)):
for i in range(len(lines2)):
    list_addr.append(lines2[list_ratio_end[i]])
print(list_addr)

#把序号 list_ratio_end_1 和地址 list_addr 
list_end_addr=[]
from itertools import chain
list_end_addr=list(chain.from_iterable(zip(list_ratio_end_1,list_addr)))
print(list_end_addr)
#print(list_end_addr[0],list_end_addr[1])
#692 锦江区点将台东街89号上行汇锦
#print(list_end_addr[2],list_end_addr[3])
#393 天府二街1206号

for i in range(1,len(list_end_addr)+1):
	if i%2 !=0: #取奇数
		str1=str(list_end_addr[i-1])
		str2=str(list_end_addr[i])
		print(str1+' '+str2)

#每取两行换一次行
'''
file=open('F:\\compare\\data_end1.txt','w')
for i in range(1,len(list_end_addr)+1):
	if i%2 !=0: #取奇数
		str1=str(list_end_addr[i-1])
		str2=str(list_end_addr[i])
		file.write(str1+' '+str2)
		str1=''
		str2=''
file.close()
'''
