# -*- coding:utf-8 -*-
# Author：sunmorg

def func(name,*args,**kwargs):
    print(name,args,kwargs)

func("alex",22,"tesla","500w",addr="jiangxi",num=1232456)
#打印结果
#alex (22, 'tesla', '500w') {'addr': 'jiangxi', 'num': 1232456}

d={'degree':'primary'}
func("alex",d)
#打印结果
#alex ({'degree': 'primary'},) {}
func("alex",**d)
#打印结果
#alex () {'degree': 'primary'}