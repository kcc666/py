import 神武竞技场,神武试炼,time,traceback,神武宝图


while 1:

    try:
        r = input("神武竞技场请输入1\n神武试炼请输入2\n神武宝图请输入3\n输入完后按回车开始:\n")
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
        else:
            print("你的输入无效,请重新输入")
    except Exception as e:
        print(traceback.format_exc())
        input("程序错误,按任意键退出")