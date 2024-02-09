import json
import os

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)


def if_update(page, titles):
    if page == 0 and os.path.exists('../second_title.txt'):
        with open('../second_title.txt', 'r') as file:
            second_title = file.read()
        # print(second_title)
        # print(titles[1].get('title'))
        if titles[1].get('title') == second_title:
            # print('yes')
            return 1
    else:
        return 0


@app.route('/', methods=['GET'])
def home():
    url = 'https://www.htu.edu.cn/8955/list'
    data = []
    pages = 8
    id_num = 0
    ifUpdate = 0
    for page in range(pages):
        url_list = str(url) + str(page + 1) + ".htm"
        # print(url_list)
        response = requests.get(url_list)
        soup = BeautifulSoup(response.content, 'html.parser')
        titles = urls = soup.select('div#wp_news_w15 ul.wp_article_list li.list_item div.fields span.Article_Title a')
        times = soup.select('div#wp_news_w15 ul.wp_article_list li.list_item div.fields span.Article_PublishDate')
        # print(page)
        ifUpdate = if_update(page, titles)
        if ifUpdate == 1:
            # print('break')
            break
        else:
            for i in range(len(titles)):
                id_num = id_num + 1
                json_dict = {
                    'id': id_num,
                    'title': titles[i].get('title'),
                    'time': times[i].text,
                    'url': urls[i].get('href')
                }
                data.append(json_dict)
                print(json_dict)
        if page == 0:
            with open('../second_title.txt', 'w') as file:
                file.write(titles[1].get('title'))
        if id_num == 100:
            break
    if ifUpdate == 0:
        with open('../news.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps({'data': data}, ensure_ascii=False))
    else:
        with open('../news.json', 'r', encoding='utf-8') as file:
            data = json.loads(file.read())['data']

    app.json.ensure_ascii = False
    return jsonify({'code': 200, 'message': 'success', 'data': data})


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
