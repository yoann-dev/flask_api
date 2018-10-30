from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    price = db.Column(db.Float, nullable=True)
    isbn = db.Column(db.Integer)

    def json(self):
        return { 'name': self.name, 'price': self.price, 'isbn': self.isbn }

    @staticmethod
    def add_book(_name, _price, _isbn):
        new_book = Book(name=_name, price=_price, isbn=_isbn)
        db.session.add(new_book)
        db.session.commit()

    @staticmethod
    def get_all_books():
        return [Book.json(book) for book in Book.query.all()]

    @staticmethod
    def get_book(_isbn):
        return Book.json(Book.query.filter_by(isbn=_isbn).first())

    @staticmethod
    def delete_book(_isbn):
        success = Book.query.filter_by(isbn=_isbn).delete()
        db.session.commit()
        return bool(success)

    @staticmethod
    def update_book_name(_isbn, _name):
        book = Book.query.filter_by(isbn=_isbn).first()
        book.name = _name
        db.session.commit()

    @staticmethod
    def update_book_price(_isbn, _price):
        book = Book.query.filter_by(isbn=_isbn).first()
        book.price = _price
        db.session.commit()

    @staticmethod
    def replace_book(_isbn, _name, _price):
        book = Book.query.filter_by(isbn=_isbn).first()
        book.name = _name
        book.price = _price
        db.session.commit()

    def __repr__(self):
        book_object = {
            'name': self.name,
            'price': self.price,
            'isbn': self.isbn
        }
        return json.dumps(book_object)