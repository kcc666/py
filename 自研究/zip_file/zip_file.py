import zipfile
z = zipfile.ZipFile("v94.zip") # 这里的第二个参数用r表示是读取zip文件，w是创建一个zip文件
for f in z.namelist():
    z.extract(f,"")
z.close()