import socket
import re

def client_exec(client):
    
    print(client.send)
    # 获取用户发送的数据(请求头)
    # --------------------------------------------
    recv_data = client.recv(1024).decode('utf-8')
    print('-----------------请求头-----------------')
    print(recv_data)
    # --------------------------------------------



    
    # 在请求头中提取用户(请求的地址)
    # group(0)代表请求方式,group(1)代表请求地址
    # --------------------------------------------
##    match = re.match('[^/]+(/[^ ]*) ', recv_data)
##    recv_path = match.group(1)
##    #print('-----------------请求路径-----------------')
##    print(recv_path)
##    print('-'*40)
    # --------------------------------------------





    # 设置响应行&响应头
    # --------------------------------------------
    response_line = 'HTTP/1.1 200 OK\r\n'
    response_head = 'Content-Type: application/javascript; charset=utf-8\r\n'
    # --------------------------------------------




    # 读取资源,赋值响应体
    # -------------------------------------------
    try:
        with open ('all.txt','r')as f:
            data = f.read()
            response_body = 'success('+str(data)+')'
            #response_body = data
    except:
        response_body = 'success("未找到该地址")'
    # -------------------------------------------
    



    # 响应报文&发送数据&关闭客户端
    response_data = response_line + response_head + '\r\n' + response_body
    client.send(response_data.encode('utf-8'))
    client.close()


    
 
def main():
    # 初始化套接字
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    # 綁定ip地址和端口(重用)
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    tcp_server.bind(('', 9001))
 
    # 设置被动模式
    tcp_server.listen(128)
 
    # 循环接收用户请求
    while True:
        print(tcp_server.accept())
        client, address = tcp_server.accept()
        
        client_exec(client)
        
    # 关闭
    tcp_server.close()
 
 
if __name__ == '__main__':
    print('接口程序，供调用以返回VPS服务器状态，请勿关闭')
    main()
