from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(token, password):
    # token
    # HTTP 账号密码
    # header key:value
    # account: hongwei
    # password: 123456
    # key=Authorization
    # value=basic base64(hongwei:123456)
    pass
