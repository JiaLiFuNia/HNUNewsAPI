import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return jsonify(json_list)


if __name__ == '__main__':
    url = 'https://www.htu.edu.cn/8955/list'
    json_list = {
        "code": 200,
        "message": "success",
        "data":
            [

            ]
    }

    pages = 10
    id_num = 0
    i = 0

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
            json_list['data'].append(json_dict)
            # print(json_dict)
    # print(json_list)

    app.run(debug=True)
