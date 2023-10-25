#!/usr/bin/python3
"""
Script that starts a simple flask web app
With seven routes
Two predefined & five dynamic
"""
from flask import Flask, render_template

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


# This is for an empty string
@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_dynamic_route(text="is cool"):
    """Return a dynamic route
    Then display the text of the route
    """
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>", strict_slashes=False)
def number_dynamic_route(n):
    """Return a dynamic route
    Then display the text of the route
    """
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template_route(n):
    """Return a dynamic route
    Then display the number in a HTML template
    """
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def odd_even_template_route(n):
    """Return a dynamic route
    Then display the number in a HTML template
    Whether its odd or even
    """
    return render_template("6-number_odd_or_even.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
