import socket
import os

os.system("cls")

def udp_send():

    while True:
        #拿到输入数据
        send_data = input("请输入数据:\n")

        #输入退出
        if(send_data == "exit"):
            break

        #发送数据,send(字节码,(IP地址,端口号))
        udp_socket.sendto(send_data.encode("gbk"),("127.168.31.132",9090))

    #关闭连接
    udp_socket.close()

def udp_accept():

    while True:

        #接收数据(接收到的消息,(发送方的IP,发送方端口))
        recv_data = udp_socket.recvfrom(1024)

        #提取消息并解码
        recv_msg = recv_data[0].decode("gbk")
        
        #提取发送方的地址信息
        recv_addr = str(recv_data[1])

        #打印消息
        print(recv_msg)


if(__name__ == "__main__"):

    #创建UDP套接字
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    #绑定套接字,一般用于双向通信时固定端口号
    udp_socket.bind(("",8888))

    #接收
    udp_accept()

    #发送
    # udp_send()
