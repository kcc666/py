def say_hi():
    print("你好啊")
    return ""

while 1:
    i = input("请输入一个数")

    say = {
        "1": "hello",
        "2": "你好",
        "3": say_hi()
    }
    try:
        print(say[i])
    except:
        print("你输入的啥玩意?")

