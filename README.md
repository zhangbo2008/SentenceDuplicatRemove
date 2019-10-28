# SentenceDuplicatRemove

运行main2.py



只是单纯根据词频.所以效果一般


解析完的结果在result目录中



处理内存不够的解决策略:

Q,S都进行分割
Q1....Qn
S1,....Sm
那么只需要Q1跟Q2,...Qn,S1,...Sm都做一次.
做n+m-1次
然后Q2同理
所以总共需要n(n+m-1)这个数量级即可.
每次复杂度还是Q1*S1的复杂度.内存每次用Q1*S1









