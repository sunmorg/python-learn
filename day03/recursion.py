# -*- coding:utf-8 -*-
# Author：sunmorg

#递归

x = 10

# while True:
#     n = int(n/2)
#     print(n)
#     if n == 0:
#         break

#  函数自己调用自己

# def calc(n):
#     n = int(n / 2)
#     print(n)
#
#     if n > 0:
#         calc(n)

#递归的返回值

count = 1

def calc(n,count):
    print(n,count)
    if count < 5:
        return calc(n/2, count+1)
    else:
        return n

res = calc(188,count)
print(res)

# 递归
#1.必须要有终止条件
#2.考虑问题复杂性 每次进入深一层递归时，问题规模相比上一次递归都应有所减少
#3.递归效率不高

#练习题
#1.打印所有节点
#2.输入一个节点名字，沙河， 你要遍历找，找到了，就打印它，并返回true
menus = [
    {
        'text':'北京',
        'children':[
            {'text':'朝阳','children':[]},
            {'text':'昌平','children':[
                {'text':'沙河','children':[]},
                {'text':'回龙观','children':[]}
            ]}
        ]
    },
    {
        'text':'上海',
        'children':[
            {'text':'宝山','children':[]},
            {'text':'金山','children':[]}
        ]
    }
]