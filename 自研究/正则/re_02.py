import re
import time

with open("text.txt","rb")as f:
    text = f.read().decode("utf8")
    # print(text)
    #最终匹配到的属性在此列表
    data_all = []
    re_ = re.findall(".*\s",text)
    print("*"*30)
    for i in re_:
        # print("当前行内容:",i)
        try:
            re_1 = re.findall("[a-zA-z]+",i)[0]
            print("当前行匹配到的内容",re_1)
            data_all.append(re_1)
        except:
            pass
    print("*"*30)
    print(data_all)
    print("*"*30)
