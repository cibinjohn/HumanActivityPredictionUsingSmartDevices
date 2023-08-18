from datetime import datetime

import pandas as pd
import requests
from flask import Flask, request
from flask_restful import Api, Resource

from env.environment_variables import APPCONFIG
from model.model import HumanActivityPredictor

app = Flask(__name__)
api = Api(app)

predictor = HumanActivityPredictor()
class Predictor(Resource):
    def get(self):
        return {'message': "Endpoint working successfully..."}

    def put(self):
        input_request = request.get_json()
        predictions, transaction_id = predictor.predict(pd.DataFrame(input_request["smartdevices_data"]))
        return {'results': predictions,
                'code':200,
                'transaction_id':transaction_id,
                'message':"Human activities predicted successfully"}


api.add_resource(Predictor, '/predict_activity')


# class DataBaseConnector(Resource):
#
#     def get(self):
#         response = "Hello, World! "
#
#         try:
#             local_api_response = requests.get(APPCONFIG.local_api_url)
#             if local_api_response.status_code == 200:
#                 response += local_api_response.text
#             else:
#                 response += "Error calling the local API"
#         except requests.exceptions.RequestException as e:
#             response += "Error calling the local API: " + str(e)
#
#             return response
#
# api.add_resource(DataBaseConnector, '/database')



class ActivityExtractorTimestamp(Resource):
    def get(self):
        input_request = request.get_json()
        transaction_id = input_request["transaction_id"]
        activity_datetime = datetime.strptime(input_request["datetime"], "%Y-%m-%d %H:%M:%S")

        response = predictor.get_recommendation_for_timestamp(transaction_id=transaction_id,
                                                              timestamp_to_compare=activity_datetime)
        return response


api.add_resource(ActivityExtractorTimestamp, '/get_activity_timestamp')

class ActivityExtractorTimeInterval(Resource):
    def get(self):
        input_request = request.get_json()
        transaction_id = input_request["transaction_id"]
        start_datetime = input_request["start_datetime"]
        end_datetime = input_request["end_datetime"]

        start_datetime = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.strptime(end_datetime, "%Y-%m-%d %H:%M:%S")


        response = predictor.get_recommendations_for_timeinterval(transaction_id=transaction_id,
                                                              start_datetime=start_datetime,
                                                                  end_datetime=end_datetime)
        return response


api.add_resource(ActivityExtractorTimeInterval, '/get_activity_timeinterval')
print(" APPCONFIG.host : ",APPCONFIG.host)
#
if __name__ == "__main__":

    app.run(debug=True, port=APPCONFIG.port, host=APPCONFIG.host)