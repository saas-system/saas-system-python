from app.exception.error_code import NotFound
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User

api = Redprint('user')


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def get_user(uid):
    """
    获取用户信息
    :param uid:
    :return:
    :说明：方式一：account secret对象
    :说明：方式二：token 1个月 2个月， 是否过期，是否合法
    """
    user = User.Query.get_or_404()
    return 'get user'


@api.route('/create')
def create_user():
    return 'create user'
