# coding=utf-8
from flask import Flask, render_template, request, jsonify
import time
import threading
import chat
from concurrent.futures import ThreadPoolExecutor
import pyttsx3
import vision_main_part

def heartbeat():
    print(time.strftime('%Y-%m-%d %H:%M:%S - heartbeat', time.localtime(time.time())))
    timer = threading.Timer(60, heartbeat)
    timer.start()

timer = threading.Timer(60, heartbeat)
timer.start()

app = Flask(__name__, static_url_path="/static")
executor = ThreadPoolExecutor()
global res_msg

@app.route('/', methods=['GET', 'POST'])
# 定义应答函数，用于获取输入信息并返回相应的答案
def reply():
    if request.method == 'GET':
        return render_template('index.html')
    else:
    # 获取参数信息
        # 语句分词
        # 生成回答信息
        # unk值处理
        # 空处理
        global res_msg
        chat.thread_it(chat.run(),)
        res_msg = chat.get_answer()
        executor.submit(get_voice)
        #res_msg = '请与我聊聊天吧'
        # return res_msg
        return render_template('index.html', response=res_msg)

def get_voice():
    global res_msg
    engine = pyttsx3.init()
    engine.say(res_msg)
    engine.runAndWait()
    # 朗读一次
    engine.endLoop()
    engine.stop()

"""
jsonify:是用于处理序列化json数据的函数，就是将数据组装成json格式返回
http://flask.pocoo.org/docs/0.12/api/#module-flask.json
"""

if __name__ == '__main__':
    thead_one = threading.Thread(target=vision_main_part.cap_start,args=())
    thead_two = threading.Thread(target=app.run, args=())
    thead_one.start()
    thead_two.start()
    #app.run()