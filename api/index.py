import json
import os

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    url = 'https://www.htu.edu.cn/8955/list'
    data = []
    pages = 8
    id_num = 0
    for page in range(pages):
        url_list = str(url) + str(page + 1) + ".htm"
        # print(url_list)
        response = requests.get(url_list)
        soup = BeautifulSoup(response.content, 'html.parser')
        titles = urls = soup.select('div#wp_news_w15 ul.wp_article_list li.list_item div.fields span.Article_Title a')
        times = soup.select('div#wp_news_w15 ul.wp_article_list li.list_item div.fields span.Article_PublishDate')
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
            if id_num == 100:
                break
        if id_num == 100:
            break
    app.json.ensure_ascii = False
    return jsonify({'code': 200, 'message': 'success', 'data': data})


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
