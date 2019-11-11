import re,os,json

print('*'*40)

with open("text.txt","rb")as f:
    txt = f.read().decode("utf8")
    # print(txt)
    list_all = []
    re_1 = re.findall("\w+\s*=\s*.*?,",txt)
    for i in re_1:
        re_2 = i.replace("{","").replace(",","")
        # print(re_2)
        re_3 = re.findall("\w+=.*",re_2)
        # print(re_3,"**re3",len(re_3))
        if len(re_3)==1:
            list_all.append(re_3[0])
        else:
            list_all.append(re_2)
        # print('*'*40)
    # print(list_all)
    for a in list_all:
        print(a)
# json.dumps()

print('*'*40)