# 绘画市级或县区级增长率柱状图


import pyecharts.options as opts
from pyecharts.charts import Bar, Line
import pymongo
import pandas as pd
from pyecharts.charts import Map, Geo
from pyecharts import options as opts
import pyecharts.options as opts
from pyecharts.charts import Line
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.faker import Faker
# 将在 v1.1.0 中更改
from pyecharts.commons.utils import JsCode

from data_process import data_process
from webserver import send2browser

"""
Gallery 使用 pyecharts 1.0.0
参考地址: https://www.echartsjs.com/examples/editor.html?c=multiple-y-axis

目前无法实现的功能:

1、暂无
"""

# 使用pyecharts接受城市房价增长率数据，画柱状图，并将图表放置于指定端口
def draw_bar(city_name, date, new_price_list, second_hand_price):
    js_formatter = """function (params) {
                console.log(params);
                params.data = params.data+100
            }"""
    colors = ["#5793f3", "#d14a61", "#675bba"]
    # date = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    # legend_list = ["新房价", "二手房价", "增长率"]
    new_price_list = [round(i * 100, 2) for i in new_price_list]
    second_hand_price = [round(i * 100, 2) for i in second_hand_price]
    date.reverse()
    date = [i[2:] for i in date]

    bar = (
        Bar(init_opts=opts.InitOpts(width="1400px", height="700px"))
            .add_xaxis(date)
            .add_yaxis("新房价", new_price_list, gap="0%")
            .add_yaxis("二手房价", second_hand_price, gap="0%")
            .set_global_opts(title_opts=opts.TitleOpts(title="{}地区房价增长柱状图".format(city_name),
                                                       subtitle="增长率/%"),
                             brush_opts=opts.BrushOpts(),
                             yaxis_opts=opts.AxisOpts(
                                 interval=50,
                                 axistick_opts=opts.AxisTickOpts(is_show=True),
                                 splitline_opts=opts.SplitLineOpts(is_show=True),
                             ),
                             )
            .set_series_opts(label_opts=opts.LabelOpts(position="inside", font_size=10))
            # .set_series_opts(label_opts=opts.LabelOpts(position="bottom"))
            #
            .render("result/{}地区房价增长柱状图.html".format(city_name))
    )
    send2browser("result/{}地区房价增长柱状图.html".format(city_name))

# 接受区县数据表和区县名称，查找房价数据，计算增长率数据，调用绘画接口
def draw_county(county_table, county_name):
    # county_name = "上海静安区"
    county_data = []
    county_data = pd.DataFrame(list(county_table.find({"name": "{}".format(county_name)})))

    # 检测到数据缺失 报错
    if len(county_data["historical_data"][0]) < 12:
        send2browser("error.html")
        return

    new_houseprice_list = list()
    second_houseprice_list = list()
    date = list()
    rate1 = list()
    rate2 = list()
    new_houseprice_list = list()
    second_houseprice_list = list()
    for i in range(0, 13):
        new_houseprice_list.append(county_data["historical_data"][0][i]["new_price"])
        second_houseprice_list.append(county_data["historical_data"][0][i]["second_hand_price"])
    new_houseprice_list.reverse()
    second_houseprice_list.reverse()
    data_process(new_houseprice_list)
    data_process(second_houseprice_list)
    print(new_houseprice_list)
    print(second_houseprice_list)
    for i in range(0, 12):
        rate1.append(round((new_houseprice_list[i + 1] - new_houseprice_list[i]) / new_houseprice_list[i], 5))
        rate2.append(round((second_houseprice_list[i + 1] - second_houseprice_list[i]) / second_houseprice_list[i], 5))
        date.append(county_data["historical_data"][0][i]["date"])
    draw_bar(county_name, date, rate1, rate2)

# 接受区县数据表和城市名称，查找房价数据，计算增长率数据，调用绘画接口
def draw_city(city_table, county_name):
    # county_name = "上海静安区"
    city_data = []
    city_data = pd.DataFrame(list(city_table.find({"name": "{}".format(county_name)})))

    # 检测到数据缺失 报错
    print(city_data["historical_data"][0])
    if len(city_data["historical_data"][0]) < 12:
        send2browser("error.html")
        return
    new_houseprice_list = list()
    second_houseprice_list = list()
    date = list()
    rate1 = list()
    rate2 = list()
    new_houseprice_list = list()
    second_houseprice_list = list()
    for i in range(0, 13):
        new_houseprice_list.append(city_data["historical_data"][0][i]["new_price"])
        second_houseprice_list.append(city_data["historical_data"][0][i]["second_hand_price"])
    new_houseprice_list.reverse()
    second_houseprice_list.reverse()
    data_process(new_houseprice_list)
    data_process(second_houseprice_list)
    print(new_houseprice_list)
    print(second_houseprice_list)
    for i in range(0, 12):
        rate1.append(round((new_houseprice_list[i + 1] - new_houseprice_list[i]) / new_houseprice_list[i],5))
        rate2.append(round((second_houseprice_list[i + 1] - second_houseprice_list[i]) / second_houseprice_list[i],5))
        date.append(city_data["historical_data"][0][i]["date"])
    draw_bar(county_name, date, rate1, rate2)


def bar_chart():
    client = pymongo.MongoClient('localhost', 27017)
    db = client['house_price']
    city_table = db['gotohui_city']
    county_table = db['gotohui_county']
    flag = input("查询市级房价增长柱状图输入1，查询县级房价增长柱状图请输入0   :")
    city_name = input("输入城市名称  :")
    print("请于localhost:8080端口查看")
    if flag:
        draw_city(city_table, city_name)
    else:
        draw_county(county_table, city_name)

# 前端调用此接口，输入城市名称，调用数据处理接口
def gen_bar_chart(_city: str, _flag: str):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['house_price']
    city_table = db['gotohui_city']
    county_table = db['gotohui_county']

    if _flag == '市':
        flag = 1
    else:
        flag = 0

    city_name = _city

    if flag:
        draw_city(city_table, city_name)
    else:
        draw_county(county_table, city_name)
