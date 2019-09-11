import socket
import os
# socket 服务器端

os.system("cls")

# 创建套接字
tcp_server_socket =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 绑定基本信息
tcp_server_socket.bind(("",7890))

#设置监听模式(最大连接数)
tcp_server_socket.listen(128)

#阻塞式接收,返回元组,1.回信息专用的套接字,2.客户端的地址
new_client_socket,client_addr = tcp_server_socket.accept()

#提取客户端发送过来的信息
recv_data = new_client_socket.recv(1024)
print(recv_data.decode("gb2312"))

#回复请求
new_client_socket.send("收到".encode('gb2312'))

#关闭套接字
new_client_socket.close()
tcp_server_socket.close()