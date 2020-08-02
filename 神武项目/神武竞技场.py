import 工具,time,random




def 竞技场():

    工具.打印("获取窗口句柄...")
    位置 = 工具.获取位置()

    工具.打印("点击日程...")
    工具.点击(位置["日程"])
    time.sleep(1)

    工具.打印("点击竞技场...")
    工具.点击(位置["日程-竞技场"])
    time.sleep(1)

    while 1:

        res = 工具.识别区域文字(位置["竞技场-剩余次数"]).replace("\n","")

        工具.打印(f"竞技场剩余次数:{res}次")

        if "0" in res:工具.打印("今天的竞技场次数已用完"); break



        s = f"竞技场-挑战{random.randint(1,4)}"
        工具.打印(f"点击{s}")
        当前挑战点击 = 位置[s]
        工具.点击(当前挑战点击)
        time.sleep(2)

        工具.打印("点击自动")
        工具.点击(位置["自动按钮"])
        time.sleep(2)
        工具.判断战斗状态()
        time.sleep(8)

        #关闭战败
        工具.点击(位置["竞技场-战败提示-关闭"])
        time.sleep(2)

        工具.打印("刷新对手")
        工具.点击(位置["竞技场-刷新对手"])
        time.sleep(5)

        #判断任务是否执行完,(竞技场次数用完时,竞技场窗口会自动关系)
        if "今日" not in 工具.识别区域文字(位置["竞技场-今日收益"]):
            time.sleep(3)
            if "今" not in 工具.识别区域文字(位置["竞技场-今日收益"]):

                工具.打印("今天的竞技场次数已用完")
                break


if __name__ == '__main__':
    # 工具.防掉线状态("2020-07-28 07:10")
    # time.sleep(2)
    竞技场()

