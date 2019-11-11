
def main4(    yuzhi=0.6,
    pathb='database(1).txt',
    pathq='query(1).txt',
    b_n=10,#切割数量
    q_n=10):
    ##
    # import distance
    #
    # def edit_distance(s1, s2):
    #     return distance.levenshtein(s1, s2)
    #
    # tmp=edit_distance("鼠标称","鼠标称")

    # print(tmp)





    #根据编辑距离来算.


    #大数据切割版代码!
    # coding=utf-8

    from tqdm import tqdm
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







    #计算文件行数最快的方法,统计\n

    def hangshu(filepath):
        count = 0
        for index, line in enumerate(open(filepath, 'r',encoding='utf-8')):
            count += 1
        return count
    # print(hangshu(pathb))
    ##










    Removesave=[]
    #pip3 install distance
    def op(  s,q,kaishi,skaishi,biaozhi):#这个函数做一次切分操作
        out=[]
        nonlocal  Removesave
        import distance

        def edit_distance(s1, s2):
            return distance.levenshtein(s1, s2)
        s=q+s
        for i in range(len(q)):
            for j in range(i+1,len(s)):




                tmp1=edit_distance(q[i],s[j])
                if tmp1<yuzhi:
                    out.append(i+kaishi)
                    Removesave.append('废除的句子是q中的'+str(i)+'句'+'      跟他相似的句子是'+str(str(j+skaishi)+biaozhi)+'       句子内容是'+str(s[j]))
                    break
        return set(out)







    import numpy as np
    out1=np.array([])
    out2=np.array([])
    out=set()
    #切割.hou yunsuan
    import linecache
    bhang=hangshu(pathb)
    qhang=hangshu(pathq)
    for i in tqdm(range(q_n)):
            delta=qhang//q_n
            if i !=q_n-1:
                q=linecache.getlines(pathq)[i*delta:(i+1)*delta]
            else:
                q=linecache.getlines(pathq)[i*delta:]


            #下面分析s的分块
            if i <q_n-1:#这时候需要s跑遍查询q后面和s的全部
                for j in range(i+1,q_n):
                      if j !=q_n-1:
                         s = linecache.getlines(pathq)[j * delta:(j + 1) * delta]
                      else:
                          s = linecache.getlines(pathq)[j  * delta:]





                      tmp=op(s,q,i*delta,j * delta,'q')
                      out=out.union(tmp)

                delta2= bhang // b_n
                for j in range(b_n):

                    if j != b_n - 1:
                        s = linecache.getlines(pathb)[j * delta2:(j + 1) * delta2]
                    else:
                        s = linecache.getlines(pathb)[j * delta2:]
                    tmp = op(s, q, i * delta,j * delta2,'s')
                    out = out.union(tmp)



            if i==q_n-1:
                delta2 = bhang // b_n
                for j in range( b_n):

                    if j != b_n - 1:
                        s = linecache.getlines(pathb)[j * delta2:(j + 1) * delta2]
                    else:
                        s = linecache.getlines(pathb)[j * delta2:]
                    tmp = op(s, q, i * delta,j * delta2,'s')
                    out = out.union(tmp)

    print("buyao的数据编号",out)

    out2=set(range(qhang))
    out2=out2-out
    print("要的数据编号",out2)
    if not os.path.exists('result'):
        os.mkdir('result')
    with open('result/Removesave.txt','w') as f:
        for i in Removesave:
           f.writelines(str(i))


    return out,out2,Removesave

    # print(out2)

    #
    #
    # #-------------后处理
    #
    # ##
    #
    # tmp3=[i for i in range(len(tmp2)) if tmp2[i] <yuzhi]
    # tmp4=[i for i in range(len(tmp2)) if i not in tmp3]
    #
    # #tmp3表示那些有价值的数据 index
    # #tmp4是无价值数据 index
    #
    #
    # tmp5=[documentsq[i] for i in  tmp3]
    # tmp6=[documentsq[i] for i in  tmp4]
    #
    #
    # ##
    # with open('result/new_add.txt','a') as f:
    #
    #     for i in tmp5:
    #         f.write(i)
    #
    #
    #
    # with open('result/new_wuxiao.txt','a') as f:
    #     for i in tmp6:
    #         f.write(i)
    # ##
    # import random
    # random.shuffle (tmp3 )
    # random.shuffle (tmp4 )
    # tmp3=tmp3[:10]
    # tmp4=tmp4[:10]
    #
    #
    # with open('result/new_add_check.txt','a') as f:
    #
    #     for i in tmp3:
    #         xiangsiwenben=documentAll[tmp[i]] #跟i最相似的文本是
    #         if '\n' not in xiangsiwenben:
    #             xiangsiwenben = xiangsiwenben + '\n'
    #
    #         wenben=documentsq[i]
    #         if '\n' not in wenben:
    #             wenben = wenben + '\n'
    #         f.write('查询的文本:'+wenben)
    #         f.write('和查询的文本最相似的文本:'+xiangsiwenben)
    #
    #         if tmp[i]>shujukushuliang-1:
    #             dex=tmp[i]-shujukushuliang+1
    #
    #             f.write('对应索引:' + "Q中" + str(i+1) + "行" + "Q中" + str(dex)+"行")
    #
    #             f.write('相似分数'+str(tmp2[i]))
    #             f.write('\n')
    #         else:
    #             dex=tmp[i]+1
    #             f.write('对应索引:' + "Q中" + str(i+1) + "行" + "B中" + str(dex) + "行")
    #             f.write('相似分数'+str(tmp2[i]))
    #             f.write('\n')
    #
    #
    #
    #
    #
    #
    # with open('result/new_wuxiao_check.txt','a') as f:
    #     for i in tmp4:
    #         xiangsiwenben = documentAll[tmp[i]]  # 跟i最相似的文本是
    #         if '\n' not in xiangsiwenben:
    #             xiangsiwenben = xiangsiwenben + '\n'
    #
    #         wenben = documentsq[i]
    #         if '\n' not in wenben:
    #             wenben = wenben + '\n'
    #         f.write('查询的文本:' + wenben)
    #         f.write('和查询的文本最相似的文本:' + xiangsiwenben)
    #         if tmp[i] > shujukushuliang-1:
    #             dex = tmp[i] - shujukushuliang+1
    #
    #             f.write('对应索引:' + "Q中" + str(i+1) + "行" + "Q中" + str(dex) + "行")
    #             f.write('相似分数'+str(tmp2[i]))
    #             f.write('\n')
    #         else:
    #             dex = tmp[i]+1
    #             f.write('对应索引:' + "Q中" + str(i+1) + "行" + "B中" + str(dex) + "行")
    #             f.write('相似分数'+str(tmp2[i]))
    #             f.write('\n')



