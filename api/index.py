import json
import os

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

LAST_TITLE_KEY = ['LAST_TITLE_AN_KEY', 'LAST_TITLE_BN_KEY', 'LAST_TITLE_CN_KEY', 'LAST_TITLE_DN_KEY',
                  'LAST_TITLE_EN_KEY']


def ifUpdate(limit, new_title):
    last_title = [os.environ.get(LAST_TITLE_KEY[0], '1'), os.environ.get(LAST_TITLE_KEY[1], '2'),
                  os.environ.get(LAST_TITLE_KEY[2], '3'), os.environ.get(LAST_TITLE_KEY[3], '4'),
                  os.environ.get(LAST_TITLE_KEY[4], '5')]
    print(last_title)
    print(new_title)
    if last_title[int(limit / 1000) - 1] == new_title:
        return True
    else:
        return False


def json_data(limit):
    res_data = requests.get('https://raw.githubusercontent.com/JiaLiFuNia/HNUNewsAPI/master/api/news.json').json()[
        'data']
    data = []
    if limit == 0:
        return res_data
    else:
        for i in res_data:
            if str(i['id'])[0] == str(limit)[0]:
                data.append(i)
        return data


def geturl(url, limit):
    data = []
    pages = 8
    id_num = limit
    if url == "":
        return data
    else:
        for page in range(pages):
            url_list = str(url) + str(page + 1) + ".htm"
            # print(url_list)
            response = requests.get(url_list)
            soup = BeautifulSoup(response.content, 'html.parser')
            titles = urls = soup.select(
                'div#wp_news_w15 ul.wp_article_list li.list_item div.fields span.Article_Title a')
            times = soup.select('div#wp_news_w15 ul.wp_article_list li.list_item div.fields span.Article_PublishDate')
            if page == 0:
                if ifUpdate(limit, titles[4].get('title')):
                    data = json_data(limit)
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
                if id_num - limit == 100:
                    break
        return data


def an():
    url = 'https://www.htu.edu.cn/8955/list'
    data = geturl(url, 1000)
    code = 200
    message = '通知公告'
    app.json.ensure_ascii = False
    return code, message, data


def bn():
    url = 'https://www.htu.edu.cn/8957/list'
    data = geturl(url, 2000)
    code = 200
    message = '院部动态'
    app.json.ensure_ascii = False
    return code, message, data


def cn():
    url = 'https://www.htu.edu.cn/xsygcs/list'
    data = geturl(url, 3000)
    code = 200
    message = '学术预告'
    app.json.ensure_ascii = False
    return code, message, data


def dn():
    url = 'https://www.htu.edu.cn/8954/list'
    data = geturl(url, 4000)
    code = 200
    message = '师大新闻'
    app.json.ensure_ascii = False
    return code, message, data


def en():
    url = 'https://www.htu.edu.cn/9008/list'
    data = geturl(url, 5000)
    code = 200
    message = '媒体师大'
    app.json.ensure_ascii = False
    return code, message, data


@app.route("/<string:types>", methods=['get'])
def home(types):
    code = 201
    message = '非法请求'
    data = []
    if types == 'an':
        code, message, data = an()
    if types == 'bn':
        code, message, data = bn()
    if types == 'cn':
        code, message, data = cn()
    if types == 'dn':
        code, message, data = dn()
    if types == 'en':
        code, message, data = dn()
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
        data = json_data(0)
    return jsonify({'code': code, 'message': message, 'data': data})


@app.route('/', methods=['post'])
def getnews():
    types = request.values.get("types")
    code = 201
    message = '非法请求'
    data = []
    if types == 'an':
        code, message, data = an()
    if types == 'bn':
        code, message, data = bn()
    if types == 'cn':
        code, message, data = cn()
    if types == 'dn':
        code, message, data = dn()
    if types == 'en':
        code, message, data = en()
    if types == 'all':
        code = 200
        message = 'success'
        data = json_data(0)
    app.json.ensure_ascii = False
    return jsonify({'code': code, 'message': message, 'data': data})


@app.route("/", methods=['get'])
def getAllNews():
    code = 200
    message = 'success'
    data = json_data(0)
    app.json.ensure_ascii = False
    return jsonify({'code': code, 'message': message, 'data': data})


def save_all_news():
    data = an()[2] + bn()[2] + cn()[2] + dn()[2] + en()[2]
    json_dict = {'code': 200, 'message': 'success', 'data': data}
    with open("news.json", 'w', encoding='utf-8') as file:
        file.write(json.dumps(json_dict, ensure_ascii=False))
    print('success')


if __name__ == '__main__':
    save_all_news()
    app.run(debug=True)
