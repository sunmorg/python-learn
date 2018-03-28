#!_*_coding:utf-8_*_
# __author__:"Alex Li"

'''
main program handle module , handle all the user interaction stuff

'''

from core import auth
from core import logger
from core import accounts
from core import transaction
from core import db_handler
from conf import settings
import datetime
import time
import os

# transaction logger
trans_logger = logger.logger('transaction')
# access logger
access_logger = logger.logger('access')

# temp account data ,only saves the data in memory
user_data = {
    'account_id': None,
    'is_authenticated': False,
    'account_data': None

}


def display_account_info(account_data):
    '''
    打印未登录用户帐户信息（管理员可直接使用）
    :param account_data: 帐户信息
    :return:
    '''
    ignore_display = ["password"]
    for k in account_data:
        if k in ignore_display:
            continue
        else:
            print("{:<20}:\033[32;1m{:<20}\033[0m".format(k, account_data[k]))


def account_info(acc_data):
    """
    打印登录用户帐户信息
    :param acc_data: 登录信息
    :return:
    """
    account_id = acc_data["account_id"]
    account_data = acc_data["account_data"]
    status = account_data["status"]
    if status == 8:  # 管理员
        new_account_id = input("\033[32;1mPlease input your query account id:\033[0m").strip()
        # 管理员之间不能相互查看对方
        new_account_data = auth.acc_check(new_account_id)  # 管理员获取普通用户信息
        new_status = new_account_data["status"]
        if new_status == 8 and account_id != new_account_id:  # 另一管理员，禁止查看
            print("\033[31;1mGet account [%s] info pemission denied!\033[0m" % new_account_id)
            return True

    display_account_info(account_data)
    return True


def pay(amount):
    '''
    消费付款
    :param amount: 付款金额
    :return:
    '''
    # acc_data = auth.acc_login(user_data, access_logger)
    # if user_data['is_authenticated']:
    #     user_data['account_data'] = acc_data
    acc_data = get_user_data()
    account_data = accounts.load_current_balance(acc_data['account_id'])
    if amount > 0:
        new_balance = transaction.make_transaction(trans_logger, account_data, 'pay', amount)
        if new_balance:
            return True
            #     print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))

    else:
        print('[\033[31;1m%s\033[0m] is not a valid amount, only accept integer!' % amount)
        return None


def repay(acc_data):
    '''
    print current balance and let user repay the bill
    :param acc_data:
    :return:
    '''
    account_data = accounts.load_current_balance(acc_data['account_id'])
    # for k,v in account_data.items():
    #    print(k,v )
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        print("Tip: [b] to back")
        repay_amount = input("\033[33;1mInput repay amount:\033[0m").strip()
        if len(repay_amount) > 0 and repay_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger, account_data, 'repay', repay_amount)
            time.sleep(0.1)  # 处理显示问题
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        elif repay_amount == 'b':
            back_flag = True
        else:
            print('[\033[31;1m%s\033[0m] is not a valid amount, only accept integer!' % repay_amount)


def withdraw(acc_data):
    '''
    print current balance and let user do the withdraw action
    :param acc_data:
    :return:
    '''
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        print("Tip: [b] to back")
        withdraw_amount = input("\033[33;1mInput withdraw amount:\033[0m").strip()
        if len(withdraw_amount) > 0 and withdraw_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger, account_data, 'withdraw', withdraw_amount)
            time.sleep(0.1)  # 处理显示问题
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        elif withdraw_amount == 'b':
            back_flag = True
        else:
            print('[\033[31;1m%s\033[0m] is not a valid amount, only accept integer!' % withdraw_amount)


def transfer(acc_data):
    '''
    打印当前余额，并转帐
    :param acc_data:
    :return:
    '''
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s

(Tip: input [b] to back)''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        receiver = input("\033[33;1mInput receiver:\033[0m").strip()  # 收款人
        if receiver == account_data["id"]:  # 判断帐号是否为自己
            print("\033[31;1mThe receiver is yourself!\033[0m")
            continue
        elif receiver == "b":
            break
        else:
            receiver_account_data = auth.acc_check(receiver)  # 判断收款人帐号是否存在和过期
            status = receiver_account_data['status']
            if status == 0:  # 只有收款人为普通帐户，且状态正常，才能转帐
                transfer_amount = input("\033[33;1mInput transfer amount:\033[0m").strip()
                if len(transfer_amount) > 0 and transfer_amount.isdigit():
                    new_balance = transaction.make_transaction(trans_logger, account_data, 'transfer', transfer_amount)
                    transaction.make_transaction(trans_logger, receiver_account_data, 'receive', transfer_amount)
                    if new_balance:
                        print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))

                else:
                    print('[\033[31;1m%s\033[0m] is not a valid amount, only accept integer!' % transfer_amount)

                if transfer_amount == 'b':
                    back_flag = True


def pay_check(acc_data):
    """
    查询帐单详情
    :param acc_data:
    :return:
    """
    bill_date = input("Please input the date you will query "
                      "like [\033[32;1m2016-12\033[0m]>>>").strip()
    log_path = db_handler.db_handler(settings.LOG_DATABASE)
    bill_log = "%s/%s.bills" % (log_path, acc_data['account_id'])
    if not os.path.exists(bill_log):
        print("Account [\033[32;1m%s\033[0m] is no bills." % acc_data["account_id"])
        return

    print("Account [\033[32;1m%s\033[0m] bills:" % acc_data["account_id"])
    print("-".center(50, "-"))
    with open(bill_log, "r") as f:
        for bill in f:
            print(bill)
            b_date = bill.split(" ")[0]  # 帐单月份
            if bill_date == b_date:
                print("\033[33;1m%s\033[0m" % bill.strip())

    log_type = "transaction"
    print("Account [\033[32;1m%s\033[0m] history log:" % acc_data["account_id"])
    logger.show_log(acc_data['account_id'], log_type, bill_date)


