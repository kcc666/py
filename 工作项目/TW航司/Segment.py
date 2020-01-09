#! /usr/bin/env python
#coding:utf-8

from app.modular.BaseModel import BaseModel

class Segment(BaseModel):
    def __init__(self):
        self.SegmentCount = ""   ##航段号  去程1234  回程1234
        self.Carrier = ""   ##航司
        self.DepAirport = ""   ##出发机场
        self.DepTime = ""  # 日期时间，格式：YYYY-MM-DD HH:MM
        self.ArrAirport = ""   ##到达机场
        self.ArrTime = ""  # 日期时间，格式：YYYY-MM-DD HH:MM
        self.StopAirports = ""  ##经停地
        self.CodeShare = False   ##是否共享
        self.Cabin = ""   ##舱位
        self.FareBasis = ""   ##运价基础
        self.AircraftCode = ""  ##机型
        self.FlightNumber = ""  ##航班号
        self.OperatingCarrier = None  ##共享航司
        self.OperatingFlightNo = None  ##共享航班
        self.DepTerminal = ""   ##出发航站楼
        self.ArrTerminal = ""   ##到达航站楼
        self.CabinClass = 'Y'  # 舱位等级，Y代表经济舱，B代表商务舱，C代表头等舱,S代表超值经济舱
        self.BaggagePiece = 0  # 行李额件数
        self.BaggageWeigh = 0  # 行李额重量
        self.Duration = 0  ##飞行时间  int 分钟

