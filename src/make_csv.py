# 此文件用于将解压后的200道题的题目文本生成csv文件用于分析

import os
import pandas

data = []
for file in os.listdir('TEST/buffer'):
    if(file.endswith('zip')):
        continue
    f = open('TEST/buffer/'+ file +'/readme.md', 'r',encoding='UTF-8')
    temp = {}
    temp['name'] = file[0:-7]
    content = f.read()
    content = "".join([s for s in content.splitlines(True) if s.strip()])
    temp['content'] = content
    data.append(temp)
    f.close()

dataFrame = pandas.DataFrame(data,columns=['name','content'])
print(dataFrame)
dataFrame.to_csv('test_text.csv',index=False,sep=',')
