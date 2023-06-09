import pandas as pd
from flask import Flask, request
from flask_restful import Api, Resource

from env.environment_variables import APPCONFIG
from src.model.model import HumanActivityPredictor

app = Flask(__name__)
api = Api(app)

predictor = HumanActivityPredictor()
class HelloWorld(Resource):
    def get(self):
        return {'message': "Endpoint working successfully..."}

    def put(self):
        input_request = request.get_json()

        return {'results': predictor.predict(pd.DataFrame(input_request["smartdevices_data"])),
                'code':200,
                'message':"Human activities predicted successfully"}


api.add_resource(HelloWorld, '/predict_activity')


if __name__ == "__main__":

    app.run(debug=True, port=APPCONFIG.port)