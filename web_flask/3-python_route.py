#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    """ Function that returns Hello HBNB """
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """ Function that returns HBNB """
    return 'HBNB'


@app.route('/c/<text>')
def c(text):
    """ Function that returns C followed by text """
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/<text>')
def python(text='is cool'):
    """ Function that returns Python followed by text """
    return 'Python {}'.format(text.repalce('_', ' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
