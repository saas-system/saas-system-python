from wtforms import Form, StringField, IntegerField
from wtforms.validators import DataRequired, length

from app.libs.enums import ClientTypeEnum


class ClientForm(Form):
    # 用户名，必填，字段长度：
    account = StringField(validators=[DataRequired(), length(
        min=5, max=32
    )])
    # 密码
    secret = StringField()
    # 客户端类型，必填
    type = IntegerField(validators=[DataRequired()])

    # 自定义验证器，验证是否枚举
    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e

        pass

    pass
