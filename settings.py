from flask import Flask
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' \
                                        + os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'meow'