from lxml import etree

with open("data copy.html","rb")as f:
    text1 = f.read().decode("utf8")
    # print(len(text1))


dep_city = "" #出发城市码
arr_city = "" #到达城市码
dep_date = "" #出发日期

air_tax1 = "" #机建
air_tax2 = "" #燃油(贵一些)

dep_time = "" #航班出发时间
arr_time = "" #航班到达时间
air_num = "" #航班号
hd_price = "售罄" #活动票价
zn_price = "" #智能票价
yb_price = "" #一般运费



#将html文本解析为element对象
html = etree.HTML(text1) #el对象

#航班列表的 li
airline_list = html.xpath("//div[@id='price_list_route_1']/ul/li")


#第一个li标签的对象
li_1 = airline_list[0]


#在第一个li标签下的a标签继续找数据,出发时间和到达时间
air_dep_arr_times = li_1.xpath("./a/div/div[1]//strong/text()")
#航班号
air_numbers = li_1.xpath("./a/div/div[1]/button/text()")
# print(len(air_numbers))
# if len(air_numbers)!=0:
#     print(air_numbers[0])
air_num = air_numbers[0]
dep_time = air_dep_arr_times[0]
arr_time = air_dep_arr_times[1]
# print(air_num,dep_time,arr_time)

#详细信息框
# hd_zn_yb = li_1.xpath("./div/div") #详细信息框

#遍历活动票价,智能票价和一般运费下的不同价格
for item in li_1.xpath("./div/div"):
    
    #标题(活动,智能,或一般))
    label = item.xpath("./div[@class='select_rate']/label/text()[2]")[0]
    #对应的价格
    price = item.xpath("./div[@class='rate_price']/strong/text()")[0]
    #对应的币种
    currency = item.xpath("./div[@class='rate_price']/span[@class='unit']/text()")[0]
    #对应的机建
    air_tax1 = item.xpath("./div[@class='select_rate']/div[last()]/@data-tax")[0]
    #对应的燃油
    air_tax2 = item.xpath("./div[@class='select_rate']/div[last()]/@data-surcharge")[0]
    

    if label =="活动票价":
        hd_price = price
    elif label =="智能票价":
        zn_price = price
    else:
        yb_price = price

print(
    air_num,
    dep_time,
    arr_time,
    hd_price,
    zn_price,
    yb_price,
    air_tax1,
    air_tax2
    )

