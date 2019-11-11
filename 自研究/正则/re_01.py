import os,re
os.system("cls")
print("*"*30)

# b = 0
# with open("abc.txt","r")as f:
#     for i in f:
#         if i.startswith("bb") and i.endswith("bb\n"):
#             print(i)

with open("test.html","rb")as f:
    text = f.read().decode("utf8")
    re_text = re.findall("name: 'FPS'([\d\D]*?)疑似卡顿点",text)[0]
    re_text1 = re.findall("data: \[[\d\D]*?\]",re_text)[0]
    print(re_text1)


print("*"*30)




