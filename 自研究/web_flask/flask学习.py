from flask import Flask,request

app = Flask("my_app")
# print(Flask.__doc__)

#接收上传的文件
app.config['UPLOAD_FOLDER'] = "upload_file"

app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'} 

@app.route('/')
def hello_world(): #当访问根目录时,返回get请求的参数

    #请求的路径不包域名
    print("*"*30)
    #请求的资源路径
    print(request.path) 
    #请求过来的参数
    print(request.full_path) 
    #get请求下的bb对应的值,如果没有就返回None,第二个参数设置默认值
    print(request.args.get('bb',"无bb"))

    print("*"*30)
    return request.args

@app.route('/post',methods=['POST'])
def post():

    #post请求头
    print(request.headers) 
    #post请求体二进制
    # print(request.stream.read()) 
    #请求体键值对
    print(request.form)
    #根据键取请求体的值
    print(request.form['name'])
    #根据键取请求体的值
    print(request.form.get('name'))
    return 'welcome'




#启动,并且端口为80
app.run(debug=True,port=80)