import json
import os

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

LAST_TITLE_KEY = ['LAST_TITLE_AN_KEY', 'LAST_TITLE_BN_KEY', 'LAST_TITLE_CN_KEY', 'LAST_TITLE_DN_KEY',
                  'LAST_TITLE_EN_KEY', 'LAST_TITLE_FN_KEY', 'LAST_TITLE_GN_KEY', 'LAST_TITLE_HN_KEY']
ALL_TYPES = ['an', 'bn', 'cn', 'dn', 'aj', 'bj', 'cj', 'dj', 'pic']
LIMIT = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
URLS = ['https://www.htu.edu.cn/8955/list', 'https://www.htu.edu.cn/8957/list', 'https://www.htu.edu.cn/xsygcs/list',
        'https://www.htu.edu.cn/8954/list.htm', 'https://www.htu.edu.cn/teaching/3257/list',
        'https://www.htu.edu.cn/teaching/3251/list', 'https://www.htu.edu.cn/teaching/3258/list',
        'https://www.htu.edu.cn/teaching/kwgl/list', 'https://www.htu.edu.cn']
MESSAGES = ['通知公告', '新闻速递', '学术预告', '师大新闻', '教学新闻', '教务通知', '公示公告', '考务管理', '主页图片']
RULES = [
    {
        "urls": 'ul.news_list li.news a',
        "times": 'ul.news_list li.news a div.news_meta',
        "titles": "ul.news_list li.news a div.wz div.news_title"
    },
    {
        "urls": 'ul.news_list li.news span.news_title a',
        "times": 'ul.news_list li.news span.news_meta',
        "titles": 'ul.news_list li.news span.news_title a'
    },
    {
        "urls": 'div#banner div.inner ul.news_list li.news div.imgs a img'
    },
    {
        "urls": 'ul.news_list li.news div.news_title a',
        "times": 'ul.news_list li.news div.news_time',
        "titles": "ul.news_list li.news div.news_title a"
    }
]


# 获取页面的所有新闻
def geturl(url, limit, count, rule):
    data = []
    pages = 8
    id_num = limit
    ifBreak = 0
    if url == "":
        return data
    else:
        if rule != 2:
            print(pages)
            for page in range(pages):
                url_list = str(url) + str(page + 1) + ".htm"
                # print(url_list)
                response = requests.get(url_list)
                soup = BeautifulSoup(response.content, 'html.parser')
                if "8957" or "8954" in url.split("/"):
                    titles = soup.select(RULES[-1]['titles'])
                    urls = soup.select(RULES[-1]['urls'])
                    times = soup.select(RULES[-1]['times'])
                else:
                    titles = soup.select(RULES[rule]['titles'])
                    urls = soup.select(RULES[rule]['urls'])
                    times = soup.select(RULES[rule]['times'])
                if len(titles) == 0:
                    break
                for i in range(len(titles)):
                    id_num = id_num + 1
                    url_temp = urls[i].get('href')
                    if url_temp[0] != 'h':
                        url_temp = 'https://www.htu.edu.cn' + url_temp
                    if times[i].get("date") is None:
                        time = times[i].text
                    else:
                        time = times[i].get("date")
                    json_dict = {
                        'id': id_num,
                        'title': titles[i].text,
                        'time': time,
                        'url': url_temp
                    }
                    data.append(json_dict)
                    print(json_dict)
                    if count > 100 or count <= 0:
                        count = 100
                    if id_num - limit == count:
                        ifBreak = 1
                        break
                if ifBreak == 1:
                    break
            print(data)
            return data
        else:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            urls = soup.select(RULES[rule]['urls'])
            data = [url+img_url.get('src') for img_url in urls]
            print(data)
            return data


# 类型 数量 规则
def xn(types: str, count: int):
    code = 201
    message = '非法请求'
    data = []
    rule = 0
    if types in ALL_TYPES:
        index = ALL_TYPES.index(types)
        if types[-1] == 'j':
            rule = 1
        if types[-1] == 'c':
            rule = 2
        else:
            pass
        data = geturl(URLS[index], LIMIT[index], count, rule)
        code = 200
        message = MESSAGES[index]
    else:
        if types == 'tabs':
            code = 200
            message = 'success'
            data = [
                {
                    "title": "通知公告",
                    "id": "1"
                },
                {
                    "title": "师大新闻",
                    "id": "2"
                },
                {
                    "title": "院部动态",
                    "id": "3"
                }
            ]
        if types == 'all':
            code = 200
            message = 'success'
            data = []
    if len(data) == 0:
        code = 201
        message = '非法请求'
    return code, message, data


# @GET
@app.route("/<string:types>", methods=['get'])
def home(types):
    code, message, data = xn(types, 0)
    app.json.ensure_ascii = False
    return jsonify({'code': code, 'message': message, 'data': data})


# @POST
@app.route('/', methods=['post'])
def getNews():
    types = request.values.get("types")
    count = int(request.values.get("count"))
    code, message, data = xn(types, count)
    app.json.ensure_ascii = False
    return jsonify({'code': code, 'message': message, 'data': data})


# @GET
@app.route("/", methods=['get'])
def getAllNews():
    code = 200
    message = 'success'
    data = []
    app.json.ensure_ascii = False
    return jsonify({'code': code, 'message': message, 'data': data})


# @POST
@app.route('/jw', methods=['post'])
def get_jw_news():
    types = request.values.get("types")
    count = int(request.values.get("count"))
    code, message, data = xn(types, count)
    app.json.ensure_ascii = False
    return jsonify({'code': code, 'message': message, 'data': data})


# 保存文件
def save_all_news():
    data = []
    for i in range(len(ALL_TYPES)):
        data = data + xn(ALL_TYPES[i], 0)[2]
    json_dict = {'code': 200, 'message': 'success', 'data': data}
    with open("news.json", 'w', encoding='utf-8') as file:
        file.write(json.dumps(json_dict, ensure_ascii=False))
    print('success')


# save_all_news()


if __name__ == '__main__':
    app.run(debug=True)
