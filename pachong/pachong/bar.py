#市级或县区级柱状图


import pyecharts.options as opts
from pyecharts.charts import Bar, Line
import pymongo
import pandas as pd
from pyecharts.charts import Map,Geo
from pyecharts import options as opts
import pyecharts.options as opts
from pyecharts.charts import Line
import pyecharts.options as opts
from pyecharts.charts import Line

# 将在 v1.1.0 中更改
from pyecharts.commons.utils import JsCode

from webserver import send2browser

"""
Gallery 使用 pyecharts 1.0.0
参考地址: https://www.echartsjs.com/examples/editor.html?c=multiple-y-axis

目前无法实现的功能:

1、暂无
"""
def draw_bar(city_name,date,new_price_list,second_hand_price,rate):
    colors = ["#5793f3", "#d14a61", "#675bba"]
    # date = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    legend_list = ["新房价", "二手房价", "增长率"]
    new_price_list.reverse()
    second_hand_price.reverse()
    date.reverse()
    bar = (
        Bar(init_opts=opts.InitOpts(width="1680px", height="800px"))
        .add_xaxis(xaxis_data=date)
        .add_yaxis(
            series_name="新房价",
            y_axis=new_price_list,
            yaxis_index=0,
            color=colors[1],
        )
        .add_yaxis(
            series_name="二手房价", y_axis=second_hand_price, yaxis_index=1, color=colors[0]
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="新房价",
                type_="value",
                min_=int(min(new_price_list) * 0.5),
                max_=int(max(new_price_list) * 1.5),
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=colors[1])
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} 元/平米"),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="增长率",
                min_=round(min(rate)*1.05,5),
                max_=round(max(rate)*1.05,5),
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=colors[2])
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} %"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="{}地区房价增长柱状图".format(city_name)),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name="二手房价",
                min_=int(min(second_hand_price)*0.5),
                max_=int(max(second_hand_price)*1.5),
                position="right",
                offset=80,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=colors[0])
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} 元/平米"),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        )
    )

    line = (
        Line()
        .add_xaxis(xaxis_data=date)
        .add_yaxis(
            series_name="增长率", y_axis=rate, yaxis_index=2, color=colors[2]
        )
    )

    bar.overlap(line).render("{}地区房价增长柱状图.html".format(city_name))
    send2browser("{}地区房价增长柱状图.html".format(city_name))


def draw_county(county_name):
    # county_name = "上海静安区"
    county_data = []
    county_data = pd.DataFrame(list(county_table.find({"name":"{}".format(county_name)})))

    new_houseprice_list= list()
    second_houseprice_list = list()
    date = list()
    rate = list()
    for i in range(0,12):
        new_houseprice_list.append(county_data["historical_data"][0][i]["new_price"])
        second_houseprice_list.append(county_data["historical_data"][0][i]["second_hand_price"])
        rate.append(round((county_data["historical_data"][0][11-i]["new_price"]-county_data["historical_data"][0][12-i]["new_price"])/county_data["historical_data"][0][11-i]["new_price"],5))
        date.append(county_data["historical_data"][0][i]["date"])
    draw_bar(county_name,date,new_houseprice_list,second_houseprice_list,rate)

def draw_city(city_name):
    # county_name = "上海静安区"
    city_data = []
    city_data = pd.DataFrame(list(city_table.find({"name":"{}".format(city_name)})))

    new_houseprice_list= list()
    second_houseprice_list = list()
    date = list()
    rate = list()
    for i in range(0,12):
        new_houseprice_list.append(city_data["historical_data"][0][i]["new_price"])
        second_houseprice_list.append(city_data["historical_data"][0][i]["second_hand_price"])
        rate.append(round((city_data["historical_data"][0][11-i]["new_price"]-city_data["historical_data"][0][12-i]["new_price"])/city_data["historical_data"][0][11-i]["new_price"],5))
        date.append(city_data["historical_data"][0][i]["date"])
    draw_bar(city_name,date,new_houseprice_list,second_houseprice_list,rate)





if __name__ == '__main__':
    client = pymongo.MongoClient('localhost', 27017)
    db = client['house_price']
    city_table = db['gotohui_city']
    county_table = db['gotohui_county']
    flag = input("查询市级房价增长柱状图输入1，查询县级房价增长柱状图请输入0   :")
    city_name = input("输入城市名称  :")
    print("请于localhost:8080端口查看")
    if(flag):
        draw_city(city_name)
    else:
        draw_county(city_name)
