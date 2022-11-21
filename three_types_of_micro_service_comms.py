import urllib.request
from flask import Flask
from flask import jsonify
import json

import requests as req
import time

# Required for Threaded execution
import concurrent.futures

# Required for Asynchronous Communication
import httpx
import asyncio



app = Flask(__name__)



micro_service_ip = '34.70.185.114'


@app.route('/')
def hello_world():
    return {'message': 'Hello World!!!!'}





# Asynchronous Launch of GET request


async def get_async(url):
    async with httpx.AsyncClient() as client:
        return await client.get(url)


async def launch():
    urls = ['http://'+micro_service_ip+':80/hello/get_msg/1',
            'http://'+micro_service_ip+':80/hello/get_msg/2',
            'http://'+micro_service_ip+':80/hello/get_msg/3',
            'http://'+micro_service_ip+':80/hello/get_msg/4',
            'http://'+micro_service_ip+':80/hello/get_msg/5',
            'http://'+micro_service_ip+':80/hello/get_msg/6',
            'http://'+micro_service_ip+':80/hello/get_msg/7']

    resps = await asyncio.gather(*map(get_async, urls))
    data = [resp.status_code for resp in resps]
    x = " "
    for status_code in data:
        x = x + str(status_code) + " "
    return x


@app.route('/async')
def asynchronous_rest_api():
    tm1 = time.perf_counter()

    p = asyncio.run(launch())

    tm2 = time.perf_counter()

    x = p + "  Elapsed Time " + str(tm2 - tm1)

    return jsonify({"Description": "Response Code  ", "Value": x})


# Threaded Launch of GET request
def get_status(url=" "):
    resp = req.get(url=url)
    return resp.status_code


@app.route('/threaded')
def concurrent_rest_api():
    urls = ['http://'+micro_service_ip+':80/hello/get_msg/1',
            'http://'+micro_service_ip+':80/hello/get_msg/2',
            'http://'+micro_service_ip+':80/hello/get_msg/3',
            'http://'+micro_service_ip+':80/hello/get_msg/4',
            'http://'+micro_service_ip+':80/hello/get_msg/5',
            'http://'+micro_service_ip+':80/hello/get_msg/6',
            'http://'+micro_service_ip+':80/hello/get_msg/7']

    tm1 = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:

        futures = []
        x = " "
        for url in urls:
            futures.append(executor.submit(get_status, url=url))

        for future in concurrent.futures.as_completed(futures):
            x = x + str(future.result()) + " "

    tm2 = time.perf_counter()
    x = x + "  Elapsed Time " + str(tm2 - tm1)

    return jsonify({"Description": "Response Code  ", "Value": x})


# Sequential Launch of GET request

@app.route('/sequential')
def sequential_rest_api():
    urls = ['http://'+micro_service_ip+':80/hello/get_msg/1',
            'http://'+micro_service_ip+':80/hello/get_msg/2',
            'http://'+micro_service_ip+':80/hello/get_msg/3',
            'http://'+micro_service_ip+':80/hello/get_msg/4',
            'http://'+micro_service_ip+':80/hello/get_msg/5',
            'http://'+micro_service_ip+':80/hello/get_msg/6',
            'http://'+micro_service_ip+':80/hello/get_msg/7']

    tm1 = time.perf_counter()
    x = ""
    for url in urls:
        resp = req.get(url)
        x = x + "Response from:    " + url + "   " + str(resp.status_code) + "/n"

    tm2 = time.perf_counter()
    x = x + "/n" + "Time Elapsed:  " + str(tm2 - tm1)
    return jsonify({"Description": "Response Code  ", "Value": x})

@app.route('/service')
def micro_service_k8():
    urls = ['http://'+micro_service_ip+':80/hello/get_msg/1']

    tm1 = time.perf_counter()
    x = ""
    for url in urls:
        resp = req.get(url)
        x = x + "Response from:    " + url + "   " + str(resp.status_code) + "/n"

    tm2 = time.perf_counter()
    x = x + "/n" + "Time Elapsed:  " + str(tm2 - tm1)
    return jsonify({"Description": "Response Code  ", "Value": x})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True)
