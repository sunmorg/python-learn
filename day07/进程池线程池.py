from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
import os,time,random

def task(name):
    print("name:%s pid:%s sun"%(name, os.getpid()))
    time.sleep(random.randint(1,3))


if __name__ == '__main__':
    # pool = ProcessPoolExecutor(4)#进程池
    pool = ThreadPoolExecutor(4)
    for i in range(10):
        pool.submit(task,'sunm %s' %i)
    pool.shutdown()

    print('zhu')