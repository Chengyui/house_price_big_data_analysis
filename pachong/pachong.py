import time

import requests
from lxml import etree
from mongoengine import Document, StringField, URLField, IntField, DateField, ListField, connect, disconnect
import re

url = ["https://fangjia.gotohui.com/fjdata-360",
       "https://www.gotohui.com/fangjia/7",
       "https://www.gotohui.com/fangjia/9",
       "https://www.gotohui.com/fangjia/25",
       "https://www.gotohui.com/fangjia/2",
       "https://www.gotohui.com/fangjia/14",
       "https://www.gotohui.com/fangjia/29",
       "https://www.gotohui.com/fangjia/8",
       "https://www.gotohui.com/fangjia/17",
       "https://www.gotohui.com/fangjia/18",
       "https://www.gotohui.com/fangjia/10",
       "https://www.gotohui.com/fangjia/15",
       "https://www.gotohui.com/fangjia/27",
       "https://www.gotohui.com/fangjia/20",
       "https://www.gotohui.com/fangjia/21",
       "https://www.gotohui.com/fangjia/28",
       "https://www.gotohui.com/fangjia/11",
       "https://www.gotohui.com/fangjia/13",
       "https://www.gotohui.com/fangjia/26",
       "https://www.gotohui.com/fangjia/22",
       "https://www.gotohui.com/fangjia/31",
       "https://www.gotohui.com/fangjia/16",
       "https://www.gotohui.com/fangjia/19",
       "https://www.gotohui.com/fangjia/30",
       "https://www.gotohui.com/fangjia/12",
       "https://www.gotohui.com/fangjia/23",
       "https://www.gotohui.com/fangjia/24",
       "https://www.gotohui.com/fangjia/32"]

_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


def remove_blank(text):
    return re.sub(r"\s+", "", text)


def get_father(text):
    text = re.sub(r"\s+", "", text)
    text = re.sub("\"", "", text)
    text = re.sub("返回", "", text)
    return text


def str_find_digit(text):
    text = re.search(r".*(\d+).*", text)
    if text is None:
        return 0
    return text.group(1)


# def str_to_date(text):
#     return time.strptime(text, "%Y-%m")


def str_to_int(text):
    if text == "":
        return 0
    return int(remove_blank(text))


def retrieve(url, params):
    response = requests.get(url, headers=_header, params=params)
    text = response.content.decode("utf8")
    return text


def parse_province(text):
    html = etree.HTML(text)
    it = dict()
    it['url'] = "".join(html.xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[1]/a/@href'))
    it['name'] = "".join(html.xpath('/html/body/div[4]/div/div[1]/div[1]/div[1]/div[2]/a/text()'))
    li_list = html.xpath('/html/body/div[4]/div/div[1]/div[2]/table/tr/td[2]/a')
    item = list()
    for li in li_list:
        li_url = "".join(li.xpath('./@href'))
        li_name = "".join(li.xpath('./text()'))
        item.append(li_name)
        cities_content = retrieve(li_url, {})
        parse_city(cities_content)
    it['cities'] = item
    print(it['name'])
    Province(**it).save()


def parse_city(text):
    html = etree.HTML(text)
    it = dict()
    it['url'] = "".join(html.xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[1]/a/@href'))
    it['name'] = "".join(html.xpath('/html/body/div[4]/div/div[1]/div[1]/div[1]/div[2]/a/text()'))
    it['unit_price_rank'] = str_find_digit(
        "".join(html.xpath('/html/body/div[4]/div/div[1]/div[1]/div[2]/a[1]/text()')))
    it['rent_rank'] = str_find_digit("".join(html.xpath('/html/body/div[4]/div/div[1]/div[1]/div[2]/a[2]/text()')))
    it['set_price_rank'] = str_find_digit("".join(html.xpath('/html/body/div[4]/div/div[1]/div[1]/div[2]/a[3]/text()')))
    it['province'] = get_father("".join(html.xpath('/html/body/div[4]/div/div[1]/div[1]/div[2]/a['
                                                   '@class="more-hot-collection"]/text()')))
    item = list()
    item_list = html.xpath('//*[@id="zoushi"]/div[1]/table/tbody/tr')
    for li in item_list:
        data = dict()
        tmp = "".join(li.xpath('./td[2]/text()'))
        if tmp == "":
            continue
        data['date'] = tmp
        data['second_hand_price'] = str_to_int("".join(li.xpath('./td[3]/text()')))
        data['new_price'] = str_to_int("".join(li.xpath('./td[4]/text()')))
        item.append(data)
    it['historical_data'] = item
    counties = list()
    counties_list = html.xpath('/html/body/div[4]/div/div[2]/div[1]/table/tbody/tr/td[1]/a')
    for li in counties_list:
        li_url = "".join(li.xpath('./@href'))
        li_name = "".join(li.xpath('./text()'))
        counties.append(li_name)
        counties_concent = retrieve(li_url, {})
        parse_county(counties_concent)
    it['counties'] = counties
    City(**it).save()
    print(it['name'])


def parse_county(text):
    html = etree.HTML(text)
    it = dict()
    it['url'] = "".join(html.xpath('/html/body/div[4]/div/div[1]/div[2]/ul/li[1]/a/@href'))
    it['name'] = "".join(html.xpath('/html/body/div[4]/div/div[1]/div[1]/div[1]/div[2]/a/text()'))
    it['city'] = get_father("".join(html.xpath('/html/body/div[4]/div/div[1]/div[1]/div[2]/a['
                                               '@class="more-hot-collection"]/text()')))
    item = list()
    item_list = html.xpath('//*[@id="zoushi"]/div[1]/table/tbody/tr')
    for li in item_list:
        data = dict()
        tmp = "".join(li.xpath('./td[2]/text()'))
        if tmp == "":
            continue
        data['date'] = tmp
        data['second_hand_price'] = str_to_int("".join(li.xpath('./td[3]/text()')))
        data['new_price'] = str_to_int("".join(li.xpath('./td[4]/text()')))
        item.append(data)
    it['historical_data'] = item
    County(**it).save()
    print(it['name'])


class Province(Document):
    url = URLField()
    name = StringField()
    cities = ListField()

    meta = {
        "collection": "gotohui_province"
    }


class City(Document):
    url = URLField()
    name = StringField()
    province = StringField()
    counties = ListField()
    unit_price_rank = IntField()
    rent_rank = IntField()
    set_price_rank = IntField()
    historical_data = ListField()

    meta = {
        "collection": "gotohui_city"
    }


class County(Document):
    url = URLField()
    name = StringField()
    city = StringField()
    historical_data = ListField()

    meta = {
        "collection": "gotohui_county"
    }


def main():
    for page in range(28):
        params = {}
        content = retrieve(url[page], params)
        parse_province(content)


if __name__ == '__main__':
    connect(host="mongodb://localhost/house_price")
    main()
    disconnect()
