#encoding:utf-8
import os
import multiprocessing
import time


def write(q):
    print("write启动(%s)，父进程为(%s)" % (os.getpid(), os.getppid()))
    for i in "python":
        q.put(i)


def read(q):
    print("read启动(%s)，父进程为(%s)" % (os.getpid(), os.getppid()))
    for i in range(q.qsize()):
        print("read从Queue获取到消息：%s" % q.get(True))


if __name__ == "__main__":
    print("(%s) start" % os.getpid())
    q = multiprocessing.Manager().Queue()
    po = multiprocessing.Pool()
    po.apply_async(write, args=(q,))



    po.apply_async(read, args=(q,))
    po.close()
    po.join()

    print("(%s) end" % os.getpid())