#! /usr/bin/env python
# coding:utf-8
from BaseModel import BaseModel

class DefaultConfig:
    DEBUG = False

##请求参数
class AirRequest(BaseModel):
    def __init__(self):
        self.Cid = ""  ##渠道身份标识（做直连使用）
        self.ChannelID = ""  ##渠道ID
        self.ChannelName = ""  ##渠道name
        self.SourceID = ""  ##航司ID
        self.SourceInsideOrderNo = ""  ##订单内部单号
        self.SourceName = ""  ##航司名字
        self.SourceCode = ""    ##供应UseSystem
        self.Action = "Search"  ## Search  Book
        self.Account = ""  ##b2b登陆
        self.Password = ""
        self.Dep = ""   ##出发城市
        self.Arr = ""   ##到达城市
        self.DepAirport = ""    #出发机场
        self.ArrAirport = ""    #到达机场
        self.DepDate = "" #出发日期 例：2019-12-02
        self.RetDate = ""  #到达日期 例：2019-12-02
        self.TripType = 1  #行程类型 1单程 2往返
        self.AdultNum = 1  ##成人数量
        self.ChildNum = 0  ##儿童数量
        self.InfNum = 0     #婴儿数量
        self.FromFlightNos = ""  ##HX123+HX123
        self.RetFlightNos = ""  ##HX123+HX123
        self.AdtFare = 0    #Book时使用  报价票面
        self.AdtTax = 0     #。。。。 报价税费
        self.ChdFare = 0    #。。。. 儿童票面
        self.ChdTax = 0     #。。。。儿童税费
        self.TotalFare = 0  #AdtFare+AdtTax  票面+税费
        self.Currency = ""  #币种
        self.DefaultRate = 0    #汇率
        self.Passengers = []    #乘机人信息
        self.Baggages = []      #需要预定行李的星系
        self.waitTime = 10  ##直连超时时间
        self.isCache = True  ##是否使用缓存（直连需要  Timer不需要）
        self.RawData = None
        self.IsProxy = False    #是否需要代理
        self.ip = ""
        self.port = ""
        self.PayAccountInfo = AirPayCard()

##搜索返回参数
class AirLowFareRes(BaseModel):
    def __init__(self):
        self.ResultCode = 500  #200成功  404无航班数据  505 IP失效，任务重置   507请求超时，任务重置  (500或者未知code)未知错误
        self.Message = ""
        self.TimeInfo = ""
        self.SearchInfo = ""
        self.LogInfo = ""
        self.sup_CarrierIDs = []
        self.LowFare = LowFare()
        self.LowFareList = []

##返回参数fare
class LowFare(BaseModel):
    def __init__(self):
        self.ResultCode = 500
        self.Message = ""
        self.PNR = ""
        self.Adtk = ""
        self.Data = ""
        self.Token = ""
        self.SessionId = ""
        self.BookingNo = ""
        self.Remark = ""
        self.F_Mark = ""
        self.R_Mark = ""
        self.TripType = 1
        self.ValidatingCarrier = ""
        self.RouteLine = ""  ##HKG-BJS+BJS-SHA/SHA-BJS+BJS-HKG
        self.FlightNums = ""  ##HX123+HX123/HX123+HX123
        self.Cabins = ""  ##V+V/V+V
        self.AdultSellPrice = 0
        self.AdultSellTax = 0
        self.ChildSellPrice = 0
        self.ChildSellTax = 0
        self.TotalSellPrice = 0
        self.TotalOrderSellPrice = 0
        self.Sell_CurrencyCode = "CNY"
        self.ExchangeRate = 0
        self.AdultPrice = 0
        self.AdultTax = 0
        self.ChildPrice = 0
        self.ChildTax = 0
        self.TotalPrice = 0
        self.TotalOrderPrice = 0
        self.CurrencyCode = ""
        self.TotalSeatPrice = 0
        self.TotalMeatPrice = 0
        self.TotalBaggagePrice = 0
        self.TotalFeePrice = 0
        self.AdSerciceCurrency = ""
        self.MaxSeat = 0
        self.FarebasisList = []
        self.FromSegments = []
        self.RetSegments = []

#支付卡信息
class AirPayCard(BaseModel):
    def __init__(self):
        self.CardNum = ""
        self.CardType=""
        self.VerificationCode=""
        self.ExpireMonth=0
        self.ExpireYear=2020
        self.CardOwner=""
        self.CardExpireData=""

##行李
class Baggage(BaseModel):
    def __init__(self):
        self.PassengerName = ""
        self.FlightNo = ""
        self.DepAirport = ""
        self.ArrAirport = ""
        self.Piece = 0
        self.Weight=0