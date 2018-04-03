import time
import sys
import pymysql.cursors

#分词算法
def max_match_segment(line, dic):
    # write your code here
    chars = line
    length=len(chars)
    words = []
    tempwords = []
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
    if len(tempwords)>0:
        words.append(''.join(tempwords))
    return words

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
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，进行查询
            # sql = "INSERT INTO mtable(field1, field2, field3...) VALUES (%s, %s, %s...)"
            if condition=='':
              query_sql = "%s" % sql
            else:
              query_sql = "%s and %s" % (sql, condition)
            print(query_sql)
            cursor.execute(query_sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        connection.close();

def insert(sql,data):
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，进行查询

            # sql = "INSERT INTO mtable(field1, field2, field3...) VALUES (%s, %s, %s...)"
            for item in datas:
            #batch_list.append(multipleRows(temp))
            # 批量插入
            # if len(batch_list) ==2:
                query_sql = "%s VALUES %s" %( sql,data)
                print(query_sql)
                try:
                 cursor.execute(query_sql)
                except:
                    print('特殊处理')
                    with open('C:/Users/Administrator/Desktop/2.txt', 'a', encoding='utf-8') as f:
                        f.write(query_sql)
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

config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'root',
          'db':'spiders',
          'charset':'utf8',
          'cursorclass':pymysql.cursors.DictCursor,
          }
connection = pymysql.connect(**config)
counts=0
batch_list=[]
china=[]
window_size = 15
dic=['东京']
str=u'东京I2Ts Inc'
print(max_match_segment(str, dic))
sql='select name from china_tree where level=7 and LEVEL =5'
result=query(sql,'')
for i in result:
    china.append(i['name'])

sql='insert into ipregion_mapped(ip1,ip2,city,location_description,source)'
#insert(sql,datas)