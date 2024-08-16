## 发送评测请求
opt 传编译选项，-O2 默认开。如果要不开 O2，需要传一个空 list。（暂时没写，无效果）
端口是 8100 放调度程序，810x 是评测机

```python
data = {
    "pid": "P1",
    "rid": "R3",
    "code": "#include <iostream>\nusing namespace std;\nint main() {\n    int a, b, c;\n    cin >> a >> b;\n    c = a + b * 2;\n    cout << c;\n    return 0;\n}\n// test"
    "opt": ['-std=c++11','-O2']
    } 
response = requests.post('http://localhost:8100', json=data)
```


## 评测结果返回

status 0 是正确返回
result 是一个list，表示若干个测试点的评测状态。
评测状态 0 AC 1 WA 2 RE 3 TLE 4 MLE 5 UKE

```python
data = {
    'status':0,
    'result':result
}
response = requests.post(Url_OJ_Back, data=data)
```

## 测试数据格式

测试数据为 zip 格式，命名为{题目编号}.zip

压缩包内文件格式：
```
{题目编号}
|
|-----config
|-----1.in
|-----1.ans
|-----......
```
config 格式
```
1000
512
2
```
第一行，时间限制，单位 ms；第二行，空间限制，单位 MB；第三行，测试点数量。

上传：
```python
    files = {
        'file': open('{题目编号}.zip', 'rb')
        } # 发评测数据
    result = requests.post('http://localhost:8100', files=files)
```

## 运行

在 `JudgeNodesDocker` 中开评测机

```sh
sudo docker-compose build
sudo docker-compose up
```

如果要改评测机数量，端口，直接改 `docker-compose.yml` 同时要改 `Scheduler` 中的 `nodes`，这个里面只要写端口。