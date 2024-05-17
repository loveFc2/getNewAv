import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, Response

app = Flask(__name__)

# 设置代理
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

def get_latest_num():
    base_url = "https://ffjav.com/torrent/tag/fc2-ppv/page/1"

    with requests.Session() as session:
        session.proxies.update(proxies)

        try:
            response = session.get(base_url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', class_='card')

        # 处理卡片
        num = process_card(cards[0])
        return num

def process_card(card):
    title_text = card.find('h5').find('a').text
    num = re.findall(r'\d{7}', title_text)
    return num[0] if num else "Not found"

@app.route('/getNew')
def get_new():
    num = get_latest_num()
    if num:
        return Response(num, mimetype='text/plain')
    else:
        return Response("Failed to fetch the latest number", status=500, mimetype='text/plain')

if __name__ == '__main__':
    app.run()
