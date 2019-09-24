import socket
import psutil
import time

# 发送数据的函数


def send(addr):

    data = {
        'process': get_process('Spider.exe'),
        'cpustate': get_cpu_state(),
        'memorystate': get_memory_state(),
        'computername': get_computer_name(),
    }

    # 创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 发送数据
    udp_socket.sendto(str(data).encode('utf8'), addr)

# 获得传入的进程数
def get_process(processname):
    # 检测进程数量
    count = 0
    # 获得一个列表里面存放了所有运行的进程的id
    pl = psutil.pids()
    # 遍历
    try:
        for pid in pl:
            if(psutil.Process(pid).name() == processname):
                count += 1
        return count
    except:
        get_process(processname)

# 获得CPU使用率
def get_cpu_state():
    return str(psutil.cpu_percent(1))

# 获得内存使用率
def get_memory_state():
    phymem = psutil.virtual_memory()
    # line = "Memory: %5s%% %6s/%s"%(
    #     phymem.percent,
    #     str(int(phymem.used/1024/1024))+"M",
    #     str(int(phymem.total/1024/1024))+"M"
    # )
    return [phymem.percent, str(int(phymem.used/1024/1024))+"M", str(int(phymem.total/1024/1024))+"M"]

# 获得计算机名
def get_computer_name():
    return socket.gethostname()

def main():
    # 声明发送地址
    addr = ('106.15.53.80', 8989)
    while True:
        try:
            send(addr)
            print("(发送数据)")
        except:
            send(addr)
        time.sleep(10)
if __name__ == '__main__':
    main()
