import os
import sys
import random
from flask import Flask, request, render_template, flash, redirect
import redis
import requests
import json
from dotenv import load_dotenv, find_dotenv
import traceback

app = Flask(__name__)
app.secret_key = 'some_secret'

redis_client = None
HOST = "http://0.0.0.0:5000"
PATH_LENGTH = 5

BASE62 = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
    'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
    'X', 'Y', 'Z'
]


def generate():
    """
    generate random path
    :return: string
    """
    sort_url, seed = "", random.randint(0, sys.maxsize)
    for i in range(PATH_LENGTH):
        sort_url += BASE62[seed % len(BASE62)]
        seed = random.randint(0, sys.maxsize) % len(BASE62)

    return sort_url


def msg(code: int, status: str, message: str):
    """
    compose data in json format
    :param code: status code
    :param status: status description
    :param message: information
    :return: string
    """
    res = {'code': code, 'status': status, 'msg': message}
    return json.dumps(res)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        url = request.form.get('basic-url')

        if not url:
            flash('請輸入要幫忙壓縮的網址!')
            return redirect(request.url)

        response = requests.post(f'{HOST}short_url', data={'url': url}).json()
        if response.get('code') != 200:
            flash(response.get('msg'))
            return redirect(request.url)

        return render_template('success.html', short_url=response.get('msg'))


@app.route('/short_url', methods=['GET', 'POST'])
def short_url():
    url = None
    if request.method == 'GET':
        url = request.args.get('url')
    elif request.method == 'POST':
        url = request.form.get('url')
        content = request.json
        if not url and content:
            url = content.get('url')

    if not url:
        return msg(400, 'error', 'Need input url parameter.')

    sort_url = generate()
    redis_client.set(sort_url, url)
    return msg(200, 'success', f'{HOST}{sort_url}')


@app.route('/<string:url>', methods=['GET', 'POST'])
def origin_url(url):
    res = redis_client.get(url)
    if res:
        return msg(200, 'success', res.decode("utf-8"))
    else:
        return msg(400, 'error', 'No such url!')


if __name__ == '__main__':
    load_dotenv(find_dotenv(), override=True)
    try:
        HOST = f'http://{os.getenv("APP_HOST")}:{os.getenv("APP_PORT")}/'
        PATH_LENGTH = int(os.getenv('PATH_LENGTH'))

        pool = redis.ConnectionPool(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')),
                                    db=int(os.getenv('REDIS_DB')), socket_connect_timeout=3)
        redis_client = redis.Redis(connection_pool=pool)
        redis_client.ping()

        app.run(host=os.getenv('APP_HOST'), port=os.getenv('APP_PORT'))
    except redis.TimeoutError or redis.ConnectionError:
        print("請先確認 redis狀態")
    except Exception as e:
        print(e)
        traceback.print_exc()
