# -*- coding:utf-8 -*-
# Author：sunmorg

import socket

phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print(phone)

phone.connect(('127.0.0.1',8080))  #0-65535   0-1024给操作系统用
while True:
    msg = input('>>:').strip()
    phone.send(msg.encode('utf-8'))
    
    data = phone.recv(1024)

    print('服务端：',data)

phone.close()