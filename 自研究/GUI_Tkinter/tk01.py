from tkinter import *

win = Tk() #声明一个根窗口

#设置窗口标题
win.title("DirectSpider 维护工具")

#设置窗口大小
win.geometry("600x380+100+100")

#设置一个可变的变量

var = StringVar()
var.set("行楷")

#创建一个label并打包
label1 = Label(win,
    textvariable=var,
    bg="#261C1A",
    fg="#E6E6E6",
    font=("楷体",20),
    anchor="nw"
    )
label1.pack(expand="yes",fill="both")

#启动主窗口
win.mainloop() 