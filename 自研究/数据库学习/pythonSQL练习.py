#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2020/1/19

import pymysql

# 连接数据库服务器
conn = pymysql.connect \
    (
        host='localhost',
        port=3306,
        user='root',
        password='root',
        database="lianxi",
        charset="utf8"
    )

# 获得交互用的游标对象
cursor = conn.cursor()

# # 通过游标对象发送语句 然后通过cursor对象的fetch来取数据
# cursor.execute("select * from students")
#
# # 取出所有数据
# a = cursor.fetchall()
# for item in a:
#     print(item)

# 插入新的数据
cursor.execute('''insert into class (name) values("中六班")''')
# 提交
conn.commit()

