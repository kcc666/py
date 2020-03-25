#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2020/1/16

import socket,threading,time

# 客户端


# 创建套接字
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 连接到客户端
ip = '106.15.53.80'
port = 9188
client.connect((ip,port))

# 多线程发送数据
def send(sock):
    while 1:
        data = input("请输入你要发送的内容:\n")
        client.send(data.encode("utf8"))
# 多线程接收数据
def recv(sock):
    while 1:
        print(client.recv(1024).decode("gbk"))

threading.Thread(target=send,args=(client,)).start()
threading.Thread(target=recv,args=(client,)).start()

print("程序等待了嘛?")