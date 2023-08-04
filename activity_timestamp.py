from flask import Flask, flash, request, redirect, render_template

app = Flask(__name__)

app.secret_key = "secret key activity"  # for encrypting the session


@app.route('/datetime')
def index():
    return render_template('activity_timestamp.html')


@app.route('/chumma')
def chumma():
    print("in chumma")
    return render_template('time_selection.html')


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app
