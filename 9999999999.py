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

    time.sleep(2)

    po.apply_async(read, args=(q,))
    po.close()
    po.join()

    print("(%s) end" % os.getpid())

















    def op(  s,q,kaishi):#这个函数做一次切分操作
        out=[]
        import distance

        def edit_distance(s1, s2):
            return distance.levenshtein(s1, s2)
        s=q+s
        for i in range(len(q)):
            for j in range(i+1,len(s)):




                tmp1=edit_distance(q[i],s[j])
                if tmp1<yuzhi:
                    out.append(i+kaishi)
                    break
        return set(out)




