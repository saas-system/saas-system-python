from app.libs.redprint import Redprint
from app.libs.token_auth import auth

api = Redprint('user')


@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    return 'get user'


@api.route('/create')
def create_user():
    return 'create user'
