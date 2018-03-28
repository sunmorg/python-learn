#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2016/12/29 14:43.
 * @author: Chinge_Yang.
'''

from core import auth
from core import logger
from core import accounts
from conf import settings
from conf import goods
import time
import os
import subprocess

# access logger
access_logger = logger.logger('access')
# 初始化购物车
shopping_cart = {}
# 初始化总花费
all_cost = 0

# temp account data ,only saves the data in memory
user_data = {
    'is_authenticated': False,
    'account_data': None
}


def interactive():
    """
    与用户交互
    :return:
    """
    menu = '''
--------------------------------------------------
    1.  Login
    2.  Sign up
    3.  Logout
--------------------------------------------------
    '''
    menu_dic = {
        '1': 'login()',
        '2': 'auth.sign_up(user_data)',
        '3': 'logout()'
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic.keys():
            exit_flag = eval(menu_dic[user_option])
        else:
            print("\033[31;1mOption does not exist!\033[0m")


def login():
    """
    登录并返回用户数据
    """
    acc_data = auth.acc_login(user_data, access_logger)  # 登录验证
    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data
        return True


def logout():
    """
    退出程序
    :return:
    """
    exit("Bye,thanks!".center(50, "#"))


def show_shopping_cart(user_data, all_cost):
    """
    # 显示购物车，更新用户信息
    """
    # 显示购物车信息
    if user_data['is_authenticated'] is True:
        account_data = user_data['account_data']  # 用户信息
        money = account_data['balance']  # 当前帐户余额
        print("You purchased products as below".center(50, "*"))
        print("%-20s %-15s %-10s %-20s" % ("Goods", "Price", "Number", "Cost"))
        for key in shopping_cart:
            p_name = key[0]
            p_price = int(key[1])
            p_number = int(shopping_cart[key])
            print("%-20s %-15s %-10s \033[32;1m%-20s\033[0m" % (p_name, p_price, p_number, p_price * p_number))
        print("End".center(50, "*"))
        print("%-20s %-15s %-10s \033[32;1m%-20s\033[0m" % ("You total cost:", "", "", all_cost))
        print("Your balance is [\033[32;1m%s\033[0m]" % money)
        accounts.dump_account(account_data)


def show_shopping_history(user_name, log_type):
    """
    存在购物历史数据则提醒用户是否打印输出
    :return:
    """
    log_file = "%s/log/%s_%s" % (settings.BASE_DIR, user_name, settings.LOG_TYPES[log_type])
    if os.path.getsize(log_file):  # 日志文件存在内容时
        # 只有输入y或者yes才读取显示购物历史，否则不显示
        print("Input \033[1;33m[y|yes]\033[0m to view your purchase history,\033[1;33m[others]\033[0m means not.")
        see_history = input("Please input:").strip()
        if see_history == "y" or see_history == "yes":
            # 显示用户购物历史
            logger.show_log(user_name, log_type)  # 显示购物历史
        else:
            print("You are not to view your purchase history!")
            print("-".center(50, "-"))


def list_one_layer():
    """
    打印输出商品列表
    :return:
    """
    one_layer_list = []  # 一级菜单
    # 打印一级菜单
    print("Species list".center(50, "-"))
    for index, item in enumerate(goods.menu):
        print("\033[32;1m%d\033[0m --> %s" % (index, item))
        one_layer_list.append(item)
    print("End".center(50, "-"))
    print("[q|b] to quit;[c] to check;[t] to top up")

    once_choice = input("Input your choice:").strip()
    if once_choice.isdigit():  # 输入数字
        once_choice = int(once_choice)
        if 0 <= once_choice < len(goods.menu):  # 输入正确数字
            print("---->Enter \033[32;1m%s\033[0m" % (one_layer_list[once_choice]))
            two_layer_list = goods.menu[one_layer_list[once_choice]]
            return two_layer_list
        else:
            print("\033[31;1mNumber out of range, please enter again!\033[0m")
    else:
        if once_choice == "b" or once_choice == "back" or once_choice == "q" or once_choice == "quit":
            show_shopping_cart(user_data, all_cost)
            time.sleep(0.1)  # 由于显示问题，添加此步解决
            exit("Bye,thanks!".center(50, "#"))
        elif once_choice == "c" or once_choice == "check":
            show_shopping_cart(user_data, all_cost)
        elif once_choice == "t":
            account_data = user_data['account_data']  # 用户信息
            money = account_data['balance']  # 当前帐户余额
            money = charge_money(money) # 充值
            user_data['account_data']['balance'] = money  # 更新帐户余额
        else:
            print("\033[31;1mPlease enter the Numbers!\033[0m")
    return None



def list_two_layer(two_layer_list):
    """
    列出二级菜单列表
    :return:
    """
    exit_flag = False
    # while exit_flag is not True:
    # 显示二级商品菜单
    print("Product list".center(50, '-'))
    for item in enumerate(two_layer_list):
        index = item[0]
        p_name = item[1][0]
        p_price = item[1][1]
        print("%s.%-20s %-20s" % (index, p_name, p_price))
    print("End".center(50, '-'))
    print("[q|quit] to quit;[b|back] to back;[c|check] to check")


def charge_money(money):
    """
    提示充值
    :return:
    """
    atm_api = os.path.dirname(settings.BASE_DIR) + \
              "/Atm/api/pay.py"
    exit_flag = False
    while exit_flag is not True:
        user_charge = input("Do you want to charge more money?[\033[32;1my|n|b]\033[0m").strip()
        if user_charge == "y" or user_charge == "yes":
            print("Please use your ATM account to pay.")
            while True:
                charge_number = input("Please input your top-up amount:").strip()
                if charge_number.isdigit():
                    # charge_number = int(charge_number)
                    cmd = "python " + atm_api + " " + charge_number
                    p = subprocess.Popen(cmd, shell = True) # 调用atm接口付款
                    sout ,serr = p.communicate()    # 交互
                    if p.returncode == 0:       # 付款成功
                        print("\033[32;1mPay successed\033[0m")
                        money += int(charge_number)  # 充值成功
                        print("Your balance is [\033[32;1m%s\033[0m]" % money)
                    else:
                        print("\033[31;1mPay failed\033[0m")

                    exit_flag = True  # 退出循环
                    break
                else:
                    print("Your input is not number!")
                    continue  # 跳到上面重新输入充值金额
        elif user_charge == "n" or user_charge == "no" or user_charge == "b" or user_charge == "back":
            exit_flag = True  # 放弃充值
        else:
            print("Your input is error!")

    return money


def go_shopping(log_obj, user_data):
    """
    购物
    :param log_obj: 日志对象
    :param user_data: 用户信息
    :return:
    """
    account_data = user_data['account_data']  # 用户信息
    money = account_data['balance']  # 当前帐户余额
    global all_cost
    flag = False
    while flag is not True:
        two_layer_list = list_one_layer()  # 得到二级菜单列表
        if not two_layer_list:
            continue

        exit_flag = False
        while exit_flag is not True:
            list_two_layer(two_layer_list)  # 列出二级菜单列表
            user_choice = input("Please choice the product:").strip()
            if user_choice.isdigit():  # 输入数字
                user_choice = int(user_choice)
                if 0 <= user_choice < len(two_layer_list):
                    product_number = input("Please input the number of product:").strip()  # 输入个数
                    if product_number.isdigit():
                        product_number = int(product_number)
                    else:
                        continue  # 重新选择商品和个数

                p_item = two_layer_list[user_choice]
                p_name = p_item[0]  # 商品名
                p_price = int(p_item[1])  # 商品价格
                new_added = {}

                if p_price * product_number <= money:  # 能付款，表示购买成功
                    new_added = {p_item: product_number}
                    # 整理购物车个数显示总数
                    for k, v in new_added.items():
                        if k in shopping_cart.keys():
                            shopping_cart[k] += v
                        else:
                            shopping_cart[k] = v
                    money -= p_price * product_number  # 更新余额
                    all_cost += p_price * product_number  # 总共花费
                    log_obj.info("account:%s action:%s product_number:%s goods:%s cost:%s" %
                                 (account_data['user'], "shopping", product_number, p_name, all_cost))
                    print("Added [\033[32;1m%d\033[0m] [\033[32;1m%s\033[0m] into shopping cart,"
                          "your balance is [\033[32;1m%s\033[0m]" % (product_number, p_name, money))
                    time.sleep(0.1)  # 由于日志显示问题，添加此步解决
                else:
                    # 钱不够时，提示充值
                    print("Your balance is [\033[31;1m%s\033[0m],cannot afford this.." % money)
                    money = charge_money(money)

                user_data['account_data']['balance'] = money  # 更新帐户余额

            else:
                if user_choice == "q" or user_choice == "quit":
                    show_shopping_cart(user_data, all_cost)
                    exit("Bye,thanks!".center(50, "#"))
                elif user_choice == "c" or user_choice == "check":
                    show_shopping_cart(user_data, all_cost)
                elif user_choice == "b" or user_choice == "back":
                    exit_flag = True
                else:
                    print("Your input is error!")


def run():
    """
    程序运行主函数
    :return:
    """
    print("Welcome to shopping mall!".center(50, "-"))
    interactive()  # 登录、注册、退出
    account_data = user_data['account_data']
    user_name = account_data['user']
    # 定义购物日志
    log_type = "shopping"
    shopping_logger = logger.logger(log_type, user_name)
    show_shopping_history(user_name, log_type)  # 是否显示购物历史
    go_shopping(shopping_logger, user_data)
