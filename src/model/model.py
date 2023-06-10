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

    def predict(self, input_df):
        print("input_df : ",input_df)
        print(input_df.columns)
        timestamp_df = input_df[['timestamp']]
        features_df = input_df[self.features]

        # preprocessing
        X_test_normalized = self.preprocess(features_df)

        # prediction
        prediction = self.model.predict(X_test_normalized)

        timestamp_df["prediction"] = pd.Series([self.label_reverse_dict[item] for item in prediction])
        return [value for key, value in timestamp_df.transpose().to_dict().items() ]


if __name__ == "__main__":
    obj = HumanActivityPredictor()

    df = pd.read_csv("/home/cibin/Desktop/lambton/TERM2/capstone/notebooks/data/model_v1/test.csv")
    # df = df[FEATURES]

    prediction = obj.predict(df.head())
    print(prediction)
