# app/error_handlers.py
from flask import jsonify, request

from app.exception.error import APIException


def register_error_handlers(app):
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        app.logger.error(f"Unhandled Exception: {str(error)}")
        response = error.get_body()
        response.status_code = error.code
        return response

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        app.logger.error(f"Unhandled Exception: {str(error)}")
        response = jsonify({
            'msg': str(error),
            'error_code': 1002,
            'request': request.method + ' ' + request.path
        })
        response.status_code = 400
        return response

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        app.logger.error(f"Unhandled Exception: {str(error)}")
        response = jsonify({
            'msg': 'An unexpected exception occurred.',
            'error_code': 1000,
            'request': request.method + ' ' + request.path
        })
        response.status_code = 500
        return response
