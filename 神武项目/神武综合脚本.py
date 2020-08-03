import 神武竞技场,神武试炼,time,traceback,神武宝图,神武科举


while 1:

    try:


        print("----------神武综合辅助----------")
        print("神武竞技请输入         1")
        print("神武试练请输入         2")
        print("神武宝图请输入         3")
        print("神武科举请输入         4")
        r = input("请输入:输入后按回车键确定:")


        if r == "1":
            print("8秒后开始执行神武竞技场,过程中请勿操作鼠标")
            time.sleep(8)
            神武竞技场.竞技场()
        elif r == "2":
            print("8秒后开始执行神武试练,过程中请勿操作鼠标")
            time.sleep(8)
            神武试炼.英雄试练()
        elif r == "3":
            print("8秒后开始执行宝图任务,过程中请勿操作鼠标")
            time.sleep(8)
            神武宝图.开始宝图()
        elif r == "4":
            print("开始神武科举,按ctrl+c退出该功能")
            神武科举.开始科举()


        else:
            print("你的输入无效,请重新输入")
    except Exception as e:
        print(traceback.format_exc())
        input("程序错误,按任意键退出")