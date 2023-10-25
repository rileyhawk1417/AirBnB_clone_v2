#!/usr/bin/python3
"""
Script that starts a simple flask web app
Renders a list of states
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def states_list_route():
    """Display HTML list with states"""
    states = storage.all(State).values()
    sorted_list = sorted(states, key=lambda x: x.name)
    return render_template("8-cities_by_states.html", states=sorted_list)


@app.teardown_appcontext
def teardown_session(exception):
    """Close the session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
