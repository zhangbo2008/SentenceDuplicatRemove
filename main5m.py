'''
在linux下才能跑多进程.

'''

#多进程,不能使用函数内部的函数!!!!!!!!!!
def op(s, q, kaishi, queue, yuzhi):  # 这个函数做一次切分操作
    from sklearn.feature_extraction.text import CountVectorizer
    import numpy as np

    def jaccard_similarity(s1, s2):
        def add_space(s):
            return ' '.join(list(s))

        # 将字中间加入空格
        s1, s2 = add_space(s1), add_space(s2)
        # 转化为TF矩阵
        cv = CountVectorizer(tokenizer=lambda s: s.split())
        corpus = [s1, s2]
        vectors = cv.fit_transform(corpus).toarray()
        # 求交集
        numerator = np.sum(np.min(vectors, axis=0))
        # 求并集
        denominator = np.sum(np.max(vectors, axis=0))
        # 计算杰卡德系数
        return 1.0 * numerator / denominator

    out = []
    import distance

    def edit_distance(s1, s2):
        return jaccard_similarity(s1, s2)

    s = q + s
    for i in range(len(q)):
        for j in range(i + 1, len(s)):

            tmp1 = edit_distance(q[i], s[j])
            if tmp1 > yuzhi:
                out.append(i + kaishi)
                break
    queue.put(out)
    return set(out)

##   jiekade算法实现.
# import distance
#
# def edit_distance(s1, s2):
#     return distance.levenshtein(s1, s2)
#
# tmp=edit_distance("鼠标称","鼠标称")

# print(tmp)

def main5m(yuzhi=0.6,
           pathb='database(1).txt',
           pathq='query(1).txt',
           b_n=10,  # 切割数量
           q_n=10,
           k=10):
    import os
    import multiprocessing
    import time

    # 根据编辑距离来算.

    # 大数据切割版代码!
    # coding=utf-8

    from tqdm import tqdm
    '''
    所有接口最后只有这个一个main
    函数

    '''
    import time
    start = time.time()

    '''
    输入参数介绍:
    shuru_database.txt 是输入的数据库,也就是被查询的库
    shuru_query.txt 是输入的查询,也就是要被插入数据库的新数据
    yuzhi 输入的阈值0到1之间.如果大于这个阈值就表示2个文本相似.
    直白的说,yuzhi越大那么去重越弱,填入数据库的新数据越多!

    '''
    # 超参数表!


    import os

    import shutil
    if os.path.exists('result'):
        shutil.rmtree('result')  # 删除文件夹用这个命令更牛逼,这个是强制删除
        os.mkdir('result')

    ##

    from gensim import corpora, models, similarities
    import logging
    from collections import defaultdict
    import jieba
    import time

    start = time.time()

    step = 1

    # --------------------------开始

    # 计算文件行数最快的方法,统计\n

    def hangshu(filepath):
        count = 0
        for index, line in enumerate(open(filepath, 'r', encoding='utf-8')):
            count += 1
        return count

    # print(hangshu(pathb))
    ##

    # pip3 install distance



    import numpy as np
    out1 = np.array([])
    out2 = np.array([])
    out = set()
    # 切割.hou yunsuan
    import linecache
    bhang = hangshu(pathb)
    qhang = hangshu(pathq)
    queue = multiprocessing.Manager().Queue()
    po = multiprocessing.Pool()
    import multiprocessing as mp

    baseshuju=open(pathb,encoding='utf-8').readlines()
    qshuju=open(pathq,encoding='utf-8').readlines()

    for i in tqdm(range(q_n)):
        delta = qhang // q_n
        if i != q_n - 1:
            q = qshuju[i * delta:(i + 1) * delta]
        else:
            q = qshuju[i * delta:]

        # 下面分析s的分块
        if i < q_n - 1:  # 这时候需要s跑遍查询q后面和s的全部
            for j in range(i + 1, q_n):
                if j != q_n - 1:
                    s = qshuju[j * delta:(j + 1) * delta]
                else:
                    s = qshuju[j * delta:]
                # print(type(s))
                # print(type(q))
                # print(type(queue))
                po.apply(op, args=(s, q, i * delta, queue,yuzhi,))

            delta2 = bhang // b_n
            for j in range(b_n):

                if j != b_n - 1:
                    s = baseshuju[j * delta2:(j + 1) * delta2]
                else:
                    s = baseshuju[j * delta2:]
                po.apply(op, args=(s, q, i * delta, queue,yuzhi,))

        if i == q_n - 1:
            delta2 = bhang // b_n
            for j in range(b_n):

                if j != b_n - 1:
                    s = baseshuju[j * delta2:(j + 1) * delta2]
                else:
                    s = baseshuju[j * delta2:]
                po.apply(op, args=(s, q, i * delta, queue,yuzhi,))

    po.close()
    po.join()

    out = set([])



    while queue.qsize()>0:
        a=queue.get()
        out=out.union(set(a))
        # print(out)
        # time.sleep(1)



    print("buyao的数据编号", out)

    out2 = set(range(qhang))
    out2 = out2 - out
    print("要的数据编号", out2)
    print("oooooooooooooooooo")
    return out, out2


