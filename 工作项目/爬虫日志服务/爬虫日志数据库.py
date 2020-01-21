#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2020/1/20

from flask import Flask, request
import pymysql,time,json,threading
import queue,traceback



class SaveLog():
    def __init__(self):

        self.conn = pymysql.connect \
            (
                host='127.0.0.1',
                port=3306,
                user='root',
                password='root',
                database="py3flask",
                charset="utf8"
            )

        self.cursor = self.conn.cursor()

        self.que = queue.Queue()

        threading.Thread(target=self.requestHandle).start()

    def requestHandle(self):

        while 1:
            jsondata = self.que.get()
            print("----------------------")
            print("收到一个请求")
            # 收到请求后先处理为Dict
            data = json.loads(jsondata.decode("utf8"))
            # print(data)
            # 提取post数据的航司,看数据库中有无该航司的表
            airname = data["airname"]
            print("航司名{}".format(airname))

            tableNum = self.cursor.execute('''show tables like '{}'; '''.format(airname))

            # 如果不存在航司对应的表则创建表
            if tableNum == 0:self.createTable(airname)

            # 存在表,存储数据
            self.saveData(data)

    def createTable(self,tablename):
        print("表不存在,创建表:{}",tablename)
        '''根据名字建表'''
        self.cursor.execute(
            '''
            create table {}(
            id          int unsigned primary key auto_increment not null,
            hostname    varchar(30),
            time        datetime,
            airname     varchar(10),
            dep         varchar(3),
            arr         varchar(3),
            date        date,
            currency    varchar(5),
            adultnum    tinyint unsigned,
            statucode   smallint,
            timing      float,
            resultnum   tinyint unsigned,
            ip          varchar(15),
            port        smallint,
            timestamp   int unsigned,
            message     varchar(3000)
            );
            '''
                .format(tablename))

    def saveData(self,data):
        print("表已创建,存储数据")
        try:
            sql =\
            '''
            insert into {tablename} values
            (
            0,
            "{hostname}",
            "{time}",
            "{airname}",
            "{dep}",
            "{arr}",
            "{date}",
            "{currency}",
            {adultnum},
            {statucode},
            {timing},
            {resultnum},
            "{ip}",
            {port},
            {timestamp},
            '{message}'
            );
            
            '''.format(
                tablename = data["airname"],
                hostname =  data["hostname"],
                time = time.strftime("%Y-%m-%d %X"),
                airname = data["airname"],
                dep = data["dep"],
                arr = data["arr"],
                date = data["date"],
                currency = data["currency"],
                adultnum = data["adultnum"],
                statucode = data["statucode"],
                timing = data["timing"],
                resultnum = data["resultnum"],
                ip = data["ip"],
                port = data["port"],
                timestamp = time.time(),
                message = pymysql.escape_string(data["message"])
            )


            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            with open("except.txt","a") as f:
                f.write('----------------------------------\n')
                f.write(time.strftime("%Y-%m-%d %X")+"|"+traceback.format_exc())





saver = SaveLog()


app =  Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/pushlog',methods=['POST'])
def pushLog():
    msg = request.stream.read()
    saver.que.put(msg)
    return msg





if __name__ == '__main__':

    app.run(host="0.0.0.0", port=7002, debug=True)





    send = {
        "hostname":"LJ888999",
        "airname":"Tway",
        "dep":"ICN",
        "arr":"NRT",
        "statucode":"200",
        "date":"2020-02-12",
        "currency":"CNY",
        "audltnum":"1",
        "timing":"3.3",
        "resultnum":"1",
        "ip":"123.8.7.4",
        "port":"1233",
        "message":"成功!"
    }