#大陆房价热力图

# 导入相关模块
import pymongo
import pandas as pd
from pyecharts.charts import Map,Geo
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode

from webserver import send2browser


def draw_heapmap_by_month(data,month):
    js_formatter = """function (params) {
              console.log(params);
          }"""

    city_list = []
    new_price_list = []
    for city in data['name']:
        city_list.append(city)
    for new_price in data['historical_data']:
        new_price_list.append(new_price[5-month]['new_price'])
    data_city = [(city, new_price) for city, new_price in zip(city_list, new_price_list)]

    china_city = (
        Map(init_opts=opts.InitOpts(width="1400px", height="700px"))
            .add(
            "房价（元/㎡）",
            data_city,
            "china-cities",
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="2022年{}月大陆地区房价热力图.html".format(month)),
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
            .render("result/2022年{}月大陆地区房价热力图.html".format(month))
    )
    send2browser("result/2022年{}月大陆地区房价热力图.html".format(month))
def heap_map():
    # 连接数据库
    client = pymongo.MongoClient('localhost', 27017)
    db = client['house_price']
    city_table = db['gotohui_city']
    data = pd.DataFrame(list(city_table.find()))
    #historical_data--citynum--month--newprice
    # print(data['historical_data'][1][0]['new_price'])
    #name--citynum
    # print(data['name'][1])
    month = input("您要生成几月份的房价热力图？   :")
    print("请于localhost:8080端口查看")
    draw_heapmap_by_month(data,int(month))



