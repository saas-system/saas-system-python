from app.libs.redprint import Redprint

api = Redprint('user')


@api.route('/get')
def get_user():
    return 'get user'


@api.route('/create')
def create_user():
    return 'create user'
