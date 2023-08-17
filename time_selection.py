from flask import Flask, render_template, request, redirect, flash, Blueprint, session, jsonify
import requests
import json
# import MAPPING from mapping.json

time_selection_bp = Blueprint('time_selection', __name__)

app = Flask(__name__)
app.secret_key = "time selection"  # for encrypting the session

headers = {
        'Content-Type': 'application/json'
    }

# Sample activities for demonstration purposes
activities_data = {
        "activity": "In computer",
        "recommendation": "In computer_recommendation",
        "date_time": "2017-07-12 12:23:20",
        "code": 200,
        "message": "Predictions extracted successfully"
    }

@time_selection_bp.route('/timestamp', methods=['GET'])
def index():
    return render_template('time_selection.html', activities=None, selected_datetime=None)

@time_selection_bp.route('/datetime', methods=['POST'])
def datetime():
    selected_date = request.form['date']
    selected_time = request.form['time']
    selected_milliseconds = request.form['milliseconds']
    # activities = get_activities(selected_datetime)

    print("the selected date time is :",selected_date,selected_time,selected_milliseconds)
    print("after adding",selected_date+" "+selected_time+":"+selected_milliseconds)
    selected_datetime = selected_date+" "+selected_time+":"+selected_milliseconds
    print("now trying to hit api\n")

    url = "http://localhost:7000/get_activity_timestamp"

    payload = json.dumps({
        "transaction_id": session.get('transaction_id'),
        "datetime": selected_datetime
    })
    # selected_datetime = "2017-07-12 12:23:20"

    response = requests.request("GET", url, headers=headers, data=payload)

    print("The activity on the particular time",response.text)

    print("in",response.text, type(response.text) )
    # Convert JSON string to a Python dictionary
    data_dict = json.loads(response.text)
    with open('mapping.json','r') as mapping:
        reco_mapping = json.load(mapping)
    print("reco_mapping", reco_mapping)
    print("data_dict",data_dict)
    code = data_dict['code']
    if code == 200:
        # add new variable to save image related to the recommendation
        if data_dict['recommendation'] in reco_mapping:
            data_dict['recommendation_title'] = reco_mapping[data_dict['recommendation']]
        print("after appending",data_dict)
        activities = data_dict
    else:
        print("not success")
        activities = ""
        message = data_dict['message']
    print(data_dict)
    print(type(data_dict))  #
    return render_template('time_selection.html', activities=activities, selected_datetime=selected_datetime)



def get_activities(selected_datetime):
    # Replace this with a function to fetch activities from a database or external source
    return activities_data.get("2017-07-12 12:23:20", [])


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app
