# -*- coding:utf-8 -*-
# Author：sunmorg

from socket import *

server = socket(AF_INET,SOCK_DGRAM)
server.bind(('127.0.0.1',8080))

# server.listen(5)
# server.accept()
while True:
    data,client_addr = server.recvfrom(1024)
    print(data)
    server.sendto(data.upper(),client_addr)

server.close()