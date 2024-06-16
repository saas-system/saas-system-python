from app.libs.redprint import Redprint

api = Redprint('book')

@api.route('/book')
def get_book():
    return 'get book'
