from config import Config
from flask import request, abort, make_response, Blueprint, send_file
from wechatpy import parse_message, create_reply, WeChatClient
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)

from app import db
from app.models.wx_user import WxUser

from bs4 import BeautifulSoup
import requests
from os import path
import numpy as np
from wordcloud import WordCloud, STOPWORDS
from io import BytesIO
from PIL import Image
import jieba

main = Blueprint('auth', __name__)
client = WeChatClient(Config.APPID, Config.APPSECRET)


@main.route('/')
def index():
    r = requests.get("http://zj.qq.com/")
    r = BeautifulSoup(r.text.encode('utf-8'))
    txt = ''
    for t in r.find_all('a'):
        txt += t.get_text().strip()
    text = " ".join(jieba.cut(txt))

    with Image.open(path.join(Config.UPLOAD_FOLDER, '原图.jpg')) as i:
        image_mask = np.array(i)

    stopwords = set(STOPWORDS)
    stopwords.add("新闻")
    stopwords.add("百度")
    stopwords.add("公告")
    stopwords.add("关键词")
    # 配置词云
    wc = WordCloud(
        background_color="white",
        max_words=20000,
        stopwords=stopwords,
        font_path="simsun.ttc",
        mask=image_mask)
    # 生成词云
    wc.generate(text)
    # 存储到文件
    # wc.to_file(path.join(d, '结果.png'))
    img = wc.to_image()

    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)

    return send_file(byte_io, mimetype='image/png', cache_timeout=0)


@main.route('/wx_flask', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    encrypt_type = request.args.get('encrypt_type', 'raw')
    msg_signature = request.args.get('msg_signature', '')

    try:
        check_signature(Config.TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == 'GET':
        echo_str = request.args.get('echostr', '')
        return echo_str

    # POST request
    if encrypt_type == 'raw':
        # plaintext mode
        msg = parse_message(request.data)
        if msg.type == 'text':
            # reply = create_reply(msg.content, msg)
            articles = [
                {
                    'title': u'腾讯网',
                    'description': u'综合门户网站',
                    'url': u'http://www.qq.com',
                    # 'image': u'http://tupian.qqjay.com/u/2017/1228/3_133221_9.jpg'
                },
                {
                    'title': u'百度',
                    'description': u'搜索网站',
                    'url': u'http://www.baidu.com'
                },
                {
                    'title': u'知乎',
                    'description': u'网络问答社区',
                    'url': u'https://www.zhihu.com/'
                }
            ]
            reply = create_reply(articles, msg)

        elif msg.event == 'subscribe':
            cont = "FromUserName: %s\nEvent: %s\nTime: %s"
            user = WxUser.query.filter_by(openid=msg.source).first()
            if not user:
                user = WxUser(subscribe=1, openid=msg.source)
            else:
                user.subscribe = 1
            db.session.add(user)
            db.session.commit()
            wuser = client.user.get(msg.source)
            print(wuser)
            reply = create_reply(cont %
                                 (msg.source, msg.event, msg.create_time), msg)
        elif msg.event == 'unsubscribe':
            cont = "FromUserName: %s\nEvent: %s\nTime: %s"
            user = WxUser.query.filter_by(openid=msg.source).first()
            user.subscribe = 0
            db.session.add(user)
            db.session.commit()
            print(cont % (msg.source, msg.event, msg.create_time))
            reply = create_reply(cont %
                                 (msg.source, msg.event, msg.create_time), msg)
        else:
            reply = create_reply('Sorry, can not handle this for now', msg)
        return reply.render()
    else:
        # encryption mode
        from wechatpy.crypto import WeChatCrypto

        crypto = WeChatCrypto(Config.TOKEN, Config.AES_KEY, Config.APPID)
        try:
            msg = crypto.decrypt_message(
                request.data,
                msg_signature,
                timestamp,
                nonce
            )
        except (InvalidSignatureException, InvalidAppIdException):
            abort(403)
        else:
            msg = parse_message(msg)
            if msg.type == 'text':
                reply = create_reply(msg.content, msg)
            else:
                reply = create_reply('Sorry, can not handle this for now', msg)
            return crypto.encrypt_message(reply.render(), nonce, timestamp)


@main.route('/create_menu')
def create_menu():
    # 第一个参数是公众号里面的appID，第二个参数是appsecret
    status = client.menu.create({
        "button": [
            {
                "type": "view",
                "name": "百度",
                "url": "http://www.baidu.com/"
            },
            {
                "type": "view",
                "name": "腾讯",
                "url": "http://www.qq.com/"
            }
        ]
    })
    print("access_token: " + client.access_token)
    print(status)
    return make_response('createmenu: ok')


