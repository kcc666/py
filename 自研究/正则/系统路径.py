#coding = utf8
import os,re,random,time
os.system("cls")
print("*"*30)


#re.math方法从字符串开头开始匹配,没有则返回None
# math_str = "823232eesay2331dadasda"
# r_math = re.match("\d+",math_str).group()
# print(r_math) #823232

#re.search返回第一个成功找到的匹配
# search_str = "sdwqewqfCfcffsafwqeqwdwww.w.w.comewqewqer"
# r_search = re.findall("[cC]f",search_str)
# print(r_search) 

print("当前工作路径:",os.getcwd())
print("当前文件路径:",__file__)
print("当前文件所在目录:",os.path.dirname(__file__))
# print(os.chdir.__doc__)

file_in = os.path.dirname(__file__)
os.chdir(file_in)

print("当前工作路径:",os.getcwd())
print("*"*30)
