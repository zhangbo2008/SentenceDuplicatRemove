import jieba
from gensim import corpora,models,similarities
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 读入文档
with open("D:/58pic.com/PPT类目标题重复度检测/test.txt","r") as f:
	f = f.readlines()
# 预处理
stopwords = ["的","和","啊"]
## 1、去停词、字母小写化
texts = [[word.lower() for word in jieba.lcut(line.strip()) if word not in stopwords] for line in f]
## 2、去标点
punctuations = [',','.',':',';','?','!','(',')','[',']','@','&','#','%','$','{','}','--','-','，','。','：','；','？','！','（','）','【','】','—','_','"','“','”','|','、','<','《','>','》','~','/']
texts = [[word for word in ele if word not in punctuations] for ele in texts]
# 建立一个字典，字典表示这个词以及这个词在texts语料库中出现的次数
dictionary = corpora.Dictionary(texts)
# 将整个语料库文档转化为(id,出现次数)
corpus = [dictionary.doc2bow(text) for text in texts]
# 训练一个LSI模型 （不知道LSI模型是个什么玩意）
lsi = models.LsiModel(corpus,id2word=dictionary,num_topics=20)
# 如何找到最相关的文档，首先建立索引index （不知道为什么要建立索引）
index = similarities.MatrixSimilarity(lsi[corpus])
for n in range(0,len(f)):
	compare_text = dictionary.doc2bow(jieba.lcut(f[n].strip().lower()))
	query_lsi = lsi[compare_text]
	sims = index[query_lsi]
	for m,ele in enumerate(sims):
		if ele >0.6 and ele != 1:
			print("{},{},相似度：{}".format(f[n].strip(),f[m].strip(),ele))