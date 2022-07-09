# 对空缺的数据进行填充，若发现数据全空，跳转到报错界面
from webserver import send2browser


def data_process(price_list):
    for i in range(len(price_list)):
        if price_list[i] == 0:
            flag = 0
            for u in price_list[i + 1:]:
                if u != 0:
                    flag = 1
                    if i != 0:
                        price_list[i] = (price_list[i - 1] + u) / 2
                    else:
                        price_list[i] = u
                    break
            if flag == 0:
                if i == 0:
                    print("**********全空**********")
                    send2browser("error.html ")
                    return price_list
                else:
                    price_list[i] = price_list[i - 1]
    return price_list