def save(acc_data):
    """
    存钱
    :param acc_data:
    :return:
    """
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' --------- BALANCE INFO --------
        Credit :    %s
        Balance:    %s

(Tip: input [b] to back)''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        save_amount = input("\033[33;1mInput your save amount:\033[0m").strip()  # 存款金额
        if save_amount == 'b':
            back_flag = True
        elif len(save_amount) > 0 and save_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger, account_data, 'save', save_amount)
            time.sleep(0.1)  # 解决日志显示问题
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
                back_flag = True
        else:
            print('[\033[31;1m%s\033[0m] is not a valid amount, only accept integer!' % save_amount)


def logout(acc_data):
    '''
    清除认证信息，退出
    :param acc_data:
    :return:
    '''
    # acc_data['account_id'] = None
    # acc_data['is_authenticated'] = False,
    # acc_data['account_data'] = None
    exit("Bye,thanks!".center(50, "#"))


def interactive(acc_data):
    '''
    interact with user
    :return:
    '''
    # 只允许普通用户
    status = acc_data["account_data"]["status"]
    if status == 8:  # 管理员登录后，直接退出
        exit("Account [%s],please use manager.py to login!"
             % acc_data["account_id"])

    menu = u'''
    ------- Oldboy Bank ---------\033[32;1m
    1.  账户信息
    2.  还款(示例)
    3.  取款(示例)
    4.  转账
    5.  存款
    6.  账单
    7.  退出
    \033[0m'''
    menu_dic = {
        '1': account_info,
        '2': repay,
        '3': withdraw,
        '4': transfer,
        '5': save,
        '6': pay_check,
        '7': logout,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option](acc_data)

        else:
            print("\033[31;1mOption does not exist!\033[0m")


def get_bill(account_id):
    '''
    生成帐单，定于每月25日
    :param account_id: 帐户id
    :return:
    '''
    i = datetime.datetime.now()  # 当前时间
    year_month = "%s-%s" % (i.year, i.month)  # 帐单年月
    account_data = accounts.load_current_balance(account_id)  # 获取帐户信息
    balance = account_data["balance"]  # 可用额度
    credit = account_data["credit"]  # 信用额度
    if i.day != settings.BILL_DAY:
        print("\033[31;1mToday is not the bill generation day!\033[0m")
        # return    # 此处为了演示，先注释

    if balance >= credit:
        repay_amount = 0
        bill_info = "Account [\033[32;1m%s\033[0m] needn't to repay." % account_id
    else:
        repay_amount = credit - balance
        bill_info = "Account [\033[32;1m%s\033[0m] need to repay [\033[33;1m%s\033[0m]" \
                    % (account_id, repay_amount)

    print(bill_info)
    log_path = db_handler.db_handler(settings.LOG_DATABASE)
    bill_log = "%s/%s.bills" % (log_path, account_id)
    with open(bill_log, "a+") as f:
        f.write("bill_date: %s account_id: %s need_repay: %d\n" % (year_month, account_id, repay_amount))


def get_all_bill():
    '''
    生成全部可用用户的帐单
    :return:
    '''
    db_path = db_handler.db_handler(settings.DATABASE)
    for root, dirs, files in os.walk(db_path):
        for file in files:
            if os.path.splitext(file)[1] == '.json':  # 以.json结尾的文件
                account_id = os.path.splitext(file)[0]  # 帐户id
                # account_file = "%s/%s.json" % (db_path, account_id)
                account_data = auth.acc_check(account_id)  # 获取用户信息
                status = account_data['status']
                print("Account bill:".center(50, "-"))
                # 除了管理员，普通帐户都应该出帐单，即使帐户禁用
                if status != 8:
                    display_account_info(account_data)  # 显示帐户详情
                    get_bill(account_id)  # 获取帐单
                print("End".center(50, "-"))

    return True


def check_admin(func):
    """
    检查是否管理员
    :param func:
    :return:
    """

    def inner(*args, **kwargs):
        if user_data['account_data'].get('status', None) == 8:
            ret = func(*args, **kwargs)
            return ret
        else:
            print('\033[31;1mPermission denied\033[0m')

    return inner


@check_admin
def manage_func(acc_data):
    """
    管理员的功能
    :return:
    """
    menu = u'''
    ------- Admin erea ---------\033[32;1m
    1.  添加账户
    2.  查询用户信息
    3.  用户信息修改（冻结帐户、用户信用卡额度等）
    4.  生成全部用户帐单
    5.  退出
    \033[0m'''
    menu_dic = {
        '1': 'auth.sign_up()',
        '2': 'account_info(acc_data)',
        '3': 'auth.modify()',
        '4': 'get_all_bill()',
        '5': 'logout(acc_data)',
    }
    go_flag = True
    while go_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic.keys():
            go_flag = eval(menu_dic[user_option])
        else:
            print("\033[31;1mOption does not exist!\033[0m")


def get_user_data():
    '''
    登录并获取新user_data
    :return:
    '''
    account_data = auth.acc_login(user_data, access_logger)
    if user_data['is_authenticated']:
        user_data['account_data'] = account_data
        return user_data
    else:
        return None


def run():
    '''
    this function will be called right a way when the program started, here handles the user interaction stuff
    :return:
    '''
    print("Welcome to ATM".center(50, "#"))
    user_data = get_user_data()
    interactive(user_data)


def manage_run():
    print("ATM admin manager".center(50, "#"))
    user_data = get_user_data()
    manage_func(user_data)
