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

        # python项目


        # C#项目




    def main(self):

        py_t1 = tk.Label(self.win, text="Py本地版本:" ,font=("微软雅黑",14))
        py_t1.place(x=20,y=20)

        cs_t1 = tk.Label(self.win, text="C#本地版本:", font=("微软雅黑", 14) )
        cs_t1.place(x=250, y=20)

        self.win.mainloop()

    def get_local_version(self,name):
        with open("version.json","r")as f:
            print(f.read())




if __name__ == '__main__':
    Himyidea().main()
