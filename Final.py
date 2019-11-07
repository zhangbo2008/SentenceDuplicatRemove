
#encoding:utf-8

'''
这个.py作为统一的最后接口

'''




#说明tfidf算法用main3参数,编辑距离用main4,杰卡德用main5

# 超参数都写这里!!!!!!!!
# 改变下行传入的参数即可:
selectMethod='main3'
yuzhi=0.6
pathb='database(1).txt'#库文件
pathq='query(1).txt'  # 插入文件
b_n=10#切割数量
q_n=10








from main3 import main3
from main4 import main4
from main5 import main5



if selectMethod=='main3':
    output=main3(yuzhi=yuzhi,
pathb=pathb, #库文件
pathq=pathq,  # 插入文件
b_n=b_n,#切割数量
q_n=q_n)
elif selectMethod=='main4':

    output = main4(yuzhi=yuzhi,
                   pathb=pathb,  # 库文件
                   pathq=pathq,  # 插入文件
                   b_n=b_n,  # 切割数量
                   q_n=q_n)
else:
    output = main5(yuzhi=yuzhi,
                   pathb=pathb,  # 库文件
                   pathq=pathq,  # 插入文件
                   b_n=b_n,  # 切割数量
                   q_n=q_n)

print(output[0],output[1])


'''
写入模块
'''

with open('result/baoliudex.txt','w') as f:
    f.write(str(output[0]))

with open('result/feichudex.txt','w') as f:
    f.write(str(output[1]))
import linecache
with open('result/baoliu.txt','w') as f, open(pathq,'r') as t:
    q = linecache.getlines(pathq)
    for i in range(len(q)):
        if i in output[0]:
            f.write(q[i])



with open('result/feichu.txt','w') as f, open(pathq,'r') as t:
    q = linecache.getlines(pathq)
    for i in range(len(q)):
        if i in output[1]:
            f.write(q[i])