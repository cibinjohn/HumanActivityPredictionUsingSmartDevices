import datetime
import pickle

import pandas as pd

from env.environment_variables import APPCONFIG
from log.cj_logger import cj_logger
from model.constants import FEATURES, LABEL_DICT
from model.preprocess import PreProcesser


class HumanActivityPredictor(PreProcesser):

    def __init__(self):
        super().__init__()
        self.load_model()
        self.load_normalizer()
        self.label_dict = LABEL_DICT
        self.label_reverse_dict = {value: key for key, value in self.label_dict.items()}
        self.features = FEATURES

    def load_model(self):
        cj_logger.info("Loading model")
        self.model = pickle.load(open(APPCONFIG.model_path, 'rb'))
        cj_logger.info("Loaded model successfully")

    @staticmethod
    def add_recommendation(x):
        pass

    def predict(self, input_df):
        transaction_id = self.create_transaction()
        # updation of db
        self.update_transaction_status(transaction_id=transaction_id,
                                       status=0)
        try:

            timestamp_df = input_df[['timestamp']]
            features_df = input_df[self.features]

            # preprocessing
            X_test_normalized = self.preprocess(features_df)

            # prediction
            prediction = self.model.predict(X_test_normalized)
            timestamp_df["prediction"] = pd.Series([self.label_reverse_dict[item] for item in prediction])

            # recommendation
            timestamp_df["recommendation"] = timestamp_df.prediction.map(lambda x: x+"_recommendation")

            # updation of db

            cj_logger.info("Updating db")
            records_df = timestamp_df.rename(columns={
                                        "prediction":"ACTIVITY",
                                        "recommendation":"RECOMMENDATION",
                                        "timestamp":"ACTIVITY_DATETIME"
                                         })
            records_df['TRANSACTION_ID'] = transaction_id
            records_df['CREATED_AT'] = str(datetime.datetime.now())


            self.add_predictions_to_db(predictions_df=records_df)
            cj_logger.info("Predictions updated")
            self.update_transaction_status(transaction_id=transaction_id,
                                           status=1)
            cj_logger.info("DB updated")


        except Exception as err:
            cj_logger.error(err)
            self.update_transaction_status(transaction_id=transaction_id,
                                           status=2)




        return [value for key, value in timestamp_df.transpose().to_dict().items()], transaction_id


if __name__ == "__main__":
    obj = HumanActivityPredictor()

    df = pd.read_csv("/home/cibin/Desktop/lambton/TERM2/capstone/notebooks/data/model_v1/test.csv")
    # df = df[FEATURES]

    prediction, transaction_id = obj.predict(df.head())
    print("transaction_id : ",transaction_id)
    print(prediction)
