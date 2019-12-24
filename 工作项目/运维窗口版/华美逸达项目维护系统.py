#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2019/12/24

import time,requests
import tkinter as tk

class Himyidea():
    def __init__(self):

        # 窗口对象
        self.win = tk.Tk()

        # 设置大小
        self.win.geometry("600x300+1200+100")

        # python项目变量
        LocalPyVersion = "v43" # 本地版本号
        self.LPV = tk.StringVar()
        self.LPV.set(LocalPyVersion)




        # C#项目变量
        LocalCsVersion = ""
        self.LCV = tk.StringVar()



    def main(self):

        py_t1 = tk.Label(self.win, text="python项目版本:" ,font=("微软雅黑",14))
        py_t1.place(x=20,y=20)

        py_t2 = tk.Label(self.win, text="C#项目版本:", font=("微软雅黑", 14) )
        py_t2.place(x=200, y=20)

        self.win.mainloop()





if __name__ == '__main__':
    Himyidea().main()
