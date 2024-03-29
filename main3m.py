'''
在linux下才能跑多进程.

'''
import os
from gensim import corpora, models, similarities
import logging
from collections import defaultdict
import jieba
import time
import shutil
#多进程,不能使用函数内部的函数!!!!!!!!!!
def op(s, q, kaishi, queue,yuzhi):  # 这个函数做一次切分操作
    step=0
    # print('当前开始处理',step,'步奏')

    # 准备数据：现有8条文本数据，将8条文本数据放入到list中
    documentsb = s

    documentsq = q

    shujukushuliang = len(documentsb)
    chaxunshuliang = len(documentsq)
    documentAll = documentsb + documentsq

    ##
    # 待比较的文档

    # 获取停用词
    stopwords = set()
    file = open("stopwords.txt", 'r', encoding='UTF-8')
    for line in file:
        stopwords.add(line.strip())
    file.close()

    # 将分词、去停用词后的文本数据存储在list类型的texts中
    documentsb__after_preprocess = []  # 预处理之后的数据库记做documentsb__after_preprocess
    for line in documentAll:
        words = ' '.join(jieba.cut(line)).split(' ')  # 利用jieba工具进行中文分词
        text = []
        # 过滤停用词，只保留不属于停用词的词语
        for word in words:
            if word not in stopwords:
                text.append(word)
        documentsb__after_preprocess.append(text)
    ##

    # 待比较的文档也进行预处理（同上）
    documentsq__after_preprocess = []  # 预处理之后的数据库记做documentsb__after_preprocess
    for line in documentsq:
        words = ' '.join(jieba.cut(line)).split(' ')  # 利用jieba工具进行中文分词
        text = []
        # 过滤停用词，只保留不属于停用词的词语
        for word in words:
            if word not in stopwords:
                text.append(word)
        documentsq__after_preprocess.append(text)

    ##
    # 2.计算词频
    # print('2.计算词频')
    frequency = defaultdict(int)  # 构建一个字典对象
    # 遍历分词后的结果集，计算每个词出现的频率
    for text in documentsb__after_preprocess:
        for word in text:
            frequency[word] += 1
    # 选择频率大于1的词(根据实际需求确定)
    texts = [[word for word in text if frequency[word] > 1] for text in documentsb__after_preprocess]

    # for line in texts:
    #     print(line)

    # 3.创建字典（单词与编号之间的映射）
    # print('3.创建字典（单词与编号之间的映射）')
    dictionary = corpora.Dictionary(texts)
    # print(dictionary)
    # 打印字典，key为单词，value为单词的编号
    # print(dictionary.token2id)

    # 4.将待比较的文档转换为向量（词袋表示方法）
    # print('4.将待比较的文档转换为向量（词袋表示方法）')
    # 使用doc2bow方法对每个不同单词的词频进行了统计，并将单词转换为其编号，然后以稀疏向量的形式返回结果
    new_vec = [dictionary.doc2bow(text) for text in documentsq__after_preprocess]
    # print(new_vec)  #这个就是query 了!!!!
    ##
    # 5.建立语料库
    # print('5.建立语料库')
    # 将每一篇文档转换为向量
    corpus = [dictionary.doc2bow(text) for text in documentsb__after_preprocess]
    # print(corpus)

    # 6.初始化模型
    # print('6.初始化模型')
    # 初始化一个tfidf模型,可以用它来转换向量（词袋整数计数），表示方法为新的表示方法（Tfidf 实数权重）
    tfidf = models.TfidfModel(corpus)
    # 将整个语料库转为tfidf表示方法
    corpus_tfidf = tfidf[corpus]  # 这个就是比较的库
    # 7.创建索引
    # print('7.创建索引')
    # 使用上一步得到的带有tfidf值的语料库建立索引#如果库太小,下行会出现bug.这时候需要制定字典.
    index = similarities.MatrixSimilarity(corpus_tfidf, num_features=len(dictionary))  # 这个是根据词频算内积,也就是看句子有多少个词汇一样,一样的越多,分数越高.

    # 8.相似度计算并返回相似度最大的文本
    # print('# 8.相似度计算并返回相似度最大的文本')
    new_vec_tfidf = [tfidf[i] for i in new_vec]  # 将待比较文档转换为tfidf表示方法
    ##
    # 计算要比较的文档与语料库中每篇文档的相似度
    sims = index[new_vec_tfidf]

    # 删除numpy矩阵q数据里面的对角线数据,因为他们是自己跟自己比没有意义的.

    for i in range(chaxunshuliang):  # q 里面0 对应 shujukushuliang
        sims[0 + i][i + shujukushuliang] = 0

    ##

    import numpy as np
    tmp = np.argmax(sims, axis=1)
    tmp2 = np.max(sims, axis=1)


    # print("当前步奏使用时间",end-start)
    step += 1

    tmp3 = set([kaishi + i for i in range(len(tmp2)) if tmp2[i] > yuzhi])  # tmp3是需要删除的文本

    queue.put(set(tmp3))
    return 1

##   jiekade算法实现.
# import distance
#
# def edit_distance(s1, s2):
#     return distance.levenshtein(s1, s2)
#
# tmp=edit_distance("鼠标称","鼠标称")

# print(tmp)

def main3m(yuzhi=0.6,
           pathb='database(1).txt',
           pathq='query(1).txt',
           b_n=10,  # 切割数量
           q_n=10,k=10):
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


