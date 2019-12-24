import tkinter as tk


if __name__ == '__main__':
    window = tk.Tk()
    window.title('第一个window')
    window.geometry('300x200')

    var = tk.StringVar()
    num = 0
    var.set(str(num))
    l = tk.Label(window,textvariable=var,bg='#00d529',fg='#fff',font=('微软雅黑',12),width=15,height=2)


    # show_hidden = False

    def click_me():
        global num
        num+=1
        var.set(str(num))
        # print("你点击了一下函数")

    def sub():
        global num
        num-=1
        var.set(str(num))

    def clear():
        global num
        num = 0
        var.set(str(num))

    b = tk.Button(window,text='+1',width=15,height=2,command=click_me)

    b1 = tk.Button(window,text='-1',width=15,height=2,command=sub)

    b2 = tk.Button(window,text='c',width=15,height=2,command=clear)


    b.pack()
    l.pack()
    b1.pack()
    b2.pack()
    window.mainloop()
