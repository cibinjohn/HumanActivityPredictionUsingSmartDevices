import pickle
import pandas as pd
from env.environment_variables import APPCONFIG
from log.cj_logger import cj_logger
from db.hapd_db import TransactionOperations, PredictionOperations

from model.constants import FEATURES


# class PreProcesser(TransactionOperations,PredictionOperations):
#
#     def __init__(self):
#
#         super().__init__()
#         self.load_normalizer()
#
#     def load_normalizer(self):
#         cj_logger.info("Loading normalizer")
#         self.scaler = pickle.load(open(APPCONFIG.normalization_file_path, 'rb'))
#         cj_logger.info("Loaded normalizer successfully")
#
#     def preprocess(self, df):
#         X_test_normalized = self.normalize(df)
#         return X_test_normalized
#
#     def normalize(self,  X_test_df):
#
#         X_test_normalized = self.scaler.transform(X_test_df)
#
#         return X_test_normalized

class PreProcesser(TransactionOperations, PredictionOperations):

    def __init__(self):
        self.features = FEATURES
        super().__init__()

    def preprocess(self, df):
        df.to_csv("data.csv",index=None)
        cj_logger.info('Preprocess start')
        cj_logger.info("1. df shape %s",str(df.shape))

        cj_logger.info('1.b df.columns : %s',str(df.columns))
        # df = df[['timestamp'] + self.features]
        cj_logger.info("2. df shape %s",str(df.shape))

        df.timestamp = pd.to_datetime(df.timestamp)
        cj_logger.info("3......")

        # rounding the timestamp into second level
        df['timestamp'] = df['timestamp'].dt.round('1s')
        cj_logger.info("4......")

        for feature in self.features:
            cj_logger.info('typecasting %s',feature)
            df[feature] = df[feature].map(lambda x: float(x))
        cj_logger.info(str(df.dtypes))


        df = df.groupby("timestamp").mean()
        cj_logger.info("3. df shape %s",str(df.shape))

        df.reset_index(inplace=True)

        df = self.impute_missing_values(df)
        cj_logger.info("df shape %s",str(df.shape))

        cj_logger.info('Preprocess end')

        timestamp_df = df[['timestamp']]
        features_df = df.drop(columns=['timestamp'])
        return features_df.values, timestamp_df

    def impute_missing_values(self, data_df):
        cj_logger.info('impute_missing_values start')
        cj_logger.info("data_df shape %s",str(data_df.shape))
        for feature in self.features:

            if data_df[feature].isna().sum()==0:
                continue

            # Forward fill missing values for the succeeding 60 seconds
            data_df[feature] = data_df[feature].fillna(method='ffill', limit=60)

            # Backward fill missing values for the preceeding 60 seconds
            data_df[feature] = data_df[feature].fillna(method='bfill', limit=60)

            # Imputing the remaining missing values with median
            median = data_df[feature].median()
            data_df[feature].fillna(median, inplace=True)

        cj_logger.info('impute_missing_values end')
        return data_df
#
#
# class PreProcesser():
#
#     def __init__(self):
#         self.features = FEATURES
#         super().__init__()
#
#     def preprocess(self, df):
#         # cj_logger.info('Preprocess start')
#         # cj_logger.info("1. df shape %s",str(df.shape))
#
#         # columns_rename_dict = {col:"Phone_"+col for col in df.columns if col!='timestamp'}
#         # df.rename(columns=columns_rename_dict, inplace=True)
#         # cj_logger.info('1.b df.columns : %s',str(df.columns))
#         # df = df[['timestamp'] + self.features]
#         # cj_logger.info("2. df shape %s",str(df.shape))
#
#         df.timestamp = pd.to_datetime(df.timestamp)
#         # cj_logger.info("3......")
#
#         # rounding the timestamp into second level
#         df['timestamp'] = df['timestamp'].dt.round('1s')
#         # cj_logger.info("4......")
#
#         df = df.groupby("timestamp").mean()
#         # cj_logger.info("3. df shape %s",str(df.shape))
#
#         df.reset_index(inplace=True)
#
#         df = self.impute_missing_values(df)
#         # cj_logger.info("df shape %s",str(df.shape))
#
#         # cj_logger.info('Preprocess end')
#
#         timestamp_df = df[['timestamp']]
#         features_df = df.drop(columns=['timestamp'])
#         return features_df.values, timestamp_df
#
#     def impute_missing_values(self, data_df):
#         # cj_logger.info('impute_missing_values start')
#         # cj_logger.info("data_df shape %s",str(data_df.shape))
#         # print(data_df.dtypes)
#         # print(data_df.isna().sum())
#         for feature in self.features:
#             # Forward fill missing values for the succeeding 60 seconds
#             if data_df[feature].isna().sum()==0:
#                 continue
#             data_df[feature] = data_df[feature].fillna(method='ffill', limit=60)
#
#             # Backward fill missing values for the preceeding 60 seconds
#             data_df[feature] = data_df[feature].fillna(method='bfill', limit=60)
#
#             # Imputing the remaining missing values with median
#             median = data_df[feature].median()
#             data_df[feature].fillna(median, inplace=True)
#
#         # cj_logger.info('impute_missing_values end')
#         return data_df



if __name__ == "__main__":
    # smart_phone = pd.read_csv('/home/cibin/Desktop/lambton/TERM2/capstone/notebooks/data_12_july.csv')
    smart_phone = pd.read_csv('/home/cibin/Desktop/lambton/TERM2/capstone/pipeline/HumanActivityPredictionUsingSmartDevices/data.csv')

    obj = PreProcesser()
    x = obj.preprocess(smart_phone)
    print(x)
