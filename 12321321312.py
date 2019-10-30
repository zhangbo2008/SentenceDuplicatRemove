##
#大数据切割版代码!
# coding=utf-8


'''
所有接口最后只有这个一个main
函数

'''
import time
start=time.time()

'''
输入参数介绍:
shuru_database.txt 是输入的数据库,也就是被查询的库
shuru_query.txt 是输入的查询,也就是要被插入数据库的新数据
yuzhi 输入的阈值0到1之间.如果大于这个阈值就表示2个文本相似.
直白的说,yuzhi越大那么去重越弱,填入数据库的新数据越多!

'''
#超参数表!
yuzhi=0.1
pathb='shuru_database.txt'
pathq='shuru_query.txt'
b_n=100#切割数量
q_n=100


import os

import shutil
if os.path.exists('result'):
    shutil.rmtree('result') #删除文件夹用这个命令更牛逼,这个是强制删除
    os.mkdir('result')



##





from gensim import corpora, models, similarities
import logging
from collections import defaultdict
import jieba
import time





start=time.time()

step=1




#--------------------------开始


#放入数据:
BAll = [i for i in open(pathb, encoding='utf-8').readlines()]

QAll = [i for i in open(pathq, encoding='utf-8').readlines()]




#计算文件行数最快的方法,统计\n

def hangshu(thefilepath):
    count = 0
    thefile = open(thefilepath, 'rb')
    print(thefile.read(213))
    print(str(thefile.read(213)).count('\n'))
    raise
    while True:
        buffer = str(thefile.read(8192*1024))
        print(buffer)
        if not buffer:
            break


        count += buffer.count('\n')
    thefile.close( )
    return count
print(hangshu(pathb))