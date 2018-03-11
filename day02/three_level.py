# -*- coding:utf-8 -*-
# Author：sunmorg

menu = {
    '北京':{
        '海淀':{
            '五道口':{
                'soho':{},
                '网易':{},
                'google':{}
            },
            '中关村':{
                '爱奇艺':{},
                '汽车之家':{},
                'youku':{},
            },
            '上地':{
                '百度':{},
            },
        },
        '昌平':{
            '沙河':{
                '老男孩':{},
                '北航':{},
            },
            '天通苑':{},
            '回龙观':{},
        },
        '朝阳':{},
        '东城':{},
    },
    '上海':{
        '闵行':{
            "人民广场":{
                '炸鸡店':{}
            }
        },
        '闸北':{
            '火车战':{
                '携程':{}
            }
        },
        '浦东':{},
    },
    '山东':{},
}

exit_flag = False

while not exit_flag:
    for key_one in menu:
        print(key_one)
    choice_one = input("请您选择第一级菜单（按q可退出）：")
    if choice_one in menu:
        while not exit_flag:
            for key_two in menu[choice_one]:
                print(key_two)
            choice_two = input("请您选择第二级菜单（按b可返回上一层，按q可退出）：")
            if choice_two in menu[choice_one]:
                while not exit_flag:
                    for key_three in menu[choice_one][choice_two]:
                        print(key_three)
                    choice_three = input("请您选择第三级菜单（按b可返回上一层，按q可退出）：")
                    if choice_three in menu[choice_one][choice_two]:
                        while not exit_flag:
                            for key_four in menu[choice_one][choice_two][choice_three]:
                                print(key_four)
                            choice_four = input("最后一级菜单，输入b返回上一层，输入q退出程序：")
                            if choice_four == 'b':
                                break
                            elif  choice_four == 'q':
                                exit_flag = True
                            else:
                                print('没有下一级啦！')
                    if choice_three == 'b':
                        break
                    elif choice_three == 'q':
                        exit_flag = True
                    else:
                        print('您选择的菜单我们没有，请重新选择')
            else:
                print('您选择的菜单我们没有，请重新选择！')
            if choice_two =='b':
                break
            elif choice_two == 'q':
                exit_flag = True
    if choice_one == 'q':
        exit_flag = True
    else:
        print('您选择的菜单我们没有，请重新选择！')