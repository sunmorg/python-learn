# -*- coding:utf-8 -*-
# Author：sunmorg

product_list = [
    ('iphone',5800),
    ('Mac Pro',9800),
    ('Bike',800),
    ('Watch',10800),
    ('coffee',58),
    ('python in action',88)
]

shopping_list = []

salary = input('请输入存款:')

if salary.isdigit():
    salary = int(salary)
    while True:
        for index,item in enumerate(product_list):
            #print(product_list.index(item),item)
            print(index,item)
        user_choice = input("选择要买的商品>>>:")
        if user_choice.isdigit():
            user_choice = int(user_choice)
            if user_choice < len(product_list) and user_choice >= 0:
                p_item = product_list[user_choice]
                if p_item[1] <= salary: #买得起
                    shopping_list.append(p_item)
                    salary -= p_item[1]
                    print("added %s into shopping cart, your current balance is \033[31;1m%s\033[0m"%(p_item,salary))
                else:
                    print("\033[41;1m你的钱只剩[%s]la ,买不起啦\033[0m" % salary)
            else:
                print("商品[%s]不存在"%user_choice)
        elif user_choice == 'q':
            print("----------- shopping list -----------")
            for p in shopping_list:
                print(p)
            print('您的余额为\033[31;1m%s\033[0m'%salary)
            exit()
        else:
            print("exit")