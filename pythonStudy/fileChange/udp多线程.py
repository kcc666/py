from socket import *
from threading import Thread
# import yanjiu

udp_socket = socket(AF_INET,SOCK_DGRAM)
udp_socket.bind(('',8989))

def recv_fun():
    while True:
        recv_data = udp_socket.recvfrom(1024)
        print(recv_data[0].decode('gb2312'))


def send():
    while True:
        addr = ('106.15.53.80',9001)
        data = input('请输入:\n')
        udp_socket.sendto(data.encode('utf8'),addr)


t1 = Thread(target=send)
t2 = Thread(target=recv_fun)

t1.start()
t2.start()
t1.join()
t2.join()

