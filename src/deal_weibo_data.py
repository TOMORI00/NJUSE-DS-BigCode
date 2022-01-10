# coding=utf-8

import os

ROOTDIR = os.path.abspath(os.path.abspath(os.path.join(os.getcwd(), "..")))
DATADIR = os.path.join(ROOTDIR, 'data')

with open(DATADIR + '/weibo.txt',encoding = 'utf-8') as f:
    for i in range(10):
        with open(DATADIR + '/口语/' + str(i+1) + '.txt','a',encoding = 'utf-8') as f0:
            for j in range(25000):
                f0.write(f.readline()+'\n')