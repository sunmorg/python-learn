# -*- coding:utf-8 -*-
# Author：sunmorg

import copy

names = ["zhansan","lisi","wangwu","zhaoliu","sunm",["lihua","com"]]

# names.append("laoqi")  #  append追加
#
# names.insert(1,"sunm")  # 按想要的位置前插入  不能批量
#
# names[3] = "zennus"

'''

names.remove("zennus") # 使用remove删除

del names[1]  #使用delete删除

names.pop()  #  删除   默认删除最后一个  填入下标 想删哪个就填哪个下标

'''

# names2 = ["lihua","com"]
#
# names.extend(names2)  #合并列表

# del names2 # 删除列表

# print(names.index("sunm"))  #  index()可取出对应下标

#print(names.count("sunm"))  # count()  出现的次数

# names.clear()  # 清楚

# names.sort() #排序

# names.reverse()  #反转

# names2 = names.copy()

#names2 = copy.copy(names)  # copy.copy(names)同names.cope 浅拷贝

names2 = copy.deepcopy(names)  # copy.deepcopy(names) 深拷贝

names[2] = "李四"

names[5][0] = "李华"

print(names)

print(names2)

# print(names[0],names[3])
#  切片  0 和 -1 都可以省略
# print(names[1:3])  #  左闭右开  顾头不顾尾  切片  从第一个开始为0  可以忽略
# print(names[-1])   #  - 表示从最后往前取
# print(names[-2:])  #  只能从左往右  小的在前  为负的时候要取到最后一个 冒号后面为空