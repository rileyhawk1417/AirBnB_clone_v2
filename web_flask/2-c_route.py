#!/usr/bin/python3
"""
Script that starts a simple flask web app
With three routes
Two predefined & one dynamic
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_route():
    """Return a greeting"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb_route():
    """Return a hbnb string"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_dynamic_route(text):
    """Return a dynamic route
    Then display the text of the route
    """
    return "C {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
