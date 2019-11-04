import psutil
import os
import time





def get_net_speed():

    #t1时刻发送/接收字节总数
    t1_send = psutil.net_io_counters()[0]
    t1_recv = psutil.net_io_counters()[1]
    
    #等待10秒
    time.sleep(10)
    #t2时刻发送/接收字节总数
    t2_send = psutil.net_io_counters()[0]
    t2_recv = psutil.net_io_counters()[1]
    #t2-t1得到一秒内的上传速率B/S,单位换算Kb/s
    send_end = (t2_send-t1_send)/1000/10
    recv_end = (t2_recv-t1_recv)/1000/10

    up = ["上行","%0.1f" % send_end,"kb/s"]
    down = ["下行","%0.1f" % recv_end,"kb/s"]
    print(up)
    print(down)
    return [up,down]

while True:
    get_net_speed()
