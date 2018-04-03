import time
import sys
import pymysql
pymysql.install_as_MySQLdb()
#分词算法
def max_match_segment(line, dic):
    # write your code here
    chars = line
    length=len(chars)
    words = []
    tempwords = []
    other=''
    idx = 0
    while idx < length:
        matched = False
        for i in range(window_size, 0, -1):
            cand = chars[idx:idx + i]
            if cand in dic:
                words.append(cand)
                matched = True
                break
        if not matched:
            i = 1
            tempwords.append(chars[idx])
        idx += i
    if len(tempwords) > 0:
        other=''.join(tempwords)
    return words,matched,other

# 返回可用于multiple rows的sql拼装值
def multipleRows(params):
    ret = []
    # 根据不同值类型分别进行sql语法拼装
    for param in params:
        if isinstance(param, (int,  float, bool)):
            ret.append(str(param))
        elif isinstance(param, (str, 'utf-8')):
            if "'" in param:
               ret.append('"' + param + '"')
            else:
               ret.append( "'" + param + "'" )
        else:
            print('unsupport value: %s ' % param)
    return '(' + ','.join(ret) + ')'

def query(sql,condition):
        connection = pymysql.connect(**config)
        cursor=connection.cursor()
        #if condition=='':
        query_sql = "%s" % sql
        #else:
        #  query_sql = "%s and %s" % (sql, condition)
        print(query_sql)
        cursor.execute(query_sql)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result


def insert(sql,datas,dic1,dic2):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，进行查询
            # sql = "INSERT INTO mtable(field1, field2, field3...) VALUES (%s, %s, %s...)"
            for item in datas:
                batch_list =[' ',' ',' ',' ',' ',' ',' ']
                temp = []
                length=len(item.split())
                if length>3:
                    for k in range(3,length):
                        temp.append(item.split()[k])
                    str=''.join(temp)
                batch_list[0]=item.split()[0].replace('﻿', '')
                batch_list[1]=item.split()[1]
                word,matched,other=max_match_segment(item.split()[2], dic1)
                if len(word)>0 and length>3:
                    batch_list[2]='中国'
                    for i in word:
                        level_sql='select level from china_tree where name like "%s" ' %i
                        result=query(level_sql,'')
                        for j in result:
                            batch_list[int((int(j['level'])+1)/2)]=i
                    batch_list[6] = '%s%s' % (other, item.split()[3])
                elif length==3:
                    batch_list[2]=item.split()[2]
                elif len(word)==0  and length>3:
                    if len(other)>13:
                        batch_list[2]='中国'
                        batch_list[6]='%s %s' % (other, item.split()[3])
                    else:
                        batch_list[2]=item.split()[2]
                        batch_list[6]=str

                '''
                newword, nwematched = max_match_segment(str, dic2)
                if len(newword)>1:
                   batch_list.append(' ')
                   batch_list.append(newword[0])
                   batch_list.append(' ')
                   batch_list.append(newword[1])
                else:
                    batch_list.append(' ')
                    batch_list.append(' ')
                    batch_list.append(' ')
                    batch_list.append(str)
             '''
                batch_list.append('纯真')
                query_sql = "%s VALUES %s;" %( sql,multipleRows(batch_list))
                print(query_sql)
                try:
                 cursor.execute(query_sql)
                except Exception as e:
                    print(e)
                    print('特殊处理')
                    with open('C:/Users/Administrator/Desktop/2.txt', 'a', encoding='utf-8') as f:
                        f.write(query_sql)
                        f.write('\n')
                    continue
                #connection.commit()
                #batch_list = []
                # counts += len(batch_list)
                # print("inserted:" + str(counts))
                # temp=[(4),(5)]
                # cursor.executemany(sql,temp)
                # 获取查询结果
                # result = cursor.fetchall()
                # for i in result:
                #    print(i[u'Tables_in_spiders'])
        # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        connection.close();

datas=[]
#with open('C:/Users/Administrator/Desktop/1.txt','r',encoding='utf-8') as f:
with open('C:\\Users\\Administrator\\Desktop\\1.txt', 'r', encoding='utf-8') as f:
    for line in f:
        datas.append(line.replace('\n',''))
'''
for item in datas:
    length = len(item.split())
    if length==4:
        print(item)
        time.sleep(5)
'''
config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'db': 'spiders',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }

counts=0
batch_list=[]
China=[]
Global=[]
window_size = 15

sql='select name from china_tree'
result=query(sql,'')
for i in result:
    China.append(i['name'])
#'''
sql='select name from global_location'
result=query(sql,'')
for i in result:
    Global.append(str(i['name']).replace('\ufeff',''))
#'''
'''
with open('C:\\Users\\Administrator\\Desktop\\aa.txt', 'r', encoding='utf-8') as f:
    for line in f:
        Global.append(line.replace('\n','').replace('\ufeff',''))
'''

sql='insert into ipregion_mapped(ip1,ip2,country,province,city,district,location_description,source)'
insert(sql,datas,China,Global)

a=[' ',' ',' ',' ',' ',' ',' ',' ']
a[0]='sss'
print(a)
time.sleep(10)
print(China)
str=u'111'
aa,bb,cc=max_match_segment(str,China)
print(len(aa))