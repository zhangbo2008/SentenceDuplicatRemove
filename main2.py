
def mai2():
    ##

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
    yuzhi=0.1

    from gensim import corpora, models, similarities
    import logging
    from collections import defaultdict
    import jieba
    import time

    pathb='shuru_database.txt'
    pathq='shuru_query.txt'



    start=time.time()

    # 准备数据：现有8条文本数据，将8条文本数据放入到list中
    documentsb =[i for  i in open(pathb,encoding='utf-8').readlines() ]*10000

    documentsq =[i for  i in open(pathq,encoding='utf-8').readlines() ]*10000


    shujukushuliang=len(documentsb)
    chaxunshuliang=len(documentsq)
    documentAll=documentsb+documentsq









    ##
    # 待比较的文档

    # 获取停用词
    stopwords = set()
    file = open("stopwords.txt", 'r', encoding='UTF-8')
    for line in file:
        stopwords.add(line.strip())
    file.close()

    # 将分词、去停用词后的文本数据存储在list类型的texts中
    documentsb__after_preprocess = [] #预处理之后的数据库记做documentsb__after_preprocess
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
    documentsq__after_preprocess = [] #预处理之后的数据库记做documentsb__after_preprocess
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
    print('2.计算词频')
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
    print('3.创建字典（单词与编号之间的映射）')
    dictionary = corpora.Dictionary(texts)
    # print(dictionary)
    # 打印字典，key为单词，value为单词的编号
    # print(dictionary.token2id)

    # 4.将待比较的文档转换为向量（词袋表示方法）
    print('4.将待比较的文档转换为向量（词袋表示方法）')
    # 使用doc2bow方法对每个不同单词的词频进行了统计，并将单词转换为其编号，然后以稀疏向量的形式返回结果
    new_vec =[dictionary.doc2bow(text) for text in documentsq__after_preprocess]
    #print(new_vec)  #这个就是query 了!!!!
    ##
    # 5.建立语料库
    print('5.建立语料库')
    # 将每一篇文档转换为向量
    corpus = [dictionary.doc2bow(text) for text in documentsb__after_preprocess]
    print(corpus)

    # 6.初始化模型
    print('6.初始化模型')
    # 初始化一个tfidf模型,可以用它来转换向量（词袋整数计数），表示方法为新的表示方法（Tfidf 实数权重）
    tfidf = models.TfidfModel(corpus)
    # 将整个语料库转为tfidf表示方法
    corpus_tfidf = tfidf[corpus]       #这个就是比较的库
    # for doc in corpus_tfidf:
    #     print(doc)
    ##









    # 7.创建索引
    print('7.创建索引')
    # 使用上一步得到的带有tfidf值的语料库建立索引
    index = similarities.MatrixSimilarity(corpus_tfidf) #这个是根据词频算内积,也就是看句子有多少个词汇一样,一样的越多,分数越高.

    # 8.相似度计算并返回相似度最大的文本
    print('# 8.相似度计算并返回相似度最大的文本')
    new_vec_tfidf =[tfidf[i] for i in new_vec]  # 将待比较文档转换为tfidf表示方法
    ##
    # 计算要比较的文档与语料库中每篇文档的相似度
    sims = index[new_vec_tfidf]




    #删除numpy矩阵q数据里面的对角线数据,因为他们是自己跟自己比没有意义的.

    for i in range(chaxunshuliang):#q 里面0 对应 shujukushuliang
        sims[0+i][i+shujukushuliang]=0





















    ##



    import numpy as np
    tmp=np.argmax(sims,axis=1)
    tmp2=np.max(sims,axis=1)
    ##
    tmp3=[i for i in range(len(tmp2)) if tmp2[i] <yuzhi]
    tmp4=[i for i in range(len(tmp2)) if i not in tmp3]

    #tmp3表示那些有价值的数据 index
    #tmp4是无价值数据 index


    tmp5=[documentsq[i] for i in  tmp3]
    tmp6=[documentsq[i] for i in  tmp4]
    import os
    if os.path.exists('result/new_add.txt'):
        os.remove('result/new_add.txt')
    if os.path.exists('result/new_wuxiao.txt'):
        os.remove('result/new_wuxiao.txt')

    ##
    with open('result/new_add.txt','w') as f:

        for i in tmp5:
            f.write(i)



    with open('result/new_wuxiao.txt','w') as f:
        for i in tmp6:
            f.write(i)
    ##
    import random
    random.shuffle (tmp3 )
    random.shuffle (tmp4 )
    tmp3=tmp3[:10]
    tmp4=tmp4[:10]


    if os.path.exists('result/new_add_check.txt'):
        os.remove('result/new_add_check.txt')
    if os.path.exists('result/new_wuxiao_check.txt'):
        os.remove('result/new_wuxiao_check.txt')
    with open('result/new_add_check.txt','w') as f:

        for i in tmp3:
            xiangsiwenben=documentAll[tmp[i]] #跟i最相似的文本是
            if '\n' not in xiangsiwenben:
                xiangsiwenben = xiangsiwenben + '\n'

            wenben=documentsq[i]
            if '\n' not in wenben:
                wenben = wenben + '\n'
            f.write('查询的文本:'+wenben)
            f.write('和查询的文本最相似的文本:'+xiangsiwenben)
            print(tmp[i])
            if tmp[i]>shujukushuliang-1:
                dex=tmp[i]-shujukushuliang+1

                f.write('对应索引:' + "Q中" + str(i+1) + "行" + "Q中" + str(dex)+"行")

                f.write('相似分数'+str(tmp2[i]))
                f.write('\n')
            else:
                dex=tmp[i]+1
                f.write('对应索引:' + "Q中" + str(i+1) + "行" + "B中" + str(dex) + "行")
                f.write('相似分数'+str(tmp2[i]))
                f.write('\n')






    with open('result/new_wuxiao_check.txt','w') as f:
        for i in tmp4:
            xiangsiwenben = documentAll[tmp[i]]  # 跟i最相似的文本是
            if '\n' not in xiangsiwenben:
                xiangsiwenben = xiangsiwenben + '\n'

            wenben = documentsq[i]
            if '\n' not in wenben:
                wenben = wenben + '\n'
            f.write('查询的文本:' + wenben)
            f.write('和查询的文本最相似的文本:' + xiangsiwenben)
            if tmp[i] > shujukushuliang-1:
                dex = tmp[i] - shujukushuliang+1

                f.write('对应索引:' + "Q中" + str(i+1) + "行" + "Q中" + str(dex) + "行")
                f.write('相似分数'+str(tmp2[i]))
                f.write('\n')
            else:
                dex = tmp[i]+1
                f.write('对应索引:' + "Q中" + str(i+1) + "行" + "B中" + str(dex) + "行")
                f.write('相似分数'+str(tmp2[i]))
                f.write('\n')
    end=time.time()
    print(end-start)