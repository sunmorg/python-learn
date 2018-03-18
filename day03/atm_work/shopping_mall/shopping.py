# -*- coding:utf-8 -*-
# Author：sunmorg

def quota_func(money):
    '信用卡额度'
    print('信用卡额度:%s' % money)
    return money

def shopping_mall():
    '商城的商品以及该商品的价格'
    mall = [{'iphone_8_plus': '6688'}, {'mac_book': '11999'}, {'app_watch': '8888'}]
    return mall

def mall():
    mal = [{'iphone_8_plus': '6688'}, {'mac_book': '11999'}, {'app_watch': '8888'}]
    print('购物商城:')
    for shopping_num, shopping in enumerate(mal):
        print('编号: %s 商品: %s 价格: %s' % (shopping_num, list(shopping.keys())[0], list(shopping.values())[0]))

def withdraw(quota):
    '信用卡提取现金'
    print('提现的手续费:5%')
    quota = quota * (1 - 0.05)
    return quota

def authentication():
    '信用卡支付认证'
    usr_auth = {'hupeng': '123@qwer'}
    return usr_auth

def transfer_money(card):
    '信用卡转账'
    card_num = input('请输入对方账号:')
    money_tran = input('转账的金额:')
    card = card - int(money_tran.split(':')[0])
    return '转账成功，目前余额:%s' % card

if __name__ == '__main__':
    card_passwd = input('请输入您的信用卡密码:')
    shopping_car = []
    if card_passwd.split(':')[0] == authentication()['hupeng']:
        balance_card = quota_func(15000)
        print('欢迎%s' % list(authentication().keys())[0])
        while True:
            print('''
            请选择你的操作选项:
            1、购物
            2、提现
            3、转账
            4、还款
            5、退出''')
            ope_choice = input('请输入您的操作选项:')
            if ope_choice.split(':')[0] == '1':
                while True:
                    mall()
                    shopping_choice = input('请输入商品编号:')
                    balance_card = balance_card - int(list(shopping_mall()[int(shopping_choice.split(':')[0])].values())[0])
                    if balance_card > 0:
                        shopping_car.append(shopping_mall()[int(shopping_choice.split(':')[0])])
                        print('商品%s已加入购物车' % shopping_mall()[int(shopping_choice.split(':')[0])])
                    elif balance_card <= 0:
                        balance_card = balance_card + int(list(shopping_mall()[int(shopping_choice.split(':')[0])].values())[0])
                        print('您的额度不足,无法继续购物')
                        print('您的购物车:%s' % shopping_car)
                        print('您的余额:%s' % balance_card)
                    ask_shopping = input('是否退出购物"yes"or"no":')
                    if ask_shopping.split(':')[0] == 'yes':
                        print('您的购物车:%s' % shopping_car)
                        print('您的余额:%s' % balance_card)
                        print('您已经退出购物!')
                        break
                    else:
                        continue
            if ope_choice.split(':')[0] == '2':
                print('您目前的额度还有:%s' % balance_card)
                withdrawal_amount = input('提现的金额:')
                print('已经提现RMB:%s元' % withdraw(int(withdrawal_amount.split(':')[0])))
                balance_card = balance_card - int(withdrawal_amount.split(':')[0])
                print('剩余额度:%s' % balance_card)
            if ope_choice.split(':')[0] == '3':
                print('目前的剩余额度:%s' % balance_card)
                print(transfer_money(balance_card))
            if ope_choice.split(':')[0] == '4':
                quota = quota_func(15000) - balance_card
                if quota == 0:
                    print('未产生欠款!')
                else:
                    print('您目前所欠金额为:%s' % quota)
                    repay_money = input('还款:')
                    balance_card = balance_card + int(repay_money.split(':')[0])
                    print('您已经还款:%s' % repay_money.split(':')[0])
                    print('目前额度为:%s' % balance_card)
                    print('目前还欠款:%s' % (quota_func(15000) - balance_card))
            if ope_choice.split(':')[0] == '5':
                print('退出登陆!')
                exit()
    else:
        print('密码错误!')