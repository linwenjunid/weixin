from app import db
from datetime import datetime


class WxUser(db.Model):
    __tablename__ = 'wx_user'
    subscribe = db.Column(db.Integer)
    openid = db.Column(db.Text, primary_key=True)
    nickname = db.Column(db.Text())
    sex = db.Column(db.Integer)
    city = db.Column(db.String(64))
    country = db.Column(db.String(64))
    province = db.Column(db.String(64))
    language = db.Column(db.String(64))
    headimgurl = db.Column(db.Text())
    subscribe_time = db.Column(
        db.DateTime(),
        index=True,
        default=datetime.utcnow)
    subscribe_scene = db.Column(db.String(64))
    remark = db.Column(db.Text())
