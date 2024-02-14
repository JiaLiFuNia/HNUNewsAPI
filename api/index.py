import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)


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


@app.route("/<string:kind>", methods=['get'])
def home(kind):
    code = 201
    message = '非法请求'
    data = []
    if kind == 'an':
        code, message, data = an()
    if kind == 'bn':
        code, message, data = bn()
    if kind == 'cn':
        code, message, data = cn()
    if kind == 'dn':
        code, message, data = dn()
    return jsonify({'code': code, 'message': message, 'data': data})


@app.route('/news', methods=['post'])
def getnews():
    newsKind = request.values.get("newsKind")
    code = 201
    message = '非法请求'
    data = []
    if newsKind == 'an':
        code, message, data = an()
    if newsKind == 'bn':
        code, message, data = bn()
    if newsKind == 'cn':
        code, message, data = cn()
    if newsKind == 'dn':
        code, message, data = dn()
    app.json.ensure_ascii = False
    return jsonify({'code': code, 'message': message, 'data': data})


if __name__ == '__main__':
    app.run(debug=True)
