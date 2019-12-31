#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2019/12/25

from flask import Flask,request
from flask_cors import *
import json,time
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

data_all = {}

@app.route('/')
def recv():
    # 计算机名
    cpn = request.args.get('cpn','nothing')
    # cpu状态
    cpu = request.args.get('cpu','nothing')
    # 内存,占用,总量
    m1 = request.args.get('m1','nothing')
    m2 = request.args.get('m2','nothing')
    m3 = request.args.get('m3','nothing')
    # 带宽利用率
    up = request.args.get('up','nothing')
    down = request.args.get('down','nothing')
    # 服务器类型
    ctype = request.args.get('type','nothing')
    # py版本
    pyv = request.args.get('pyv','nothing')
    # c#版本
    csv = request.args.get('csv','nothing')

    data_all[cpn] = '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(cpu,m1,m2,m3,up,down,ctype,pyv,csv,int(time.time()))

    return "success"

@app.route('/vpsinfo')
@cross_origin()
def secv():
    return json.dumps(data_all)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=7001)