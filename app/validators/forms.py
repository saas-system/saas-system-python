from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form

class ClientForm(Form):
    """
    基础客户端表单，包含用户账号、密码和客户端类型
    """
    # 用户账号
    account = StringField(
        validators=[
            DataRequired(message="不允许为空"),
            Email(message="无效的邮箱"),
        ]
    )
    # 用户密码
    secret = StringField()
    # 客户端类型
    type = IntegerField(
        validators=[
            DataRequired(message="客户端类型不允许为空")
        ]
    )

    def validate_type(self, value):
        """
        校验客户端类型是否合法
        """
        try:
            client = ClientTypeEnum(value.data)
        except ValueError:
            raise ValidationError('无效的客户端类型')
        self.type.data = client

class UserEmailForm(ClientForm):
    """
    校验 email 注册的表单
    """
    # 重新定义账号字段，以便对 email 格式进行单独验证
    account = StringField(
        validators=[
            DataRequired(message="不允许为空"),
            Email(message="无效的邮箱")
        ]
    )
    # 密码字段，包含必需和正则表达式验证
    secret = StringField(
        validators=[
            DataRequired(message="密码不允许为空"),
            Regexp(
                r'^[A-Za-z0-9_*&$#@]{6,22}$',
                message="密码只能包含字母、数字和特殊字符，并且长度在6到22之间"
            )
        ]
    )
    # 昵称字段，包含长度验证
    nickname = StringField(
        validators=[
            DataRequired(message="昵称不允许为空"),
            Length(min=2, max=22, message="昵称长度应在2到22个字符之间")
        ]
    )

    def validate_account(self, value):
        """
        校验账号是否已经被注册过
        """
        if User.query.filter_by(email=value.data).first():
            raise ValidationError('该邮箱已被注册')

class BookSearchForm(Form):
    """
    书籍搜索表单，包含搜索关键词
    """
    q = StringField(
        validators=[
            DataRequired(message="搜索关键字不允许为空")
        ]
    )

class TokenForm(Form):
    """
    Token表单，包含Token字段
    """
    token = StringField(
        validators=[
            DataRequired(message="Token不允许为空")
        ]
    )
