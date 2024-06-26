from werkzeug.exceptions import HTTPException
from app.app import create_app
from app.exception.error import APIException
from app.exception.error_code import ServerError

__author__ = '七月'

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        return ServerError()


if __name__ == '__main__':
    app.run()
