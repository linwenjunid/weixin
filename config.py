import os


class Config:
    BOOTSTRAP_SERVE_LOCAL = True

    UPLOAD_FOLDER = r'D:\Python\weixin\app\static'

    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('ADMIN_SQLURL')

    DEBUG = True

    TOKEN = os.getenv('WECHAT_TOKEN', 'linwenjun')
    AES_KEY = os.getenv(
        'WECHAT_AES_KEY',
        '7R57M87PevVSq67XMSjqFX5L9r5kITs6dVDHvO5dDT7')
    APPID = os.getenv('WECHAT_APPID', 'wx51ecf70a6c46b1bb')
    APPSECRET = os.getenv(
        'WECHAT_APPSECRET',
        'c75cdc902c98c3a4055a25a1b0bcaf98')
