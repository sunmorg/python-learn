# -*- coding:utf-8 -*-
# Author：sunmorg

from multiprocessing import Process
import time,os
def task():
    print("%s is running,prentid is %s" %(os.getpid(),os.getppid()))
    time.sleep(3)
    print("%s is done,prentid is %s" %(os.getpid(),os.getppid()))

if __name__ == '__main__':
    # Process(target=task,kargs={'name':'子进程1'})
    p = Process(target=task,)
    p.start()

    print("主",os.getpid(),os.getppid())