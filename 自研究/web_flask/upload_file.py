from flask import Flask, request  # 导入request对象
import os
app = Flask(__name__)


@app.route("/", methods=["GET"])
def get():
    return'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
            <h1>文件上传示例</h1>
            <form action="./upload" enctype='multipart/form-data' method='POST'>
                <input type="file" name="pic">
                <input type="submit" value="上传">
            </form>
        </body>
        </html>
    '''

@app.route("/upload", methods=["POST"])
def upload():
    file_obj = request.files.get("pic")  # "pic"对应前端表单name属性
    print(request.files)
    filename = file_obj.filename #文件名
    # print(filename)
    if file_obj is None:
        # 表示没有发送文件
        return "未上传文件"
 
    # 将文件保存到本地
    # # 1. 创建一个文件
    # f = open("./demo.png", "wb")
    # # 2. 向文件写内容
    # data = file_obj.read()
    # f.write(data)
    # # 3. 关闭文件
    # f.close()
 
    # 直接使用上传的文件对象保存
    file_obj.save("./demo1.png")
    return "上传成功"
 
 
if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=80, debug=True)
    with open("aa.txt","w",encoding="utf8")as f:
        f.write("111")
    print("*"*30)
    print("工作目录目录:",os.getcwd())
    print("绝对路径",__file__)
    print("文件所在目录",os.path.dirname(__file__))
    print("*"*30)

