# -*- coding:utf-8 -*-
# Author：sunmorg

import socket

phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print(phone)

phone.bind(('127.0.0.1',8080))  #0-65535   0-1024给操作系统用

phone.listen(5)  # 5表示最大挂起的链接数

print('starting...')
conn,client_add = phone.accept()

while True:
    data = conn.recv(1024) #1024 代表接收数据的最大数 单位是bytes
    print('客户端：',data)

    conn.send(data.upper())

conn.close()

phone.close()