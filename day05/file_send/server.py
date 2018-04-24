# -*- coding:utf-8 -*-
# Author：sunmorg
import socket
phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
phone.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

phone.bind(('127.0.0.1',8080))  #0-65535   0-1024给操作系统用
phone.listen(5)  # 5表示最大挂起的链接数

print('starting......')
while True:
    conn,client_addr=phone.accept()

    while True:
        try:
            pass
        except ConnectionResetError:
            break