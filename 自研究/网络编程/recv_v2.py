#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2020/1/17

import socket,time,threading,psutil,os,requests,json,traceback

class Recv():
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 9188
    def main(self):
        # 开启服务
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((self.ip,self.port))
        self.server.listen(128)


        client_socket, clientAddr = self.server.accept()
        threading.Thread(target=self.clientHandle,args=(client_socket,)).start()


    def clientHandle(self,client):
        print("建立连接")
        while 1:
            recv_data = client.recv(4096).decode()
            print(recv_data)
if __name__ == '__main__':
    Recv().main()