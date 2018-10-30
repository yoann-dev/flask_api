from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)

print(app.config['SQLALCHEMY_DATABASE_URI'])


class Book(db.Model):
        __tablename__ = 'books'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), nullable=True)
        price = db.Column(db.Float, nullable=True)
        isbn = db.Column(db.Integer)