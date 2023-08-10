from flask import Flask, render_template, request, redirect, flash, Blueprint, url_for, session
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import csv
import json
import requests

home_bp = Blueprint('home', __name__)

app = Flask(__name__)


# app.secret_key = "secret keys"  # for encrypting the session

@home_bp.route('/')
def home():
    return render_template('home.html',file_created = None)


# save the file location in uploads folder

# It will allow below 16MB contents only, you can change it
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
path = os.getcwd()
print("path :", path)

# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set([ 'csv', 'xlsx'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@home_bp.route('/timestamp', methods=['POST'])
def timestamp():
    print("i clicked on timestamp button")
    return redirect(url_for('time_selection.index'))

@home_bp.route('/timerange', methods=['POST'])
def timerange():
    print("i clicked on timerange button")
    return redirect(url_for('activity_range.index'))

@home_bp.route('/', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        NEW_FILE = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print("the file created", NEW_FILE)
        flash('File successfully uploaded!!! Please select any of the options below to see your result','success')
        file_created = True

        print("file uploaded")
        # Driver Code

        # Decide the two file paths according to your
        # computer system
        print("upload folder", UPLOAD_FOLDER, "filename", filename)
        file_extension = filename.rsplit('.')
        print("the result", file_extension)
        csvFilePath = NEW_FILE
        # UPLOAD_FOLDER + "\'" + rem_extension[0] + '.json'
        jsonFilePath = os.path.join(app.config['UPLOAD_FOLDER'], file_extension[0] + '.json')
        print("the new file path with json extension", jsonFilePath)
        # Call the make_json function
        make_json(csvFilePath, jsonFilePath)
        # return redirect(request.url)
        return render_template('home.html', file_created=file_created)




# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
    # create a dictionary
    data = {}
    element = []
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        print("csvReader read: ", csvReader)
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Assuming a column named 'No' to
            # be the primary key

            # key = rows['customer_id']
            element.append(rows)
        data['smartdevices_data'] = element
    # Open a json writer, and use the json.dumps()
    # function to dump data
    print("data - 1", data)
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

    print("CSV file converted to JSON and sent to DB", data)
    url = "http://localhost:7000/predict_activity"

    payload = json.dumps(data, indent=4)
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print("The response is: ", response.text)
    response_dict = json.loads(response.text)

    print(response_dict)
    print("res",response_dict["transaction_id"])
    session['transaction_id'] = response_dict["transaction_id"]


if __name__ == '__main__':
    app.run()
