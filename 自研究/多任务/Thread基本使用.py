#coding = utf-8

import time
import os
import threading


def sing():
    for i in range(1, 8):
        print("唱~", i)
        time.sleep(0.5)


def dance():
    for i in range(1, 6):
        print("跳~", i)
        time.sleep(0.5)


def main():
    os.system("cls")
    # 并发与并行的概念
    # 并发指的是任务数大于CPU核心数
    # 并行指的是任务数小于等于CPU核心数

    # t1.start 表示开启一个子线程
    # 主线程会等待子线程执行完毕
    # 线程执行的顺序不确定

    t1 = threading.Thread(target=sing)
    t2 = threading.Thread(target=dance)
    t1.start()
    t2.start()

    while True:
        os.system("cls")
        print(len(threading.enumerate()))
        time.sleep(0.3)


if __name__ == "__main__":
    main()
