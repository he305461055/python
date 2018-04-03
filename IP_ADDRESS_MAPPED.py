import requests
import sys
import pymysql.cursors
from warnings import filterwarnings

####更改打印级别，保证警告级别不打印出来 如果不加mysql的waring基本会打印出来
filterwarnings('ignore', category = pymysql.Warning)

def multipleRows(params):
    ret = []
    # 根据不同值类型分别进行sql语法拼装
    for param in params:
        if isinstance(param, (int,float, bool)):
            ret.append(str(param))
        elif isinstance(param, (str, 'utf-8')):
            ret.append('"' + param + '"')
        else:
            print('unsupport value: %s ' % param)
    return '(' + ','.join(ret) + ')'

def query(sql,datas):
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'db': 'spiders',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，进行查询
            # sql = "INSERT INTO mtable(field1, field2, field3...) VALUES (%s, %s, %s...)"
            if datas!='':
                # 批量插入
                sql = "%s VALUES %s" %( sql,multipleRows(datas))
                print(sql)
                cursor.execute(sql)
                #connection.commit()
                # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                connection.commit()
            else:
                print(sql)
                cursor.execute(sql)
                # 获取查询结果
                result = cursor.fetchall()
                return result

    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        connection.close();

def checkip(ip):
    #payload = {'qcip': 'value1', 'key2': 'value2'}
    #URL = 'http://api.map.baidu.com/highacciploc/v1'
    detail_ip=[]

    sql='select formatted_address from ip_address_mapped where ip="%s"' %ip
    result=query(sql,'')
    if result==():
        try:
           # r = requests.get(URL, params=ip, timeout=30)
            r = requests.get( 'http://api.map.baidu.com/highacciploc/v1?qcip=%s&qterm=pc&ak=Y98gYzEPtSNETD23QDZUm4NqSLqibYxl&extensions=3&coord=bd09ll' %ip,timeout=30)
        except requests.RequestException as e:
            print(e)
        else:
            json_data = r.json()
            if json_data[u'result'][u'error'] =='161':
                detail_ip.append(ip)
                print('纬度：' + str(json_data[u'content'][u'location'][u'lat']))
                detail_ip.append(str(json_data[u'content'][u'location'][u'lat']))
                print('经度：' + str(json_data[u'content'][u'location'][u'lng']))
                detail_ip.append(str(json_data[u'content'][u'location'][u'lng']))
                print('结构化地址信息： ' + str(json_data[u'content'][u'formatted_address']))
                detail_ip.append(str(json_data[u'content'][u'formatted_address']))
                print('位置描述信息：' + str(json_data[u'content'][u'location_description']))
                detail_ip.append(str(json_data[u'content'][u'location_description']))
                print('所在国家： ' + str(json_data[u'content'][u'address_component'][u'country']) )
                detail_ip.append(str(json_data[u'content'][u'address_component'][u'country']))
                print('所在省份： ' + str(json_data[u'content'][u'address_component'][u'province']))
                detail_ip.append(str(json_data[u'content'][u'address_component'][u'province']))
                print('所在城市： ' + str(json_data[u'content'][u'address_component'][u'city']))
                detail_ip.append(str(json_data[u'content'][u'address_component'][u'city']))
                print('所在区县： ' + str(json_data[u'content'][u'address_component'][u'district']))
                detail_ip.append(str(json_data[u'content'][u'address_component'][u'district']))
                print('所在街道： ' + str(json_data[u'content'][u'address_component'][u'street']))
                detail_ip.append(str(json_data[u'content'][u'address_component'][u'street']))
                print('所在门牌号： ' + str(json_data[u'content'][u'address_component'][u'street_number']))
                detail_ip.append(str(json_data[u'content'][u'address_component'][u'street_number']))
                print('所在行政区划代码： ' + str(json_data[u'content'][u'address_component'][u'admin_area_code']))
                detail_ip.append(str(json_data[u'content'][u'address_component'][u'admin_area_code']))
                detail_ip.append('百度精确查找')
                print(detail_ip)

                sql='insert into ip_address_mapped(ip,lat,lng,formatted_address,location_description,country,province,city,district,street,street_number,admin_area_code,source)'
                query(sql,detail_ip)

                #print('所在商圈：' + str(json_data[u'content'][u'business']))
                print('#####################################周边信息：')
                for i in json_data[u'content'][u'pois']:
                    pois = []
                    pois.append(ip)
                    print('名称：' + str(i[u'name']))
                    pois.append(str(i[u'name']))
                    print('地址：' + str(i[u'address']))
                    pois.append(str(i[u'address']))
                    print('分类：' + str(i[u'tag']))
                    pois.append(str(i[u'tag']))
                    print('纬度：' + str(i[u'location'][u'lat']))
                    pois.append(str(i[u'location'][u'lat']))
                    print('经度：' + str(i[u'location'][u'lng']))
                    pois.append(str(i[u'location'][u'lng']))
                    pois.append('百度精确查找')

                    sql = 'insert into pois(ip,name,address,tag,lat,lng,source)'
                    query(sql, pois)

                #print('所在省份： ' + str(json_data[u'data'][u'region']))
                #print( '所在城市： ' + str(json_data[u'data'][u'city']))
                #print('所属运营商：' + str(json_data[u'data'][u'isp']))
            else:
                print('百度精确查找查询失败,查询纯真数据库！')
                sql="SELECT * FROM ipregion_mapped WHERE '%s'>INET_ATON(ip1) AND '%s'<INET_ATON(ip2)" %(str(ip),str(ip))
                result=query(sql,'')
                for i in result:
                    print('%s  %s' %(str(i[u'city']),str(i[u'location_description'])))
    else:
        print('查询到结果')
        for i in result:
           print(i['formatted_address'])
