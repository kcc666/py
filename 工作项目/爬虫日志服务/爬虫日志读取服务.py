#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2020/1/21

from flask import Flask, request
import pymysql,time,json,threading,datetime
import queue,traceback
from flask_cors import *


class Readlog():
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

    def getlog(self,req):
        print(req)
        retnum = self.cursor.execute('''select * from {} where timestamp>{} and timestamp<{};'''
                                .format(req["airname"],req["start"],req["end"]))

        ret_data = {
            "code":0,
            "msg":"",
            "count":retnum,
            "data":[]
        }


        data_all = self.cursor.fetchall()
        for line in data_all:
            print(type(line[6]))
            linedict = {
                "id":line[0],
                "hostname":line[1],
                "time":line[2].strftime('%Y-%m-%d %H:%M:%S'),
                "airname":line[3],
                "dep":line[4],
                "arr":line[5],
                "date":line[6].strftime('%Y-%m-%d'),
                "currency":"CNY" if line[7]=="" else line[7],
                "adultnum":line[8],
                "statucode":line[9],
                "timing":line[10],
                "resultnum":line[11],
                "ip":line[12],
                "port":line[13],
                "timestamp":line[14],
                "message":line[15]
            }
            ret_data["data"].append(linedict)
        return ret_data


getlog_app = Flask(__name__)
getlog_app.config['JSON_AS_ASCII'] = False

reader = Readlog()

@getlog_app.route('/getlog')
@cross_origin()
def getlog():
    req = {
        "airname":request.args.get("airname"),
        "start":request.args.get("start"),
        "end":request.args.get("end"),
        "statu":request.args.get("statu")
    }
    return json.dumps(reader.getlog(req))

if __name__ == '__main__':
    getlog_app.run(host="0.0.0.0", port=7003, debug=True)