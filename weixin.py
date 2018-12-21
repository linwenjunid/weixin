# -*- coding: utf-8 -*-
from app import create_app, db
from flask_script import Manager, Shell

app = create_app()
manager = Manager(app)


def make_shell_context():
    from app.models.wx_user import WxUser
    return dict(app=app, db=db, user=WxUser)


manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
