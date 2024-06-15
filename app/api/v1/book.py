from flask import Blueprint

book = Blueprint('book', __name__)


@book.route('/v1/user/book')
def get_book():
    return 'get book'
