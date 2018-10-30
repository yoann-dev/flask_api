from flask import Flask, jsonify, request, Response, json
from settings import *

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 978039400165
    },
    {
        'name': 'The Cat In The Hat',
        'price': 6.99,
        'isbn': 9782371000193   
    }
]


# GET /books
@app.route('/books')
def get_books():
    return jsonify({'books': books})  # Create Response


# Validate book object for POST request
def valid_book_object_post(book_object):
    return 'name' in book_object and 'price' in book_object and 'isbn' in book_object


# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if valid_book_object_post(request_data):
        books.insert(0, request_data)
        response = Response(status=201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalid_error_msg = {
            'error': "Invalid book passed in request"
        }
        response = Response(response=json.dumps(invalid_error_msg), status=400,
                            mimetype='application/json')
        return response


# GET /books/isbn
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    item = {}
    find_books = filter(lambda x: x['isbn'] == isbn, books)
    list_bool = list(find_books)
    if list_bool :
        item = list_bool[0]
    return jsonify(item)  # Create Response


def valid_book_object_put(book_object):
    return 'name' in book_object and 'price' in book_object


# PUT /books/isbn
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if valid_book_object_put(request_data):
        new_book = {
            'name': request_data['name'],
            'price': request_data['price'],
            'isbn': isbn
        }
        for i, book in enumerate(books):
            if book['isbn'] == isbn:
                books[i] = new_book
        return Response(status=204)
    else:
        invalid_error_msg = {
            'error': "Invalid book passed in request"
        }
        return Response(response=json.dumps(invalid_error_msg), status=400,
                        mimetype='application/json')


# PATCH books/isbn
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if 'name' in request_data:
        updated_book['name'] = request_data['name']
    if 'price' in request_data:
        updated_book['price'] = request_data['price']
    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_book)
    return Response(status=204)


# DELETE books/isbn
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    for book in books:
        if book['isbn'] == isbn:
            books.remove(book)
            return Response(status=204)
    return Response(status=400)  # No book found


app.run(port=5000)