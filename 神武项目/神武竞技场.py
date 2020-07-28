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
        res = 工具.识别区域文字(位置["竞技场-剩余次数"])
        res = res.replace("\n","")
        工具.打印(f"竞技场剩余次数:{res}次")
        if "0" in res:break

        s = f"竞技场-挑战{random.randint(1,4)}"
        工具.打印(f"点击{s}")
        当前挑战点击 = 位置[s]
        工具.点击(当前挑战点击)
        time.sleep(2)

        工具.打印("点击自动")
        工具.点击(位置["自动按钮"])
        time.sleep(2)
        工具.判断战斗状态()
        time.sleep(5)
        if "1" in res :break

if __name__ == '__main__':
    # 工具.防掉线状态("2020-07-28 07:10")
    # time.sleep(2)
    竞技场()

