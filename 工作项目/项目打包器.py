# -*- coding:utf-8 -*-
# author: kcc time:2019/12/31

import os,time,requests
import shutil,zipfile

def get_version():
    try:
        r = requests.get("http://106.15.53.80:56789/pyProject/newVersion.txt")
        print("线上版本:{}".format(r.text))
    except:
        print("获取最新版本错误")
def zip_yasuo(start_dir):
    file_news = start_dir + '.zip'
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(start_dir):
        file_path = dir_path.replace(start_dir, '')
        file_path = file_path and file_path + os.sep or ''
        for filename in file_names:
            z.write(os.path.join(dir_path, filename), file_path+filename)

    # print(start_dir)
    z.close()

def copy_dir(v):
    '''将一个目录下的全部文件和目录,完整地<拷贝并覆盖>到另一个目录'''
    # yuan 源目录
    # target 目标目录
    target = "C:\\Users\\46321\Desktop\临时"
    yuan = "d:/work_py/hmyd_flask_scrapy"

    if not os.path.exists(os.path.join(target,v,v)):os.makedirs(os.path.join(target,v,v))
    else:print("版本目录已存在");return
    target = os.path.join(target,v,v)



    if not (os.path.isdir(yuan) and os.path.isdir(target)):
        # 如果传进来的不是目录
        print("传入目录不存在")
        return
    try:
        for a in os.walk(yuan):
            # 递归创建目录
            for d in a[1]:
                dir_path = os.path.join(a[0].replace(yuan, target), d)
                if not os.path.isdir(dir_path):
                    if ".git" in dir_path: continue
                    if ".idea" in dir_path: continue
                    if "__pycache__" in dir_path: continue
                    os.makedirs(dir_path)
            # 递归拷贝文件
            for f in a[2]:
                dep_path = os.path.join(a[0], f)
                arr_path = os.path.join(a[0].replace(yuan, target), f)
                # print(dep_path)
                if ".git" in dep_path:continue
                if ".idea" in dep_path:continue
                if "__pycache__" in dep_path:continue
                if "chromedriver.exe" in dep_path:continue
                shutil.copy(dep_path, arr_path, follow_symlinks=True)
        # zip_yasuo(os.path.join(target,os.path.pardir))
        # print("C:\\Users\\46321\Desktop\临时")
        print("打包完毕")
    except BaseException as e:
        print(e)
        print("文件打包失败")






print("*"*25)
get_version()
v = input("请输入版本号:")
copy_dir(v)
zip_yasuo(os.path.join("C:\\Users\\46321\Desktop\临时",v))
shutil.rmtree(os.path.join("C:\\Users\\46321\Desktop\临时",v))

print("*"*25)
print("\n\n\n\n3秒后关闭本窗口....")
time.sleep(3)
