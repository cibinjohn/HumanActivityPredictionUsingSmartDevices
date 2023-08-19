import json

import requests
from flask import Flask, render_template, request, Blueprint, session
from datetime import datetime
from src.env.environment_variables import APPCONFIG


activity_range_bp = Blueprint('activity_range', __name__)

app = Flask(__name__)
app.secret_key = "activity range"  # for encrypting the session

headers = {
        'Content-Type': 'application/json'
    }


@activity_range_bp.route('/timerange', methods=['GET'])
def index():
    return render_template('activity_range.html',selected_from_datetime = None, selected_to_datetime = None,activities = None)
# , date=None, time=None, milliseconds=None,
#                            to_date=None, to_time=None, to_milliseconds=None

@activity_range_bp.route('/rangesubmit', methods=['POST'])
def datetime_picker():
    # from_date = request.form['from_date']
    # to_date = request.form['to_date']
    selected_date = request.form['date']
    selected_time = request.form['time']
    selected_milliseconds = request.form['milliseconds']
    selected_to_date = request.form['to_date']
    selected_to_time = request.form['to_time']
    selected_to_milliseconds = request.form['to_milliseconds']
    # Convert the date strings to datetime objects
    # from_date = datetime.strptime(from_date, '%Y-%m-%dT%H:%M')
    # to_date = datetime.strptime(to_date, '%Y-%m-%dT%H:%M')
    print(selected_date, selected_time,
          selected_milliseconds,
          selected_to_date, selected_to_time, selected_to_milliseconds)
    # Perform any desired processing with the selected dates
    print("the selected date time is :", selected_date, selected_time, selected_milliseconds)
    print("after adding", selected_date + " " + selected_time + ":" + selected_milliseconds)
    selected_from_datetime = selected_date + " " + selected_time + ":" + selected_milliseconds
    selected_to_datetime = selected_to_date + " " + selected_to_time + ":" + selected_to_milliseconds
    print("now trying to hit api\n")

    # url = "http://localhost:7000/get_activity_timeinterval"
    url = "http://{}:{}/get_activity_timeinterval".format(APPCONFIG.hapd_api_host,
                                                          APPCONFIG.hapd_api_port)



    payload = json.dumps({
        "transaction_id": session.get('transaction_id'),
        "start_datetime": selected_from_datetime,
        "end_datetime": selected_to_datetime
    })
    # selected_datetime = "2017-07-12 12:23:20"

    response = requests.request("GET", url, headers=headers, data=payload)

    print("The activity on the  time range", response.text)

    print("in", response.text, type(response.text))
    # Convert JSON string to a Python dictionary
    data_dict = json.loads(response.text)

    print(data_dict,data_dict['code'])
    code = data_dict['code']
    if code == 200:
        print(data_dict['activities_and_recommendations'][0]['activity'])
        with open('mapping.json', 'r') as mapping:
            reco_mapping = json.load(mapping)
        print("reco_mapping", reco_mapping)
        print("data_dict", data_dict['activities_and_recommendations'])
        for data in data_dict['activities_and_recommendations']:
            print("data", data)
            if data['recommendation'] in reco_mapping:
                data['recommendation_title'] = reco_mapping[data['recommendation']]
        print("after appending", data_dict)
        activities = data_dict['activities_and_recommendations']
    else:
        activities = ""

    print(type(data_dict))  #
    return render_template('activity_range.html',selected_from_datetime = selected_from_datetime, selected_to_datetime = selected_to_datetime,
                           activities = activities)

# , date=selected_date, time=selected_time, milliseconds=selected_milliseconds, to_date=selected_to_date,
# to_time=selected_to_time, to_milliseconds=selected_to_milliseconds


if __name__ == '__main__':
    app.run(debug=True)