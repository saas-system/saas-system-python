from wtforms import StringField, IntegerField, Form
from wtforms.validators import DataRequired, length, Email, Regexp
from wtforms import ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User


# from app.validators.base import BaseForm as Form


class ClientForm(Form):
    # 用户账号
    account = StringField(
        # 验证器
        validators=[
            DataRequired(message='不允许为空'),
            length(min=5, max=32)
        ]
    )
    # 用户密码
    secret = StringField()
    # 客户端类型
    type = IntegerField(
        validators=[
            DataRequired()
        ]
    )

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    """
    校验 email 注册的表单
    """
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    def validate_account(self, value):
        """
        校验账号是否已经被注册过
        :param value:
        :return:
        """
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired()])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])
