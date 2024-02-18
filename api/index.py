import json
import os

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

LAST_TITLE_KEY = ['LAST_TITLE_AN_KEY', 'LAST_TITLE_BN_KEY', 'LAST_TITLE_CN_KEY', 'LAST_TITLE_DN_KEY',
                  'LAST_TITLE_EN_KEY', 'LAST_TITLE_EN_KEY', 'LAST_TITLE_EN_KEY', 'LAST_TITLE_EN_KEY']
ALL_TYPES = ['an', 'bn', 'cn', 'dn', 'aj', 'bj', 'cj', 'dj']
LIMIT = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
URLS = ['https://www.htu.edu.cn/8955/list', 'https://www.htu.edu.cn/8957/list', 'https://www.htu.edu.cn/xsygcs/list',
        'https://www.htu.edu.cn/8954/list', 'https://www.htu.edu.cn/teaching/3257/list',
        'https://www.htu.edu.cn/teaching/3251/list', 'https://www.htu.edu.cn/teaching/3258/list',
        'https://www.htu.edu.cn/teaching/kwgl/list']
MESSAGES = ['通知公告', '院部动态', '学术预告', '师大新闻', '教学新闻', '教务通知', '公示公告', '考务管理']
RULES = [
    {
        "urls": 'div#wp_news_w15 ul.wp_article_list li.list_item div.fields span.Article_Title a',
        "times": 'div#wp_news_w15 ul.wp_article_list li.list_item div.fields span.Article_PublishDate'
    },
    {
        "urls": 'ul.news_list li.news span.news_title a',
        "times": 'ul.news_list li.news span.news_meta'
    }
]


# 检测是否相同
def ifUpdate(limit, new_title):
    last_title = [os.environ.get(LAST_TITLE_KEY[0], '1'), os.environ.get(LAST_TITLE_KEY[1], '2'),
                  os.environ.get(LAST_TITLE_KEY[2], '3'), os.environ.get(LAST_TITLE_KEY[3], '4'),
                  os.environ.get(LAST_TITLE_KEY[4], '5'), os.environ.get(LAST_TITLE_KEY[5], '6'),
                  os.environ.get(LAST_TITLE_KEY[6], '7'), os.environ.get(LAST_TITLE_KEY[7], '8')]
    print(last_title)
    print(new_title)
    if last_title[int(limit / 1000) - 1] == new_title:
        return True
    else:
        return False


# 如果相同直接返回GitHub上的news.json
def json_data(limit, count):
    res_data = requests.get('https://raw.githubusercontent.com/JiaLiFuNia/HNUNewsAPI/master/api/news.json').json()[
        'data']
    data = []
    counts = 0
    if limit == 0:
        return res_data
    else:
        for i in res_data:
            if str(i['id'])[0] == str(limit)[0]:
                counts = counts + 1
                data.append(i)
            if count != 0 and counts == count:
                break
        return data


# 获取页面的所有新闻
def geturl(url, limit, count, rule):
    data = []
    pages = 8
    id_num = limit
    ifBreak = 0
    if url == "":
        return data
    else:
        for page in range(pages):
            url_list = str(url) + str(page + 1) + ".htm"
            # print(url_list)
            response = requests.get(url_list)
            soup = BeautifulSoup(response.content, 'html.parser')
            titles = urls = soup.select(RULES[rule]['urls'])
            times = soup.select(RULES[rule]['times'])
            if len(titles) == 0:
                break
            if page == 0:
                if ifUpdate(limit, titles[4].get('title')):
                    data = json_data(limit, count)
                    break
                else:
                    os.environ[LAST_TITLE_KEY[int(limit / 1000) - 1]] = titles[4].get('title')
            else:
                pass
            for i in range(len(titles)):
                id_num = id_num + 1
                url_temp = urls[i].get('href')
                if url_temp[0] != 'h':
                    url_temp = 'https://www.htu.edu.cn' + url_temp
                json_dict = {
                    'id': id_num,
                    'title': titles[i].get('title'),
                    'time': times[i].text,
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
            data = json_data(0, 0)
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
def getnews():
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
    data = json_data(0, 0)
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
