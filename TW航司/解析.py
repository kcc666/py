from lxml import etree

with open("data.html","rb")as f:
    text = f.read().decode("utf8")

def parse_data(text1):

    

    data_all = [] #列表下的字典

    #将html文本解析为element对象
    html = etree.HTML(text1) #el对象

    #航班列表的 li
    airline_list = html.xpath("//div[@id='price_list_route_1']/ul/li")

    #遍历li
    for li_1 in airline_list:

        data_all_dict = {

            "dep_city":"" #出发城市码
            ,"arr_city":"" #到达城市码
            ,"dep_date":"" #出发日期

            ,"air_tax1":"" #机建
            ,"air_tax2":"" #燃油(贵一些)
            ,"dep_time":"" #航班出发时间
            ,"arr_time":"" #航班到达时间
            ,"air_num":"" #航班号
            ,"hd_price":"售罄" #活动票价
            ,"zn_price":"" #智能票价
            ,"yb_price":"" #一般运费
        }

        #出发和到达时间
        air_dep_arr_times = li_1.xpath("./a/div/div[1]//strong/text()")

        #航班号
        air_numbers = li_1.xpath("./a/div/div[1]/button/text()")

        #赋值,出发时间到达时间航班号
        data_all_dict["air_num"] = air_numbers[0]
        data_all_dict["dep_time"] = air_dep_arr_times[0]
        data_all_dict["arr_time"] = air_dep_arr_times[1]

        #遍历每条航班下的活动,智能,一般票价的分别价格
        for item in li_1.xpath("./div/div"):
    
            #标题(活动,智能,或一般))
            label = item.xpath("./div[@class='select_rate']/label/text()[2]")[0]
            try:
                #价格
                price = item.xpath("./div[@class='rate_price']/strong/text()")[0]
                #币种
                currency = item.xpath("./div[@class='rate_price']/span[@class='unit']/text()")[0]
                #机建
                data_all_dict["air_tax1"] = item.xpath("./div[@class='select_rate']/div[last()]/@data-tax")[0]
                #燃油
                data_all_dict["air_tax2"] = item.xpath("./div[@class='select_rate']/div[last()]/@data-surcharge")[0]
            except:
                price = "售罄"
                currency = "无"
                data_all_dict["air_tax1"] = "无"
                data_all_dict["air_tax2"] = "无"
            
            

            if label =="活动票价":
                data_all_dict["hd_price"] = price
            elif label =="智能票价":
                data_all_dict["zn_price"] = price
            else:
                data_all_dict["yb_price"] = price
        
        #把本条航班信息添加到数组&打印
        # print(data_all_dict)
        data_all.append(data_all_dict)
    
    #打印最后结果
    print(data_all)

parse_data(text)
