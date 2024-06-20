from flask import Flask, jsonify, request

from app.libs.error import APIException


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

    # 全局捕获异常
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        response = error.get_body()
        response.status_code = error.code
        return response

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        response = jsonify({
            'msg': str(error),
            'error_code': 1002,
            'request': request.method + ' ' + request.path
        })
        response.status_code = 400
        return response

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        response = jsonify({
            'msg': 'An unexpected error occurred.',
            'error_code': 1000,
            'request': request.method + ' ' + request.path
        })
        response.status_code = 500
        return response

    return app
