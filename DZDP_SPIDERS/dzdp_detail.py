import DZDP_SPIDERS.dzdp_detail_spiders as dz_spiders
from selenium import webdriver
import os
web_address=[]
'''
#dz_spiders.GET_FILE('dzdp', 'food_basic_list', 'null',2)
#dz_spiders.GET_FILE('dzdp', 'detail_address', 'null',2)
#dz_spiders.GET_FILE('dzdp', 'food_detail', 'null',2)
dz_spiders.GET_FILE('dzdp', 'food_user_content', 'null',2)
dz_spiders.GET_FILE('dzdp', 'success_list', 'null',2)
dz_spiders.GET_FILE('dzdp', 'intelligence', 'null',2)
'''
#driver.get('http://www.dianping.com/shop/531142')
'''
#dz_spiders.SHOP_DETAILS_INFO_1('dzdp', 'food_detail','http://www.dianping.com/shop/68041635')
sum=len(open('C:/Users/Administrator/Desktop/DZDP_BASIC/dzdp_success_list.txt').readlines())
print('成功数：%s' %sum)

filename='dzdp_detail_address'
for i in range(0,52):
  file='C:/Users/Administrator/Desktop/DZDP_BASIC/%s_%d.txt' %(filename,i)
  with open(file, 'r',encoding='utf-8') as f:
        for line in f:
           web_address.append(line.split('[}')[0])

web_address=list(set(web_address))
print(len(web_address))
sum=len(open('C:/Users/Administrator/Desktop/DZDP_BASIC/dzdp_success_list.txt').readlines())
while sum<len(web_address):
    for i in web_address:
        url='http://www.dianping.com' + str(i)
        web_success = []
        with open('C:/Users/Administrator/Desktop/DZDP_BASIC/dzdp_success_list.txt', 'r') as f:
            for line in f:
                web_success.append(line.replace('\n',''))
        if url not in web_success:
            try:
                dz_spiders.SHOP_DETAILS_INFO_1('dzdp', 'food_detail',url)
                print('成功')
                with open('C:/Users/Administrator/Desktop/DZDP_BASIC/dzdp_success_list.txt', 'a') as f:
                        f.write(url)
                        f.write('\n')
                dz_spiders.GET_LOG('dzdp_deatail', '%s:%s' % (url, '成功'))
            except Exception as e:
                print(url)
                print(e)
                dz_spiders.GET_LOG('dzdp_deatail','[ERROR:::::::::]%s:%s' %(url,str(e)))
                continue
    sum=len(open('C:/Users/Administrator/Desktop/DZDP_BASIC/dzdp_success_list.txt').readlines())
    print('成功数：%s' %sum)
'''
#profile_dir=r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
#chrome_options=webdriver.ChromeOptions()
#chrome_options.add_argument("user-data-dir="+os.path.abspath(profile_dir))
#driver=webdriver.Chrome(chrome_options=chrome_options)
#driver.maximize_window()
#driver = webdriver.Chrome()
#driver.get('http://www.dianping.com/shop/531142')

#dz_spiders.GET_DETAIL_HTML( 'http://www.dianping.com/shop/68117774')
chrome_driver = os.path.abspath("C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.31.exe")
os.environ["webdriver.chrome.driver"] = chrome_driver
driver = webdriver.Chrome(chrome_driver)
driver.get('http://www.dianping.com/citylist')

with open('C:/Users/Administrator/Desktop/shop_detail.txt', 'r',encoding='utf-8') as f:
    for line in f:
        web_address.append(line.split('[}')[0].replace('\n', ''))

with open('C:/Users/Administrator/Desktop/daipaqu_1.txt', 'r', encoding='utf-8') as f:
    for line in f:
        url=line.split('[}')[1].replace('\n', '')
        if url.split('/')[-1] not in web_address:
            try:
                dz_spiders.GET_DETAIL_HTML( driver,url)
            except Exception as e:
                print(url)
                print(e)
                continue
