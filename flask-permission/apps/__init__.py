from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


# 获取 Flask 的 app对象
def get_app():
    app = Flask(__name__)
    # 允许跨域
    CORS(app, resources=r'/*')
    # 应用自动刷新
    app.debug = True
    # 应用ip/端口 配置
    app.config['SERVER_NAME'] = 'localhost:5000'
    # 数据库连接配置
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost/db_permission?charset=utf8"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'j'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
    db.init_app(app)
    # 注册蓝图
    # 用户蓝图
    from apps.user import user_dp
    app.register_blueprint(user_dp)
    # 角色蓝图
    from apps.role import role_dp
    app.register_blueprint(role_dp)
    # 权限蓝图
    from apps.permission import permission_dp
    app.register_blueprint(permission_dp)
    # 菜单蓝图
    from apps.menu import menu_dp
    app.register_blueprint(menu_dp)
    return app
