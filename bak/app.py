# -*- coding:utf-8 -*-

from flask import Flask, make_response, request
from flask_script import Manager
import time
import xml.etree.ElementTree as ET

import hashlib

app = Flask(__name__)
app.debug = True
manager = Manager(app)


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return 'hello'


@app.route('/wx_flask', methods=['GET', 'POST'])
def wechat():

    if request.method == 'GET':
        # 这里改写你在微信公众平台里输入的token
        token = 'linwenjun'
        # 获取输入参数
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        # 字典排序
        list = sorted([token, timestamp, nonce])

        s = list[0] + list[1] + list[2]
        # sha1加密算法
        hascode = hashlib.sha1(s.encode('utf-8')).hexdigest()
        # 如果是来自微信的请求，则回复echostr
        if hascode == signature:
            return echostr
        else:
            return "测试"
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text
        print("#############")
        xml_rep = """<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        <FuncFlag>0</FuncFlag>
        </xml>"""
        response = make_response(xml_rep % (fromu, tou, str(int(time.time())), content))
        response.content_type = 'application/xml'
        return response
    return 'Hello weixin!'


if __name__ == '__main__':
    manager.run()
