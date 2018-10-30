from flask import Flask, jsonify, request, Response, json
from settings import *
from BookModel import Book


# GET /books
@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})  # Create Response


# Validate book object for POST request
def valid_book_object_post(book_object):
    return 'name' in book_object and 'price' in book_object and 'isbn' in book_object


# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if valid_book_object_post(request_data):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
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
    item = Book.get_book(isbn)
    return jsonify(item)  # Create Response


def valid_book_object_put(book_object):
    return 'name' in book_object and 'price' in book_object


# PUT /books/isbn
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if valid_book_object_put(request_data):
        Book.replace_book(isbn, request_data['name'], request_data['price'])
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
    if 'name' in request_data:
        Book.update_book_name(isbn, request_data['name'])
    if 'price' in request_data:
        Book.update_book_price(isbn, request_data['price'])
    return Response(status=204)


# DELETE books/isbn
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if Book.delete_book(isbn):
        return Response(status=204)
    return Response(status=400)  # No book found


app.run(port=5000)