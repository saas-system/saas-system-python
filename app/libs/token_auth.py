from collections import namedtuple
from flask import current_app, g
from flask_httpauth import HTTPBasicAuth
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from app.exception.error_code import AuthFailed
import logging

# from app.libs.scope import is_in_scope

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'ac_type', 'scope'])

# 配置日志
logging.basicConfig(level=logging.DEBUG)

@auth.verify_password
def verify_password(token, password):
    """
    验证身份
    :param token:
    :param password:
    :说明：token， HTTP 账号密码， header key:value，
    :说明：account:hongwei； password: 123456
    :说明：key=Authorization
    :说明：value =basic base64(qiyue:123456)
    :return:
    """
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        # request， flask中的g变量
        g.user = user_info
        return True


def verify_auth_token(token):
    """
    验证token
    :param token:
    :return:
    """
    logging.debug(f"Secret Key: {current_app.config['SECRET_KEY']}")
    logging.debug(f"Token: {token}")

    key = current_app.config['SECRET_KEY']
    try:
        data = jwt.decode(token, key, algorithms=['HS256'])
        logging.debug(f"Decoded Data: {data}")
    except ExpiredSignatureError:
        # 是否过期
        logging.error("Token is expired")
        raise AuthFailed(msg='token is expired', error_code=1003)
    except InvalidTokenError:
        # 是否合法
        logging.error("Token is invalid")
        raise AuthFailed(msg='token is invalid', error_code=1002)

    # 读取数据
    uid = data.get('uid')
    ac_type = data.get('type')
    scope = data.get('scope', '')
    if uid is None or ac_type is None:
        logging.error("Token data is incomplete")
        raise AuthFailed(msg='token is invalid', error_code=1002)

    return User(uid, ac_type, scope)