#sum=len(open('C:/Users/Administrator/Desktop/DZDP_BASIC/dzdp_success_list.txt').readlines())
#print('成功数：%s' %sum)
ip = '1.0.0.3'
#checkip(ip)
#r = requests.get( 'http://api.map.baidu.com/geoconv/v1/?coords=104.06467,30.56652&from=3&to=5&ak=6VIf8p9LCeQW9vm7kA8ll8afVSAZgEDn',timeout=30)
#r = requests.get( 'http://api.map.baidu.com/geoconv/v1/?coords=114.21892734521,29.575429778924;114.21892734521,29.575429778924&from=1&to=5&ak=6VIf8p9LCeQW9vm7kA8ll8afVSAZgEDn')
def checkaddress(address):
    r = requests.get('http://api.map.baidu.com/geocoder?output=json&address=%s' %address)
    json_data=r.json()
    if json_data[u'status'] =='OK':
        try:
            lng=json_data[u'result'][u'location'][u'lng']
            lat=json_data[u'result'][u'location'][u'lat']
            data='%s{%s{%s'%(address,lng,lat)
        except:
            data = '%s{%s{%s' % (address, '', '')
        with open('C:/Users/Administrator/Desktop/经纬度.txt', 'a', encoding='utf-8') as f:
            f.write(data)
            f.write('\n')

#r = requests.get('http://api.map.baidu.com/geocoder?output=json&address=%s' % '成都高新区奥克斯广场C座1702')
#print(r.json())
#with open('C:/Users/Administrator/Desktop/地址.txt', 'r', encoding='utf-8') as f:
#    for line in f:
#        checkaddress(line.replace('\n','').replace(' ',''))
import numpy as np
from  collections import defaultdict

dataset_filename = "F:/学习文档/数据挖掘/python数据挖掘入门与实战以及配套代码/python数据挖掘入门与实战配套代码/Code_REWRITE/Chapter 1/affinity_dataset.txt"
X = np.loadtxt(dataset_filename)
n_samples, n_features = X.shape
print(X.shape)
print("This dataset has {0} samples and {1} features".format(n_samples, n_features))

valid_rules = defaultdict(int)
invalid_rules = defaultdict(int)
num_occurances = defaultdict(int)
for sample in X:
    for premise in range(4):
        if sample[premise] == 0:
            continue
        num_occurances[premise] +=1
        print(n_features)
        for conclusion in range(n_features):

                if premise == conclusion:
                    continue
        if sample[conclusion] == 1:
            valid_rules[(premise,conclusion)] +=1
        else:
            invalid_rules[(premise,conclusion)] +=1
support = valid_rules
confidence = defaultdict(float)
for premise,conclusion in valid_rules.keys():
    rule = (premise,conclusion)
    confidence[rule] = valid_rules[rule]/conclusion[premise]
def print_rule(premise,conclusion,support,confidence,features):
    premise_name = features[premise]
    conclusion_name = features[conclusion]
    print("Rule : If a person buys {0} they will also buy {1}".format(premise_name,conclusion_name))
    print("- Support: {0}".format(support[(premise,conclusion)]))
    print("- Confidence:{0:.3f}".format(confidence[(premise,conclusion)]))