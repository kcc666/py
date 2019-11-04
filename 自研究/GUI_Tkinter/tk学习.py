import tkinter


root = tkinter.Tk() #创建一个窗口对象

def cc():
    print("nihao")

#按钮样式
btn1_style = {
    "activebackground":"blue", #点击按钮时,按钮的背景色
    "activeforeground":"#fff", #点击按钮时,按钮的前景色(字体颜色)
    "text":"hello!kcc", #按钮上的文字
    "bd":"4", #按钮的边框大小
    "bg":"#ffb123", #按钮的背景色
}

#创建按钮对象,root是刚才创建的窗体,btn1_style是样式,command是点击按钮时的事件
btn1 = tkinter.Button(root,btn1_style,command=cc)
text1 = tkinter.Text(root,text = "你好")

#将按钮生成并打包到窗体上
btn1.pack()
text1.pack()
root.mainloop() #使窗口对象保持

