# -*- coding:utf-8 -*-
# Author：sunmorg

import os

cmd_res = os.system("dir") #os.system() 只执行命令  不保存结果
#print(cmd_res)  #输出0   表示命令执行成功

cmd_res = os.popen("dir").read() #os.popen()执行之后结果可理解为临时存在内存地址 使用read() 方法读取
#print(cmd_res)

os.mkdir("new_dir")#新建文件夹