import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)


def geturl(url, id_num):
    data = []
    pages = 8
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

            to_str = str(id_num)
            str_len = len(to_str)
            last_four = int(to_str[str_len - 3:str_len])

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
                if last_four == 100:
                    break
            if last_four == 100:
                break
        return data


@app.route('/', methods=['get'])
def home():
    url_1 = 'https://www.htu.edu.cn/8955/list'
    url_2 = 'https://www.htu.edu.cn/8957/list'
    url_3 = 'https://www.htu.edu.cn/xsygcs/list'
    url_4 = 'https://www.htu.edu.cn/8954/list'
    data_1 = geturl(url_1, 1000)
    data_2 = geturl(url_2, 2000)
    data_3 = geturl(url_3, 3000)
    data_4 = geturl(url_4, 4000)
    data = data_1 + data_2 + data_3 + data_4
    code = 200
    message = 'success'
    app.json.ensure_ascii = False
    return jsonify({'code': code, 'message': message, 'data': data})


@app.route('/news', methods=['post'])
def news():
    newsKind = request.values.get("newsKind")
    code = 201
    message = '非法请求'
    data = []
    if newsKind == 'an':
        url = 'https://www.htu.edu.cn/8955/list'
        code = 200
        message = '通知公告'
        data = geturl(url, 100)
    if newsKind == 'bn':
        url = 'https://www.htu.edu.cn/8957/list'
        code = 200
        message = '院部动态'
        data = geturl(url, 200)
    if newsKind == 'cn':
        url = 'https://www.htu.edu.cn/xsygcs/list'
        code = 200
        message = '学术预告'
        data = geturl(url, 300)
    if newsKind == 'dn':
        url = 'https://www.htu.edu.cn/8954/list'
        code = 200
        message = '师大新闻'
        data = geturl(url, 400)

    app.json.ensure_ascii = False
    return jsonify({'code': code, 'message': message, 'data': data})


if __name__ == '__main__':
    app.run(debug=True)
