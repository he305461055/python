import re
company_info='公司已经有五年历史'
regx=u'(\d{4}[\s\S]*成立|\d{1,3}年|[\s\S]{1,2}年)'
company_year=re.findall(regx,company_info)
print(company_year)