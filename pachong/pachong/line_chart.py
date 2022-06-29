# 市及县的房价走势图



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


def draw_line(location,new_houseprice_list,second_houseprice_list):
    new_houseprice_list.reverse()
    second_houseprice_list.reverse()
    js_formatter = """function (params) {
            console.log(params);
            return '房价  ' + params.value + (params.seriesData.length ? '：' + params.seriesData[0].data : '');
        }"""

    (
        Line(init_opts=opts.InitOpts(width="1600px", height="800px"))
            .add_xaxis(
            xaxis_data=[
                "2021-6",
                "2021-7",
                "2021-8",
                "2021-9",
                "2021-10",
                "2021-11",
                "2021-12",
                "2022-1",
                "2022-2",
                "2022-3",
                "2022-4",
                "2022-5"
            ]
        )
            .extend_axis(
            xaxis_data=[
                "2021-6",
                "2021-7",
                "2021-8",
                "2021-9",
                "2021-10",
                "2021-11",
                "2021-12",
                "2022-1",
                "2022-2",
                "2022-3",
                "2022-4",
                "2022-5"
            ],
            xaxis=opts.AxisOpts(
                type_="category",
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                axisline_opts=opts.AxisLineOpts(
                    is_on_zero=False, linestyle_opts=opts.LineStyleOpts(color="#6e9ef1")
                ),
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True, label=opts.LabelOpts(formatter=JsCode(js_formatter))
                ),
            ),
        )
            .add_yaxis(
            series_name="新房",
            is_smooth=True,
            symbol="emptyCircle",
            is_symbol_show=False,
            # xaxis_index=1,
            color="#d14a61",
            y_axis=new_houseprice_list,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
            .add_yaxis(
            series_name="二手房",
            is_smooth=True,
            symbol="emptyCircle",
            is_symbol_show=False,
            color="#6e9ef1",
            y_axis=second_houseprice_list,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
            .set_global_opts(
            legend_opts=opts.LegendOpts(),
            tooltip_opts=opts.TooltipOpts(trigger="none", axis_pointer_type="cross"),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                axisline_opts=opts.AxisLineOpts(
                    is_on_zero=False, linestyle_opts=opts.LineStyleOpts(color="#d14a61")
                ),
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True, label=opts.LabelOpts(formatter=JsCode(js_formatter))
                ),
            ),
            title_opts=opts.TitleOpts(title="{}地区房价月走势".format(location)),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            ),
        )
            .render("{}地区房价月走势.html".format(location))
    )
    send2browser("{}地区房价月走势.html".format(location))
def draw_county(county_name):
    # county_name = "上海静安区"
    county_data = []
    county_data = pd.DataFrame(list(county_table.find({"name":"{}".format(county_name)})))

    new_houseprice_list= list()
    second_houseprice_list = list()
    for i in range(0,12):
        new_houseprice_list.append(county_data["historical_data"][0][i]["new_price"])
        second_houseprice_list.append(county_data["historical_data"][0][i]["second_hand_price"])

    draw_line(county_name, new_houseprice_list, second_houseprice_list)

def draw_city(city_name):
    # city_name = "上海"
    city_data = []
    city_data = pd.DataFrame(list(city_table.find({"name": "{}".format(city_name)})))

    new_houseprice_list= list()
    second_houseprice_list = list()
    for i in range(0,12):
        new_houseprice_list.append(city_data["historical_data"][0][i]["new_price"])
        second_houseprice_list.append(city_data["historical_data"][0][i]["second_hand_price"])

    draw_line(city_name, new_houseprice_list, second_houseprice_list)





if __name__ == '__main__':
    client = pymongo.MongoClient('localhost', 27017)
    db = client['house_price']
    city_table = db['gotohui_city']
    county_table = db['gotohui_county']
    flag = input("查询市级房价趋势图输入1，县区级房价趋势图请输入0   :")
    city_name = input("输入城市名称   :")
    print("请于localhost:8080端口查看")
    if(flag):
        draw_city(city_name)
    else:
        draw_county(city_name)


