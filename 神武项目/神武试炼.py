import 工具,time



工具.打印("神武试练启动,获取窗口句柄...")
位置 = 工具.获取位置()

工具.打印("点击日程...")
工具.点击(位置["日程"])
time.sleep(1)

工具.打印("点击英雄试炼...")
工具.点击(位置["日程-英雄试炼"])
time.sleep(1)

工具.打印("点击我愿意接受试练...")
工具.点击(位置["我愿意接受试炼"])
time.sleep(3)

工具.打印(f"点击-试练-{工具.周几()}")
工具.点击(位置[f"试练-{工具.周几()}"])
time.sleep(1)

工具.打印("识别已挑战完成的...")
通关识别 = 工具.通关识别(工具.周几())


for i,v in enumerate(通关识别,start=1):
    if 通关识别[v]:print(f"当前第{i}关已挑战完成");continue
    点击位置 = 位置[f"试练-{工具.周几()}-{i}"]
    工具.打印(f"正在挑战第{i}关")
    工具.点击(点击位置)
    time.sleep(2)
    工具.点击(位置["试炼-挑战"])
    time.sleep(2)
    工具.判断战斗状态()
    time.sleep(2)

工具.打印("试练已全部挑战完毕")