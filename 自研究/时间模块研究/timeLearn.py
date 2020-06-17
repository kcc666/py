#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kcc time:2019/12/6

import time




# 时间元组的两个参数
# tm_wday代表星期,(中国)0是星期六,1是星期日....
# tm_yday 表示该日期在该年的第几天

# 时间字符串
time_str = "2017-12-31"
print(time_str)

# 时间字符串转换为时间元组,
time_struct = time.strptime(time_str,"%Y-%m-%d")
print(time_struct)

# 时间元组转换为时间戳
time_stamp = time.mktime(time_struct)
print(time_stamp)

# 时间戳转换为时间元组
time_struct2 = time.localtime(time_stamp)
print(time_struct2)

# 时间元组转为时间字符串
time_str2 = time.strftime("%Y-%m-%d %H:%M:%S",time_struct2)
print(time_str2)

# 时间戳转为时间字符串
print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(2000000000)))