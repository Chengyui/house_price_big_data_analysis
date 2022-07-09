# 绘制最近12个月的大陆房价热力图

import pymongo
import pandas as pd
from pyecharts.charts import Map
from pyecharts import options as opts
from webserver import send2browser

# 调用pyecharts 接受月份和数据表，进行数据处理并绘制热力图并传送到指定端口
def draw_heapmap_by_month(data, year, month):
    js_formatter = """function (params) {
              console.log(params);
          }"""
    # prov_city = ['长沙', '株洲', '湘潭', '衡阳']
    # data_prov_city = [(i, random.randint(100, 200)) for i in prov_city]
    city_list = []
    new_price_list = []
    for city in data['name']:
        city_list.append(city)
    for new_price in data['historical_data']:
        new_price_list.append(new_price[(5 - month+12) % 12]['new_price'])
    data_city = [(city, new_price) for city, new_price in zip(city_list, new_price_list)]

    china_city = (
        Map(init_opts=opts.InitOpts(width="1400px", height="700px"))
            .add(
            "房价（元/㎡）",
            data_city,
            "china-cities",
            label_opts=opts.LabelOpts(is_show=False),
        )
            # .add("",
            #      data_prov_city,
            #      "晋中")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="{}年{}月大陆地区房价热力图(部分地区暂无数据)".format(year,month)),
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True,
                pieces=[
                    {"max": max(new_price_list), "min": 30000, "label": ">=30000", "color": "#B40404"},
                    {"max": 29999, "min": 10000, "label": "10000-29999", "color": "#DF0101"},
                    {"max": 9999, "min": 5000, "label": "5000-9999", "color": "#F78181"},
                    {"max": 4999, "min": 0, "label": "1000-4999", "color": "#F5A9A9"},
                ],
                is_show=True,

            )

        )
            .render("result/{}年{}月大陆地区房价热力图.html".format(year,month))
    )
    send2browser("result/{}年{}月大陆地区房价热力图.html".format(year,month))

def heap_map():
    # 连接数据库
    client = pymongo.MongoClient('localhost', 27017)
    db = client['house_price']
    city_table = db['gotohui_city']
    data = pd.DataFrame(list(city_table.find()))
    # historical_data--citynum--month--newprice
    # print(data['historical_data'][1][0]['new_price'])
    # name--citynum
    # print(data['name'][1])
    month = input("您要生成几月份的房价热力图？   :")
    print("请于localhost:8080端口查看")
    draw_heapmap_by_month(data, int(month))

# 从前端接受月份数据，调用绘画函数
def gen_heap_map(_month):
    # 连接数据库
    client = pymongo.MongoClient('localhost', 27017)
    db = client['house_price']
    city_table = db['gotohui_city']
    data = pd.DataFrame(list(city_table.find()))
    month = int(_month[5:7])
    year = int(_month[0:4])
    print(month,year)
    draw_heapmap_by_month(data, year, month)
