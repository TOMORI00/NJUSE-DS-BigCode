#此文件用于对题目文本六角度分析的结果进行可视化处理与分析

#源数据文件格式
#问题编号 文学性得分 专业性得分 二次元度得分 口语化程度得分 难度得分 受欢迎度得分

#输出目标
#问题的六芒星均值
#例子问题的六芒星图
#问题的六性分布与均分
#六性间相关性分析

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

#读csv
csv_file = 'results/leetcode_result.csv'
csv_data = pd.read_csv(csv_file, low_memory=False)
data = pd.DataFrame(csv_data)
csv_fileq = 'results/question.csv'
csv_dataq = pd.read_csv(csv_fileq, low_memory=False)
dataq = pd.DataFrame(csv_dataq)

#绘制某组数据的六角度雷达图
def result_pic(result):
    """
    雷达图的绘制
    :param result: 分类数据
    :return: 雷达图
    """
    labels = ['lite_score', 'sch_score', 'd2_score', 'oral_score', 'diffculty', 'popularity']
    kinds = list(result.iloc[:, 0])
    result = pd.concat([result, result[['lite_score']]], axis=1)
    centers = np.array(result.iloc[:, 1:])
    n = len(labels)
    angle = np.linspace(0, 2 * np.pi, n, endpoint=False)
    angle = np.concatenate((angle, [angle[0]]))
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    for i in range(len(kinds)):
        ax.plot(angle, centers[i], linewidth=2, label=kinds[i])
    ax.set_thetagrids(angle * 180 / np.pi, labels)
    plt.title('distribution of case')
    plt.show()

#某性分布与均分
def distri(type):
    print('性质类型：'+type)
    print(data[type])
# 使用前200项数据，方便作图与查看分析
    data[type][0:200].plot(kind='line',title=type)
    plt.axhline(y=data[type][0:200].mean(),color="green")
    plt.legend(loc='best')
    plt.show()

#绘制所有题目的六角度分数分布叠合图
result_pic(data)

#计算六角度均分
print(data.mean())

# 下面为leetcode所有题目的六角度得分的均分
# questionId          /
# lite_score      0.197817
# sch_score       0.766502
# d2_score        0.341472
# oral_score      0.266059
# diffculty       0.546679
# popularity      0.485128
# dtype: float64

#绘制所有题目六角度均分的雷达图
result_pic(pd.DataFrame({
    'questionId':[-1], # 无意义
    'lite_score':[0.197817],
    'sch_score':[0.766502],
    'd2_score':[0.341472],
    'oral_score':[0.266059],
    'diffculty':[0.546679],
    'popularity':[0.485128]
}))

#选择一道题目作为例子进行分析（此处为leetcode的第121道题目）
print('\n题目文本:\n'+dataq.loc[120,:]['translatedContent'])
print('\n本题的做题情况:')
print(dataq.loc[120,:])
print('\n模型结果:')
print(data.loc[120,:])
#绘制本题的六角度得分的雷达图
result_pic(pd.DataFrame({
    'questionId':[3.000000],
    'lite_score':[0.136364],
    'sch_score':[0.863636],
    'd2_score':[0.409091],
    'oral_score':[0.272727],
    'diffculty':[0.542878],
    'popularity':[0.444247]
}))

# 绘制leetcode前200道题各个角度得分的分布与均分
# 竖直方向可以进行比较的形式
data[0:200].plot(subplots=True, figsize=(6, 6)); plt.legend(loc='best')
plt.show()
# 每一个角度单列并展示均分线的形式
distri('lite_score')
distri('sch_score')
distri('d2_score')
distri('oral_score')
distri('diffculty')
distri('popularity')

# 探究题目难度得分与文本风格四角度得分的相关性，绘制热力图
f, ax= plt.subplots(figsize = (14, 10))
sns.heatmap(data[['lite_score','sch_score','d2_score','oral_score','diffculty']].corr(),cmap='RdBu', linewidths = 0.05, ax = ax)
ax.set_title('Correlation between features')
plt.show()

# 探究实测难度得分与模型所得六个角度分数的相关性，绘制热力图
dataa = data[['lite_score','sch_score','d2_score','oral_score']].join(dataq['acRate'].str.strip("%").astype(float)/100)
f, ax= plt.subplots(figsize = (14, 10))
sns.heatmap(dataa.corr(),cmap='RdBu', linewidths = 0.05, ax = ax)
ax.set_title('Correlation between features')
plt.show()

# 探究模型难度得分与实测难度的相关性，绘制散点图
datab = data[['diffculty']].join(dataq['acRate'].str.strip("%").astype(float)/100)
plt.scatter(datab['diffculty'], datab['acRate'])
plt.xlabel('diffculty')
plt.ylabel('acRate')
plt.show()

# 探究模型六角度得分的相关性与特征，绘制散点图矩阵
pd.plotting.scatter_matrix(data[['lite_score','sch_score','d2_score','oral_score','diffculty','popularity']],figsize=(8,8),#注意Pandas中的用法与之前不同
                  c = 'k',
                 marker = '+',
                 diagonal='hist',
                 alpha = 0.8,
                 range_padding=0.1)
plt.show()
