#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask
from flask import render_template

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
def python(text):
    """ Function that returns Python followed by text """
    return 'Python {}'.format(text.repalce('_', ' '))


@app.route('/number/<int:n>')
def number(n):
    """ Fucntion that retuns n only if it is an integer"""
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>')
def number_template(n):
    """ Function that returns an HTML page only if n is an integer """
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
