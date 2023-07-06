import pickle

from env.environment_variables import APPCONFIG
from log.cj_logger import cj_logger
from db.hapd_db import TransactionOperations, PredictionOperations

class PreProcesser(TransactionOperations,PredictionOperations):

    def __init__(self):

        super().__init__()
        self.load_normalizer()

    def load_normalizer(self):
        cj_logger.info("Loading normalizer")
        self.scaler = pickle.load(open(APPCONFIG.normalization_file_path, 'rb'))
        cj_logger.info("Loaded normalizer successfully")

    def preprocess(self, df):
        X_test_normalized = self.normalize(df)
        return X_test_normalized

    def normalize(self,  X_test_df):

        X_test_normalized = self.scaler.transform(X_test_df)

        return X_test_normalized

if __name__=="__main__":
    obj = PreProcesser()
