# -*- coding:utf-8 -*-
# Author：sunmorg

#递归练习题

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

n = 0

def recursionc(options):
    print(options)


recursionc(menus)