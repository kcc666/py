#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2020/1/16

import socket,time,threading

# TCP服务器

# 1.创建套接字
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 2.绑定端口号
ip = "0.0.0.0"
port = 7630
server.bind((ip,port))

# 监听端口,最大连接数128
server.listen(128)

# # 阻塞等待连接着发送数据,收到一个请求时
# # 返回一个新的套接字,和请求客户端的地址
# print("-----等待客户端连接------")
# client_socket,clientAddr = server.accept()
# print("已有客户端连接,连接地址是:{}".format(clientAddr))
#
# # 阻塞等待客户端发送数据
# while 1:
#     recvdata = client_socket.recv(1024)
#     print(recvdata.decode("gbk"))
#     client_socket.send("你好".encode("GBK"))

def 接收连接():
    while 1:
        # client_socket,clientAddr = server.accept()
        t1 = threading.Thread(target=处理连接,args=(server.accept()))
        t1.start()

def 处理连接(client_socket,clientAddr):
    print(f"{clientAddr}已连接")

    try:
        while 1:
            recvdata = client_socket.recv(1024).decode("GBK")
            if recvdata == "":print("空消息")
            print(f"收到来自{clientAddr}的消息:{recvdata}")
            client_socket.send("你好~".encode("GBK"))
    except ConnectionAbortedError:
        print(f"{clientAddr}已断开连接")
        client_socket.close()


接收连接()