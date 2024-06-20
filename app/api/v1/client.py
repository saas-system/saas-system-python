from flask import request

from app.libs.error_code import Success, ClientTypeError
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm
from app.libs.enums import ClientTypeEnum

api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    data = request.json
    # 校验
    form = ClientForm(data=data)
    if form.validate():
        promise = {
            # 邮件
            ClientTypeEnum.USER_EMAIL: __register_user_by_email
            # 小程序...
        }
        try:
            promise[form.type.data]()
        except KeyError as e:
            raise ClientTypeError('Invalid client type')
    else:
        raise ClientTypeError()
    return 'success'


def __register_user_by_email():
    """
    通过邮件注册
    :param form: 从验证器中可以读取所有参数
    :return:
    """
    form = UserEmailForm(data=request.json)
    if form.validate():
        User.register_by_email(form.nickname.data,
                               form.account.data,
                               form.secret.data)
