# app.py
from flask import Flask, render_template  # import flask

from activity_range import activity_range_bp
from time_selection import time_selection_bp
from home import home_bp

app = Flask(__name__)             # create an app instance
#
# @app.route("/")                   # at the end point /
# def hello():                      # call method hello
#     return "Hello World!"         # which returns "hello world"
#
#

# Set a secret key for the Flask application
app.secret_key = 'activity_tracker'

# Register the blueprints with the app
app.register_blueprint(home_bp)
app.register_blueprint(time_selection_bp)
app.register_blueprint(activity_range_bp)
# ... (other configurations and route definitions if any)

@app.route('/')
def homepage():
    return render_template('home.html',file_created = True)

if __name__ == '__main__':
    app.run(debug=True)
