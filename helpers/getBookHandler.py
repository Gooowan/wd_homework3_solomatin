from helpers.getParams import get_params_from_url
from helpers.getById import get_item_by_id
from data.books import modern_books, older_books

def get_book(path):
    params = get_params_from_url(path) # {bookId : ['1']}
    intBookId = int(params['bookId'][0])
    book = get_item_by_id(intBookId, modern_books + older_books)
    return book


# params = get_book('/books?bookId=1')
# print(params)