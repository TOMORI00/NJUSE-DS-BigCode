#此文件用于获取慕测系统中同学们所做题目的每道题均分

import json
import pandas

# json文件来自助教
# src = 'D:/WORK_SPACE/PYTHON/Test_For_Python/TEST/test_data.json'
f = open(src,encoding='utf-8')
test_data = json.loads(f.read())

testList = []
i = 0
for person in test_data.keys():
    for cases in test_data[person]['cases']:
        if cases["case_id"] not in testList:
            testList.append(cases["case_id"])

print(len(test_data.keys())) # 输出总做题
print(len(testList)) # 输出总题目数

# 共271人
# 共882道不同的题目

# 输出每一道题的做题人数与均分
out = {}
outt = []
for id in testList:
    temp = []
    for person in test_data.keys():
        for cases in test_data[person]['cases']:
            if cases["case_id"]==id:
                temp.append(cases["final_score"])
    ans=0
    for i in temp:
        ans+=i
    ans = ans / len(temp)
    out[id] = '题目id: ' + id + ' 做题人数: ' + str(len(temp)) + " 均分: " + str(ans)
    outt.append(out[id])
dataFrame = pandas.DataFrame(outt)
print(dataFrame)
