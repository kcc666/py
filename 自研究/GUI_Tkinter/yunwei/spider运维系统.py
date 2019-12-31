#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2019/12/23

import tkinter as tk
import time

class yunwei():
    def __init__(self):

        # 初始化一个窗口
        self.win = tk.Tk()

        # 设置窗口大小
        self.win.geometry("600x600+1200+100")

        # 公共变量
        self.screenText = "▍"
        self.system_info = tk.StringVar() #对象
        self.system_info.set(self.screenText) #默认值

    def main(self):
        self.ButtonCreater("重启 Python",[40,300],self.ReStartPy)
        self.ButtonCreater("重启 Spider",[40,400],self.RestartCS)
        self.LabelCreater(self.system_info,[0,0])
        self.win.mainloop()


    #---------按钮生成器-----------
    def ButtonCreater(self,text,position,cmd):
        # print(text,position,cmd)
        btn = tk.Button(self.win
                           ,text=text
                           ,activeforeground="#fff"
                           ,activebackground="#716186"
                           ,bd=2
                           ,bg="#663366"
                           ,fg="#fff"
                           ,font=("微软雅黑",14)
                           ,width=20
                           ,height=1
                           ,command=cmd
                           )
        btn.place(x=position[0],y=position[1])
    #---------文本生成器-----------
    def LabelCreater(self,text,position):
        text = tk.Label(self.win
                        , font=("微软雅黑", 14)
                        ,textvariable=text
                        ,width=50
                        ,height=10
                        ,bg="#BDABA9")

        text.place(x=position[0],y=position[1])



    #---------按钮功能区-----------

    def ReStartPy(self):
        self.screenText  +="▍"
        self.system_info.set(self.screenText)
        pass
    def RestartCS(self):
        self.screenText += "c#\n"
        self.system_info.set(self.screenText)

        pass

if __name__ == '__main__':
    yunwei().main()