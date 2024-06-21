import jwt
from flask import current_app, jsonify
from app.libs.enums import ClientTypeEnum
from app.exception.error_code import AuthFailed
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, TokenForm
from authlib.jose import JsonWebToken, JoseError
from typing import Dict, Any
from datetime import datetime, timedelta

api = Redprint('token')


@api.route('', methods=['POST'])
def get_token():
    """
    获取TOKEN
    :return:
    """
    form = ClientForm().validate_for_api()
    # 验证身份
    identity = verify_identity(ClientTypeEnum(form.type.data), form.account.data, form.secret.data)
    # 生成令牌
    token = generate_auth_token(identity['uid'], form.type.data, identity['scope'],
                                current_app.config['TOKEN_EXPIRATION'])
    response_data = {
        'token': token
    }
    return jsonify(response_data), 201


@api.route('/secret', methods=['POST'])
def get_token_info():
    """
    获取令牌信息
    """
    form = TokenForm().validate_for_api()
    token_info = verify_token(form.token.data)

    response_data = {
        'scope': token_info['scope'],
        'create_at': token_info['iat'],
        'expire_in': token_info['exp'],
        'uid': token_info['uid']
    }
    return jsonify(response_data)


def generate_auth_token(uid: int, ac_type: ClientTypeEnum, scope: str = None, expiration: int = 7200) -> str:
    """
    生成令牌
    """
    payload = {
        'uid': uid,
        'type': ac_type.value,
        'scope': scope,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=expiration)
    }
    key = current_app.config['SECRET_KEY']
    token = jwt.encode(payload, key, algorithm='HS256')
    return token


def verify_identity(client_type: ClientTypeEnum, account: str, secret: str) -> Dict[str, Any]:
    """
    验证身份
    """
    verifier = {
        ClientTypeEnum.USER_EMAIL: User.verify,
    }
    return verifier[client_type](account, secret)


def verify_token(token: str) -> Dict[str, Any]:
    """验证令牌"""
    jwt = JsonWebToken(['HS256'])
    key = current_app.config['SECRET_KEY']
    try:
        claims = jwt.decode(token, key)
        claims.validate()
    except JoseError as e:
        if 'expired' in str(e):
            raise AuthFailed(msg='token is expired', error_code=1003)
        raise AuthFailed(msg='token is invalid', error_code=1002)

    return {
        'scope': claims['scope'],
        'iat': claims['iat'],
        'exp': claims['exp'],
        'uid': claims['uid']
    }
