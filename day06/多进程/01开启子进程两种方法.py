# -*- coding:utf-8 -*-
# Author：sunmorg


#方式1
# from multiprocessing import Process
# import time
#
# def task(name):
#     print("%s is running" %name)
#     time.sleep(3)
#     print("%s is done" %name)
#
# if __name__ == '__main__':
#     # Process(target=task,kargs={'name':'子进程1'})
#     p = Process(target=task, args=('子进程1',))
#     p.start()
#
#     print("主")

#方式二

from multiprocessing import Process
import time
class MyProcss(Process):
    def __init__(self,name):
        super().__init__()
        self.name = name
    def run(self):
        print("%s is running" %self.name)
        time.sleep(3)
        print("%s is done" %self.name)

if __name__ == '__main__':
    # Process(target=task,kargs={'name':'子进程1'})
    p = MyProcss('子进程1')
    p.start()

    print("主")