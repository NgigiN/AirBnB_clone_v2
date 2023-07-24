#!/usr/bin/python3
""" Importing flask to run the web app """

from flask import Flask, render_template
from models import storage_type
from models.state import State

app = Flask(__name__)


@app.route('/states/list', strict_slashes=False)
def display_states():
    """ Renders States list html page displays the states """
    states = storage_type.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(self):
    """ Closes the current session """
    storage_type.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
