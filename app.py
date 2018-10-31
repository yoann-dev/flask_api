from flask import Flask, jsonify, request, Response, json
from settings import *
from BookModel import Book
from UserModel import User
import jwt
import datetime
from functools import wraps


# Decorateur pour imposer l'authentification sur les routes
def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return Response(response=json.dumps({'error': 'Need valid token'}), status=401,
                            mimetype='application/json')
    return wrapper


# Methode de login
@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    if User.username_password_match(username, password):
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return Response(response=token, status=200,
                        mimetype='application/text')
    else:
        return Response(status=401)


# Information sur tous les livres
# GET /books
# GET /books?token=shdfuhdsuhfdusfnjn (jwt token)
@app.route('/books')
@token_required
def get_books():
    return jsonify({'books': Book.get_all_books()})  # Create Response


# Validate book object for POST request
def valid_book_object_post(book_object):
    return 'name' in book_object and 'price' in book_object and 'isbn' in book_object


# Ajout d'un livre
# POST /books
@app.route('/books', methods=['POST'])
@token_required
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


# Information sur un livre par isbn
# GET /books/isbn
@app.route('/books/<int:isbn>')
@token_required
def get_book_by_isbn(isbn):
    item = Book.get_book(isbn)
    return jsonify(item)  # Create Response


def valid_book_object_put(book_object):
    return 'name' in book_object and 'price' in book_object


# Modification d'un livre par isbn
# PUT /books/isbn
@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
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


# Modification d'une propriète d'un livre par isbn
# PATCH books/isbn
@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json()
    if 'name' in request_data:
        Book.update_book_name(isbn, request_data['name'])
    if 'price' in request_data:
        Book.update_book_price(isbn, request_data['price'])
    return Response(status=204)


# Suppression d'un livre par isbn
# DELETE books/isbn
@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    if Book.delete_book(isbn):
        return Response(status=204)
    return Response(status=400)  # No book found


# Lancement du serveur
app.run(port=5000)