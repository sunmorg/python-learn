# -*- coding:utf-8 -*-
# Author：sunmorg

import socket

phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
phone.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

phone.bind(('127.0.0.1',8080))  #0-65535   0-1024给操作系统用
phone.listen(5)  # 5表示最大挂起的链接数

print('starting...')
conn,client_add = phone.accept()

while True:
    try:
        data = conn.recv(1024)
        if not data:break
        print('客户端：',data)

        conn.send(data.upper())
    except ConnectionResetError:
        break
conn.close()

phone.close()