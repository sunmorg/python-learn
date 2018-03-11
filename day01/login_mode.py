# -*- coding:utf-8 -*-
# Author：sunmorg

import getpass

users = [["sunm",'abc123'],["zennu","abc456"],["chan","abc789"]]
count = 0
error_count = 0

while count < 3:
    userName = input("请输入用户名：").strip()
    userPwd = getpass.getpass("请输入密码:").strip()

    hasUser = False

    for i, v in enumerate(users):
        if userName in v:
            hasUser = True
            break
        else:
            hasUser = False

    if hasUser:
        errorFile = open(file='error_log.txt', mode='r', encoding='utf-8')
        errorData = errorFile.read()
        if userName in errorData:  # 判断该用户是否被锁定
            print("对不起！用户\033[31;1m%s\033[0m被锁定！请使用其他用户名登录！" % userName)
        else:
            for i, v in enumerate(users):
                if userName == v[0] and userPwd == v[1]:
                    print("欢迎登录！")
                    exit()  # 直接退出程序
                else:
                    errorFile = open(file="error_log.txt", mode='a+', encoding="utf-8")
                    error_count += 1
                    if error_count == 9:  # 每次for循环3次
                        errorFile.write("%sStatus：lock" % userName)
            print("您的用户名密码输入有误！")
        count += 1
        errorFile.close()
    else:
        print("对不起！用户\033[31;1m%s\033[0m不存在！请使用其他用户名登录！" % userName)