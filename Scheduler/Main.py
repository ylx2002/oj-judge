from flask import Flask, request, jsonify, redirect, url_for, after_this_request
import requests
import time
import threading
import zipfile
from io import BytesIO
import json

FilePath = r'./data/' # 数据包地址
NodesStatus = []  # 0:空闲
Ports = []

"""
data = {
    "pid": "P1",
    "rid": "R1",
    "code": "..."
}
"""

"""
# 创建线程列表
threads = []

# 创建N个线程
for i in range(N):
    thread = threading.Thread(target=print_numbers, args=(i,))
    threads.append(thread)
    thread.start()  # 启动线程
"""

JudgeThreads = []
Url_OJ_Back = 'http://127.0.0.1:8001/record/update' # 后端Url

def return_result(data):
   print(data)
   response = requests.post(Url_OJ_Back, data=data)
   return response.text

def run_judge_tasks(Url, pid, data, id):
    time.sleep(0.005)
    print(data['rid'], id, data['language'])
    files = {'file': open(FilePath+str(pid)+'.zip', 'rb')} # 发评测数据
    # print(files)
    result = requests.post(Url, files=files, data=data) # 评测
    print(result.json())
    NodesStatus[id] = 0
    x=result.json()['result']
    Result= {'status':0,'rid':data['rid']}
    flag = 0
    for i in x:
        if (i != 0):
            flag = i
    Result['result'] = flag
    # print(Result)
    return_result(Result)
    return 0

def distribution_tasks(pid, data): # 分发评测给空闲评测机
    Num = len(NodesStatus)
    if not('language' in data): # 设一个default
        data['language'] = 'c++'
    if data['language'] == 'C++' or data['language'] == 'cpp':
        data['language'] = 'c++'
    print(data['language'])
    while True:
        time.sleep(0.001)
        for i in range(0, Num):
            # print('now', i)
            if NodesStatus[i] == 0:
                NodesStatus[i] = 1
                Thread = threading.Thread(target=run_judge_tasks, args=('http://localhost:' + str(Ports[i]), pid, data, i))
                JudgeThreads.append(Thread)
                Thread.start()
                return 0

app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            # 发来的是一个评测请求
            data = request.json
            # print(data)
            Thread = threading.Thread(target = distribution_tasks, args = (str(data['pid']), data))
            Thread.start()
            """
            data = {
                "pid": "P1",
                "rid": "R1",
                "language": "C++" 
                "code": "..."
                "opt": "..."
            }
            """
            return jsonify({'status': 0}), 200

        file = request.files['file']
        print('get', file.filename)
        # 保存文件到本地，解压缩
        file.save(f"./data/{file.filename}")
        # 发来的是一个数据包 
        return jsonify({'status': 0}), 200
    
    return 'Hello, World!', 200



def main():
    with open('nodes','r') as file:
        Ports.extend(file.read().split())
    for i in Ports:
        NodesStatus.append(0)
    
    app.run(host='0.0.0.0', port=8100) 


if __name__ == "__main__":
    main()
