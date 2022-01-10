# 此文件用于找出一位完成了200道题的人，下载他所做的所有题目文本用于分析

import json  
import requests
import urllib.request

# 打开json文件,此json文件为助教提供
# src='D:/WORK_SPACE/PYTHON/Test_For_Python/TEST/test_data.json',encoding='utf-8'

f =open(src)
res=f.read()
dict_ = json.loads(res)

theone_ = ''
for person in dict_.keys():
    if(len(dict_[person]['cases'])==200):
        theone = person
# print(theone)
# 49405号完成了200题
urls = []
for case in dict_[theone]['cases']:
    # print(case['case_zip'])
    urls.append(case['case_zip'])
for url in urls:
    response = requests.get(url, stream=True)
    with open( './TEST/buffer/'+url.split('/')[-1], 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

