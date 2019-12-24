import tkinter as tk


class app():
    def __init__(self):
        self.window = tk.Tk()


        self.window.title('第一个window')
        self.window.geometry('600x600')

        self.var = tk.IntVar()
        self.num = 0
        self.var.set(self.num)


    def labelCreater(self):
        l = tk.Label(self.window,textvariable=self.var,bg='#00d529',fg='#fff',font=('微软雅黑',12),width=15,height=2)
        l.pack()

    def btnCreater(self,text,cmd):
        b = tk.Button(self.window, text=text, width=15, height=2, command=cmd)
        b.pack()

    def add(self):
        self.num+=1
        self.var.set(self.num)

    def sub(self):
        self.num-=1
        self.var.set(self.num)

    def clear(self):
        self.num = 0
        self.var.set(self.num)


    def main(self):
        self.btnCreater("+1",self.add)
        self.labelCreater()
        self.btnCreater("+1",self.sub)
        self.btnCreater("C",self.clear)
        self.window.mainloop()

app().main()