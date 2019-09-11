from socket import *
import json
import time 
import os
from threading import Thread

udp_socket = socket(AF_INET,SOCK_DGRAM)
udp_socket.bind(('',8989))

def recv_fun():
    
    while True:
        recv_data = udp_socket.recvfrom(1024)
        data = recv_data[0].decode('utf8')
        objdata = eval(data)
        computername = objdata['computername']
        objdata['time'] = time.strftime("%Y-%m-%d %X",time.localtime())
        with open('d:/vpsFile/vpsServerState/'+computername+'.txt','w') as f:
            f.write(json.dumps(objdata))
            print(computername,time.strftime("%Y-%m-%d %X",time.localtime()))

def saveAllList():
  while True:
    time.sleep(10)
    print('打包数据')
    print(time.strftime("%Y-%m-%d %X",time.localtime()))
    #获取目标文件夹的路径 
    meragefiledir = os.getcwd()

    #获取当前文件夹中的文件名称列表 
    filenames=os.listdir(meragefiledir)
    filename_txt = []
    for item in filenames:
        if item.endswith('.txt'):
            filename_txt.append(item)
        
    #打开当前目录下的all.txt文件，如果没有则创建
    file=open('all.txt','w') 
    #向文件中写入字符 
    file.write('[')
    # #先遍历文件名 
    for filename in filename_txt: 
      for line in open(filename):
        file.writelines(line) 
      file.write(',\n') 
    file.write(']')

    file.seek(1,0)
    file.write(' ')
    #关闭文件 
    file.close() 


    
    

  

print('用于接收VPS服务器状态数据，请勿关闭')
t1 = Thread(target=recv_fun)
t2 = Thread(target=saveAllList)

t1.start()
t2.start()
t1.join()
t2.join()
