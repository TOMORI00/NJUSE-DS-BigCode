#此文件用于解压所下载到的压缩包并保存在源路径文件夹下

import zipfile
import os
import shutil

def un_zip(file_name):
    """解压单个文件"""
    zip_file = zipfile.ZipFile(file_name)
    zip_file.extract(zip_file.namelist()[zip_file.namelist().index('readme.md')],file_name+"out")
    zip_file.close()
    print(file_name,'解压成功')

def un_zip_Tree(path):                        # 解压文件夹中的zip文件
    if not os.path.exists(path):               # 如果本地文件夹不存在，则创建它
        os.makedirs(path)
    for file in os.listdir(path):               #listdir()返回当前目录下清单列表
        Local = os.path.join(path, file)
        if os.path.isdir(file):  # 判断是否是文件
            if not os.path.exists(Local):           #对于文件夹：如果本地不存在，就创建该文件夹
                os.makedirs(Local)
            un_zip_Tree(path)
        else:  # 是文件
            if os.path.splitext(Local)[1] == '.zip':            #os.path.splitext(Remote)[1]获取文件扩展名，判断是否为.zip文件
                un_zip(Local)       #解压文件

un_zip_Tree('./TEST/buffer/')
