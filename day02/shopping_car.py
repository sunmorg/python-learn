# -*- coding:utf-8 -*-
# Author：sunmorg

import getpass

count = 0  # 计数器
username = "sunm"  # 登录用户名
userpassword = "abc123"  # 登录密码


#创建黑名单表
f=open('name.txt','a', encoding='utf-8')
f.close()
#创建用户余额存放地址
f = open('salary.txt', 'a', encoding='utf-8')
f.close()
#创建用户历史消费记录
f = open('history.txt', 'a', encoding='utf-8')
f.close()

f = open("name.txt", "r", encoding='utf-8')
file_list = f.readlines()
f.close()

lock = []
name = input("登录用户名:")

# 判断用户是否在黑名单
for i in file_list:
    line = i.strip("\n")
    lock.append(line)
if name in lock:
    print("您的账号已锁定，请联系管理员。")
    exit()
else:
    # 如果用户没有在黑名单，判断用户是否存在。
    if name == username:
        # 如果密码连续输错三次，锁定账号。
        while count < 3:
            password = input("登录密码：")
            if name == username and password == userpassword:
                print("\033[92mWelcome to Mr.wang mall\033[0m")
                break
            else:
                print("账号密码不匹配")
                count += 1
                if count ==3:
                    print("对不起，您的账号连续输错三次账号已锁定，请联系管理员。")
                    f = open("aaa.txt", "w+", encoding="utf-8")
                    li = ['%s' % username]
                    f.writelines(li)
                    f.close()
                    exit()
        else:
            print("对不起，您的账号连续输错三次账号已锁定，请联系管理员。")
            f = open("name.txt", "w+", encoding="utf-8")
            li = ['%s' % username]
            f.writelines(li)
            f.close()
    else:
        print("用户名不存在，请输入正确的用户名。")
        exit()

#用户购买商品列表
shopping_list = []
#用户购买物品名称存放列表
goods_name = []
#用户购买物品价格存放列表
goods_price = []
#商品价格列表

goods =[
    {"name": "电脑", "price": 1999},
    {"name": "鼠标", "price": 10},
    {"name": "游艇", "price": 20},
    {"name": "美女", "price": 998},
    {"name": "手机", "price": 2998},
    {"name": "键盘", "price": 598}
]

#读取用户的余额，如果首次登陆余额为0
f1 = open("salary.txt", "r", encoding='utf-8')
file_list = f1.readlines()
f1.close()
salary = []
if file_list:
    print("")
else:
    f2 = open("salary.txt", "w", encoding='utf-8')
    f2.write("0")
    f2.close()
f1 = open("salary.txt", "r", encoding='utf-8')
fil_list = f1.readlines()
f1.close()
for i in fil_list:
    lin = i.strip("\n")
    salary.append(lin)

salary = int(salary[0])

#商品购买循环
while True:
     #循环打印商品目录
     for j in range(1):
         print("----  商品列表  ----")
         for i,v in enumerate(goods):
          print (i,v['name'], v['price'])
     var = (input("\033[94m请输入你要买的商品序列号(充值：t 余额：b 已购买：y 购买记录：h 退出：q)：\033[0m"))
     #判断用户输入的是否为商品序号是否为数字
     if var.isdigit():
         var = int(var)
         #判断用户输入的商品序号是否在范围内
         if var >=0 and len(goods) > var:
               choiceGood = goods[var]
               #判断用户的余额是否足够买想要的商品
               if choiceGood['price'] <= salary:
                   shopping_list.append(choiceGood)
                   goods_name.append(choiceGood['name'])
                   goods_price.append(choiceGood['price'])
                   salary = salary - choiceGood['price']
                   print("\033[94m您购买\033[0m\033[95m%s\033[0m\033[94m已加入购物车后，您的余额还有\033[0m\033[95m%s\033[0m"%(choiceGood['name'],salary))
                   f = open("history.txt", "a", encoding='utf-8')
                   li = ['购买%s，价格%s，余额%s\n' % (choiceGood['name'],choiceGood['price'],salary)]
                   f.writelines(li)
                   f.close()
               else:
                   print("\033[91m您的余额不足(余额：%s)，请充值后购买(充值：t)。\033[0m"%salary)
         else:
             print("\033[91m没有找到您想要的商品,请重新输入商品编号。\033[0m")
             continue
     elif var == "t":
        num1 = input("\033[94m请输入充值金额：\033[0m")
        if num1.isdigit():
          num1 = int(num1)
          salary = salary + num1
          print("您现在的总余额是：",salary)
        else:
          print("\033[91m请输入正确的充值金额\033[0m")
          num1 = input("\033[94m请输入充值金额：\033[0m")
          continue
     elif var == "q":
         exit()
     elif var == "b":
         print("\033[91m您当前余额为：%s\033[0m"%salary)
     elif var == 'h':
         f = open("history.txt", "r", encoding='utf-8')
         print("历史消费记录：")
         for i,line in enumerate(f.readlines()):
             print(i,line)
         f.close()
     elif  var == "y":
         print("--------shopping list------")
         goods_name.sort()
         s = set(goods_name)
         for item in s:
             print (" %s     x   %d"%(item,goods_name.count(item)))
         sum = 0
         for j in goods_price:
             sum = sum +j
         print("您总计消费：\033[95m % s\033[0m余额:\033[95m % s\033[0m"%(sum,salary))
         print("\033[94m欢迎您下次购物\033[0m")
         f = open("salary.txt", "w+", encoding='utf-8')
         la = ['%s' %salary]
         f.writelines(la)
         f.close()
         exit()
     else:
         print("\033[91m请输入正确的商品编号。\033[0m")
         continue
