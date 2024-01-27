from data import books

def update_list(new_item):
    books.older_books.append(new_item)
    return books.modern_books + books.older_books
