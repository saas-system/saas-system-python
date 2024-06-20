from flask import Flask
from app.config.log import setup_logger
from app.exception.error_handlers import register_error_handlers


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    # 上下文创建数据库
    with app.app_context():
        db.create_all()
    pass


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')

    # 注册
    register_blueprints(app)
    register_plugin(app)

    # 设置日志
    setup_logger(app)

    # 全局捕获异常
    register_error_handlers(app)

    return app
