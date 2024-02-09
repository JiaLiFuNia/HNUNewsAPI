import json
import os

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)


def if_update(page, titles):
    if page == 0:
        with open('second_title.txt', 'r') as file:
            second_title = file.read()
        file.close()
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
    json_list = {
        "code": 200,
        "message": "success",
        "data":
            [

            ]
    }

    pages = 3
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
        if page == 0:
            with open('second_title.txt', 'w') as file:
                file.write(titles[1].get('title'))
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
                json_list['data'].append(json_dict)
                # print(json_dict)
    if ifUpdate == 0:
        with open('news.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(json_list, ensure_ascii=False))
        file.close()
    else:
        with open('news.json', 'r', encoding='utf-8') as file:
            json_list = json.loads(file.read())
        file.close()

    app.json.ensure_ascii = False
    return jsonify(json_list)


if __name__ == '__main__':
    app.run(debug=True)
