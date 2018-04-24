# -*- coding:utf-8 -*-
# Author：sunmorg

import socketserver, os
from usermanagement import useropr
from server import MyTCPHandler

info = '''
        1、启动服务器
        2、进入用户管理
        按q退出
'''

if __name__ == '__main__':
    while True:
        print(info)
        choice = input('>>>:')
        if choice == 'q':
            exit()
        elif choice == '1':
            ip, port = '0.0.0.0', 9999
            server = socketserver.ThreadingTCPServer((ip, port), MyTCPHandler)
            server.serve_forever()
        elif choice == '2':
            useropr.interactive()
        else:
            continue