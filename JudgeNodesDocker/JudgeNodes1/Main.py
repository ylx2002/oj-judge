from flask import Flask, request, jsonify, redirect, url_for, after_this_request, session
import os
import zipfile
import module.RunCode as run
import threading, subprocess
import json


app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = './data'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/judge', methods = ['GET','POST'])
def judge():
    code = session.get('code', {}) 
    rid = session.get('rid', {}) 
    pid = session.get('pid', {}) 
    lang = session.get('language', {})
    print(lang)
    if lang == 'c++':    
        with open('./submissions/'+str(rid)+'.cpp', 'w') as file:
            file.write(code)
        x=run.Compile(str(rid)) # 编译记录号为 R1 的程序
        if x.returncode == 1: # CE
            return jsonify({'result': [80], 'rid' : str(rid)}), 200

    if lang == 'python':
        with open('./submissions/'+str(rid)+'.py', 'w') as file:
            file.write(code) 
    
    result = run.Run(str(rid),str(pid),lang)
    print(result)
    # import time
    # time.sleep(5)
    return jsonify({'result': result, 'rid' : str(rid)}), 200


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        file = request.files['file']
        data = request.form.to_dict()

        print(data)

        session['code'] = data['code']
        session['pid'] = data['pid']
        session['rid'] = data['rid']
        session['language'] = data['language']

        @after_this_request
        def redirect_to_judge(response):
            # 使用302重定向（默认）进行跳转
            return redirect(url_for('judge'))
    
        # 保存文件到本地，解压缩
        file.save(f"./data/{file.filename}")
        zip_path=f"./data/{file.filename}"
        extract_to = f"./data/"+data['pid'] 
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            RmResult = subprocess.run(['rm','-r',zip_path], capture_output=True, text=True)
            # print(CompileResult)
            return "File and data received!", 200
        except zipfile.BadZipFile:
            return "Unzip failed", 400

    return 'Hello, World!', 200

def AppRun():
    app.run(host='0.0.0.0', port=8001) 


if __name__ == '__main__':

    thread = threading.Thread(target=AppRun)
    thread.start()

# x=run.Compile('R1') # 编译记录号为 R1 的程序
# run.Run('R1','P1') # 运行记录号为 R1，题号为 P1 的程序


