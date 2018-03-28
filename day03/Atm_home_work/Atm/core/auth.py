#!_*_coding:utf-8_*_
# __author__:"Alex Li"
import os
from core import db_handler
from conf import settings
from core import accounts
import json
import datetime



def acc_auth(account, password):
    '''
    account auth func
    :param account: credit account number
    :param password: credit card password
    :return: if passed the authentication , retun the account object, otherwise ,return None
    '''
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account)
    # print(account_file)
    if os.path.isfile(account_file):
        with open(account_file, 'r') as f:
            account_data = json.load(f)
            if account_data['password'] == password:
                exp_time_stamp = datetime.datetime.strptime(account_data['expire_date'], "%Y-%m-%d")
                status = account_data['status']
                if datetime.datetime.now() > exp_time_stamp:
                    print(
                        "\033[31;1mAccount [%s] has expired,please contact the admin to get a new card!\033[0m" % account)
                elif status == 0 or status == 8:  # 状态正常，或者为admin
                    return account_data
                else:
                    print("Account \033[31;1m%s\033[0m] status is abnormal,please contact the admin.")
            else:
                print("\033[31;1mAccount ID or password is incorrect!\033[0m")
    else:
        print("\033[31;1mAccount [%s] does not exist!\033[0m" % account)


def acc_login(user_data, log_obj):
    '''
    account login func
    :user_data: user info data , only saves in memory
    :return:
    '''
    exit_count = 3  # 登录次数限制
    retry_count = 0 # 初始化重试数据
    same_account = 0    # 输入时，相同用户计数
    last_account = ""   # 初始化上一次输入的用户
    while user_data['is_authenticated'] is not True and retry_count < exit_count:
        account = input("\033[32;1maccount:\033[0m").strip()
        password = input("\033[32;1mpassword:\033[0m").strip()
        if account == last_account:
            same_account += 1
        auth = acc_auth(account, password)
        last_account = account
        if auth:  # not None means passed the authentication
            user_data['is_authenticated'] = True
            user_data['account_id'] = account
            # print("welcome")
            return auth
        retry_count += 1
    else:
        if same_account == exit_count - 1:
            log_obj.error("account [%s] too many login attempts" % account)
        exit()


def acc_check(account):
    '''
    查找帐号是否存在
    :param account: credit account number
    :return: 帐号存在返回真，否则返回假
    '''
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account)
    if os.path.isfile(account_file):
        with open(account_file, 'r') as f:
            account_data = json.load(f)
            status = account_data['status']
            # if status == 8:  # 帐户为管理员
            #     print("\033[31;1mGet account [%s] info pemission denied!\033[0m" % account)
            #     return False

            exp_time_stamp = datetime.datetime.strptime(account_data['expire_date'], "%Y-%m-%d")
            if datetime.datetime.now() > exp_time_stamp:
                print("\033[31;1mAccount [%s] has expired!\033[0m" % account)
                return False
            else:
                return account_data
    else:
        return False


def sign_up():
    """
    用户注册和admin管理用户
    :return:
    """
    pay_day = 22
    exist_flag = True
    while exist_flag is True:
        account = input("\033[32;1maccount id:\033[0m").strip()
        password = input("\033[32;1mpassword:\033[0m").strip()
        exist_flag = acc_check(account)
        if exist_flag:
            print("Account [\033[31;1m%s\033[0m] is exist,try another account." % account)
            exist_flag = True
            continue
        else:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            # 默认5年后过期
            after_5_years = int(datetime.datetime.now().strftime('%Y')) + 5 # 5年后的年份
            after_5_years_today = datetime.datetime.now().replace(year = after_5_years)   # 5年后的今天
            expire_day = (after_5_years_today + datetime.timedelta(-1)).strftime('%Y-%m-%d')
            """用户数据库格式
            {"enroll_date": "2016-01-02", "password": "abc", "id": 1000, "credit": 15000,
             "status": 0, "balance": 1000.0, "expire_date": "2021-01-01", "pay_day": 22}
            """
            account_data = {"enroll_date": today, "balance": 15000, "password": password, "id": account,
                            "credit": 15000, "status": 0, "expire_date": expire_day,"pay_day": pay_day}
            accounts.dump_account(account_data)
            print("account [\033[32;1m%s\033[0m] added sucessed" % account)
            return True


def modify():
    """
    修改用户信息
    :return:
    """
    # 可以修改的项目
    items = ["password", "credit", "status", "expire_date", "pay_day"]
    acc_data = False
    continue_flag = False
    while acc_data is False:
        account = input("\033[32;1maccount id:\033[0m").strip()
        account_data = acc_check(account)
        if account_data is False:  # 用户不存在
            print("Account [\033[31;1m%s\033[0m] is not exist,try another account." % account)
            continue
        else:
            while continue_flag is not True:
                # 判断输入，要求为json格式
                print('''You can choose the items like this:
{
    "password": "abc",
    "credit": 15000,
    "status": 0,
    "expire_date": "2021-01-01",
    "pay_day": 22
}''')
                modify_items = input("Input modify items(\033[32;1mjson\033[0m):").strip()
                try:
                    modify_items_dict = json.loads(modify_items)
                except Exception as e:
                    print("\033[31;1mInput not a json data type!\033[0m")
                    continue

                error_flag = False  # 初始化错误标记
                for index in modify_items_dict:
                    if index in items:
                        account_data[index] = modify_items_dict[index]  # 修改
                    else:
                        print("Your input item [\033[31;1m%s\033[0m] is error!" % index)
                        error_flag = True  # 输入有错误
                        continue

                if error_flag:  # 输入有错误，要求重新输入
                    continue

                accounts.dump_account(account_data) # 更新到数据库
                print("\033[32;1mAccount infomation updated!\033[0m")
                continue_flag = True
                acc_data = True

    return True

