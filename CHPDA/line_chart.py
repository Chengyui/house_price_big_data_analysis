# 生成市及县的房价走势图及未来一个月的房价


import pymongo
import pandas as pd
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Line

# 将在 v1.1.0 中更改
from pyecharts.commons.utils import JsCode


from data_process import data_process
from predict import GM11
from webserver import send2browser

# 预测模式下，对预测的房价进行自定义标记
def flagjudge(flag, date, houseprice_list):
    if flag:
        return opts.MarkPointOpts(data=[
            opts.MarkPointItem(name="自定义标记点", coord=[date[12], houseprice_list[12]],
                               value=houseprice_list[12], symbol_size=80)])
    else:
        return None

# 使用pyecharts 接受输入数据画图并将图表传送到指定端口
def draw_line(location, new_houseprice_list, second_houseprice_list, flag):
    js_formatter = """function (params) {
            console.log(params);
            return params.value + (params.seriesData.length ? '：' + '新房 '+params.seriesData[0].data[1] + ' 二手房 ' +params.seriesData[1].data[1] : '');
        }"""
    date = [
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
    if flag:
        date = date + ["2022-6"]
    title_choice = ["{}地区房价月走势".format(location), "{}地区房价月走势图（预测）".format(location)]
    (
        Line(init_opts=opts.InitOpts(width="1400px", height="700px"))
            .add_xaxis(
            xaxis_data=date
        )
            .extend_axis(
            xaxis_data=date,
            # xaxis=opts.AxisOpts(
            #     type_="category",
            #     axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
            #     # axisline_opts=opts.AxisLineOpts(
            #     #     is_on_zero=False, linestyle_opts=opts.LineStyleOpts(color="#d14a61")
            #     # ),
            #     # axispointer_opts=opts.AxisPointerOpts(
            #     #     is_show=True, label=opts.LabelOpts(formatter=JsCode(js_formatter),position="bottom")
            #     # ),
            # ),
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

            markpoint_opts=flagjudge(flag, date, new_houseprice_list),

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
            markpoint_opts=flagjudge(flag, date, second_houseprice_list),

        )
            .set_global_opts(
            legend_opts=opts.LegendOpts(),
            tooltip_opts=opts.TooltipOpts(trigger="none", axis_pointer_type="cross"),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                axisline_opts=opts.AxisLineOpts(
                    is_on_zero=False, linestyle_opts=opts.LineStyleOpts(color="#2e3079")
                ),
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True, label=opts.LabelOpts(formatter=JsCode(js_formatter),position="top")
                ),

            ),
            title_opts=opts.TitleOpts(title=title_choice[flag]),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
                min_=int(min(second_houseprice_list + new_houseprice_list) * 0.95),
                max_=int(max(second_houseprice_list + new_houseprice_list) * 1.05),
            ),
        )
            .render("result/{}地区房价月走势.html".format(location))
    )
    send2browser("result/{}地区房价月走势.html".format(location))

# 接受数据表，查找指定区县的房价数据，调用画图函数
def draw_county(county_table, county_name, opt):
    # county_name = "上海静安区"
    county_data = []
    county_data = pd.DataFrame(list(county_table.find({"name": "{}".format(county_name)})))
    print(county_data["historical_data"][0])
    if len(county_data["historical_data"][0])<12:
        send2browser("error.html")
        return
    new_houseprice_list = list()
    second_houseprice_list = list()
    # try:
    for i in range(0, 12):
        new_houseprice_list.append(county_data["historical_data"][0][i]["new_price"])
        second_houseprice_list.append(county_data["historical_data"][0][i]["second_hand_price"])
    # except Exception as e:
    #     send2browser("default.html")
    new_houseprice_list.reverse()
    second_houseprice_list.reverse()
    data_process(new_houseprice_list)
    data_process(second_houseprice_list)
    if opt:
        new_houseprice_list = new_houseprice_list + [predict(new_houseprice_list)]
        second_houseprice_list = second_houseprice_list + [predict(second_houseprice_list)]
    draw_line(county_name, new_houseprice_list, second_houseprice_list, opt)

# 接受数据表，查找指定地级市的房价数据，调用画图函数
def draw_city(city_table, city_name, opt):
    # city_name = "上海"
    city_data = []
    city_data = pd.DataFrame(list(city_table.find({"name": "{}".format(city_name)})))

    # 检测到数据缺失 报错
    print(city_data["historical_data"][0])
    if len(city_data["historical_data"][0]) < 12:
        send2browser("error.html")
        return
    new_houseprice_list = list()
    second_houseprice_list = list()
    for i in range(0, 12):
        new_houseprice_list.append(city_data["historical_data"][0][i]["new_price"])
        second_houseprice_list.append(city_data["historical_data"][0][i]["second_hand_price"])
    new_houseprice_list.reverse()
    second_houseprice_list.reverse()
    data_process(new_houseprice_list)
    data_process(second_houseprice_list)
    if opt:
        new_houseprice_list = new_houseprice_list + [predict(new_houseprice_list)]
        second_houseprice_list = second_houseprice_list + [predict(second_houseprice_list)]
    draw_line(city_name, new_houseprice_list, second_houseprice_list, opt)

# 调用GM11函数对未来一个月房价进行预测，返回预测值。
def predict(price_list):
    price_list = np.array(price_list)
    #
    # # 拟合
    # reg = LinearRegression()
    # reg.fit(x_axis, price_list)
    # a = reg.coef_[0][0]  # 系数
    # b = reg.intercept_[0]  # 截距
    x = price_list  # 输入数据
    result = GM11(x, 1)
    # print(result)
    return int(result['predict']['value'][0])
    # return int(np.array(price_list).mean())


def line_chart(opt):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['house_price']
    city_table = db['gotohui_city']
    county_table = db['gotohui_county']
    flag = input("查询市级房价趋势图输入1，县区级房价趋势图请输入0   :")
    flag = int(flag)
    city_name = input("输入城市名称   :")
    print("请于localhost:8080端口查看")
    if flag:
        draw_city(city_table, city_name, opt)
    else:
        draw_county(county_table, city_name, opt)

# 从前端接受到指定的城市或区县
def gen_line_chart(_city: str, _flag: str, opt=1):
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
        draw_city(city_table, city_name, opt)
    else:
        draw_county(county_table, city_name, opt)
