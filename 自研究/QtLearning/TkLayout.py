import tkinter as tk


if __name__ == '__main__':
    window = tk.Tk()
    window.title('第一个window')
    window.geometry('300x300')

    xx=0

    var = tk.IntVar()
    var.set(xx)
    def a():
        global xx
        xx+=1
        b.place(x=xx,y=0)
        var.set(xx)

    b = tk.Button(window, textvariable=var, width=15, height=2,command=a)
    b.place(x=0,y=0)

    window.mainloop()
