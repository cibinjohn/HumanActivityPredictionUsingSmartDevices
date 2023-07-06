import uuid
import datetime
from datetime import datetime, timedelta

import uuid

import pandas as pd
from sqlalchemy import insert, func, text

from src.db.error_responses import PREDICTION_IN_PROGRESS_ERROR, PIPELINE_FAILURE_ERROR, UNKNOWN_ERROR, \
    NO_RECORDS_ERROR_TIMESTAMP, NO_RECORDS_ERROR_TIMEINTERVAL
from src.db.session_maker import DbSessionMaker
from src.db.tables.predictions import Predictions
from src.db.tables.transactions import Transactions
from src.model.constants import STATUS_MESSAGE_DICT


class TransactionOperations():

    def __init__(self):
        self.engine, self.session = DbSessionMaker().get_new_db_session(Transactions.__table_args__.get('schema'))
        print("Connected to DB...")

    def create_transaction(self):
        transaction_id = str(uuid.uuid4())

        self.session.execute(
            insert(Transactions),
            [
                {"ID": transaction_id,
                 "STATUS": 0,
                 'MESSAGE': "In progress",
                 'CREATED_AT': datetime.now(),
                 'MODIFIED_AT': datetime.now()
                 }
            ],
        )
        self.session.commit()

        return transaction_id

    def update_transaction_status(self, transaction_id, status, message=None):
        message = message if message else STATUS_MESSAGE_DICT[status]

        row = self.session.query(Transactions).filter_by(ID=transaction_id).first()
        row.STATUS = status
        row.MESSAGE = message
        row.MODIFIED_AT = datetime.now()
        self.session.commit()

    def get_all_transactions(self):
        transactions_df = pd.DataFrame(self.session.query(Transactions.ID,
                                                          Transactions.STATUS,
                                                          Transactions.MESSAGE,
                                                          Transactions.CREATED_AT,
                                                          Transactions.MODIFIED_AT
                                                          ).all())

        return transactions_df

    def get_transaction_status(self, transaction_id):
        status = self.session.query(Transactions.STATUS).filter_by(ID=transaction_id).first()[0]
        return status

    def get_recommendation_for_timestamp(self, transaction_id, timestamp_to_compare):
        # extracts the activity of the user nearest to the 'timestamp_to_compare' if there is any with in one hour
        # window of 'timestamp_to_compare'
        print(transaction_id, timestamp_to_compare)
        response = {
        }

        status = self.get_transaction_status(transaction_id=transaction_id)

        if status == 1:
            # Define the minimum time difference of 1 hour
            minimum_time_difference = timedelta(hours=1)

            # Calculate the minimum timestamp by subtracting the minimum time difference
            minimum_timestamp = timestamp_to_compare - minimum_time_difference
            maximum_timestamp = timestamp_to_compare + minimum_time_difference

            # Query the nearest ACTIVITY_DATETIME with the extra condition
            # Query the nearest ACTIVITY_DATETIME with the extra condition
            records = self.session.query(
                Predictions.ACTIVITY,
                Predictions.RECOMMENDATION,
                Predictions.ACTIVITY_DATETIME
            ).filter(
                Predictions.ACTIVITY_DATETIME <= maximum_timestamp,
                Predictions.ACTIVITY_DATETIME >= minimum_timestamp
            ).order_by(
                func.abs(
                    func.timestampdiff(
                        text('SECOND'),
                        Predictions.ACTIVITY_DATETIME,
                        timestamp_to_compare
                    )
                )
            ).first()

            if records:
                activity, recommendation, date_time = records
                date_time = str(date_time)
                response = {
                    "activity": activity,
                    "recommendation": recommendation,
                    "date_time": date_time,
                    "code": 200,
                    "message": "Predictions extracted successfully"
                }
            else:
                response = NO_RECORDS_ERROR_TIMESTAMP



        elif status == 0:
            response = PREDICTION_IN_PROGRESS_ERROR

        elif status == 2:
            response = PIPELINE_FAILURE_ERROR

        else:
            response = UNKNOWN_ERROR
        return response

    def get_recommendations_for_timeinterval(self, transaction_id, start_datetime, end_datetime):
        # Extracts the activity of the user within the specified datetime range
        print(transaction_id, start_datetime, end_datetime)
        response = {}

        status = self.get_transaction_status(transaction_id=transaction_id)

        if status == 1:
            # Query the activity within the specified datetime range
            records = self.session.query(
                Predictions.ACTIVITY,
                Predictions.RECOMMENDATION,
                Predictions.ACTIVITY_DATETIME
            ).filter(
                Predictions.ACTIVITY_DATETIME >= start_datetime,
                Predictions.ACTIVITY_DATETIME <= end_datetime
            ).order_by(
                Predictions.ACTIVITY_DATETIME
            ).all()

            if records:
                activities_and_recommendations_dict = [{"activity": record[0],
                                                   "recommendation": record[1],
                                                   "date_time": str(record[2])} for record in records]

                response = {
                    "activities_and_recommendations": activities_and_recommendations_dict,
                    "code": 200,
                    "message": "Predictions extracted successfully"
                }
            else:
                response = NO_RECORDS_ERROR_TIMEINTERVAL

        elif status == 0:
            response = PREDICTION_IN_PROGRESS_ERROR

        elif status == 2:
            response = PIPELINE_FAILURE_ERROR

        else:
            response = UNKNOWN_ERROR

        return response

    def delete_all_transactions(self):
        self.session.query(Transactions).delete()

        # Commit the changes
        self.session.commit()


class PredictionOperations():

    def __init__(self):
        self.engine, self.session = DbSessionMaker().get_new_db_session(Predictions.__table_args__.get('schema'))
        print("Connected to DB...")

    def add_predictions_to_db(self, predictions_df):
        predictions_df['ID'] = [str(uuid.uuid4()) for _ in range(len(predictions_df))]

        # predictions_df.drop(columns=['TRANSACTION_ID'], inplace=True)

        predictions_df.to_sql(Predictions.__tablename__,
                              con=self.engine,
                              if_exists='append',
                              index=False)

    def get_all_predictions(self):
        predictions_df = pd.DataFrame(self.session.query(
            Predictions.TRANSACTION_ID,
            Predictions.ACTIVITY_DATETIME,
            Predictions.ACTIVITY,
            Predictions.RECOMMENDATION,
            Predictions.CREATED_AT
        ).all())

        return predictions_df

    def delete_all_predictions(self):
        self.session.query(Predictions).delete()

        # Commit the changes
        self.session.commit()


if __name__ == "__main__":
    print(1)

    trasactions_obj = TransactionOperations()
    predictions_obj = PredictionOperations()
    # #
    # trasactions_obj.delete_all_transactions()
    # predictions_obj.delete_all_predictions()
    #
    # print(trasactions_obj.create_transaction())
    #
    transactions_df = trasactions_obj.get_all_transactions()
    print(transactions_df)
    #
    # # print(obj.create_transaction())
    # # obj.delete_all_transactions()
    predictions_df = predictions_obj.get_all_predictions()
    print(predictions_df)
    #
    transactions_df.to_csv("transactions.csv", index=None)
    predictions_df.to_csv("predictions.csv", index=None)
    #
    # obj = TransactionOperations()
    #
    # transaction_id = 'bcfe057d-8482-4c25-a6ff-c47cad429d72'
    #
    # print(obj.get_transaction_status(transaction_id=transaction_id))
    #
    # # # date_string="2017-07-12 12:23:20"
    # # date_string="2017-07-12 13:22:02"
    # # sample_dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    # #
    # # print(obj.get_recommendation_for_timestamp(transaction_id=transaction_id,
    # #                                            timestamp_to_compare=sample_dt))
    #
    # start_date_string = "2017-07-12 12:22:02"
    # end_date_string = "2017-07-12 12:22:03"
    # start_date = datetime.strptime(start_date_string, "%Y-%m-%d %H:%M:%S")
    # end_date = datetime.strptime(end_date_string, "%Y-%m-%d %H:%M:%S")
    #
    # activitites_recommendations = obj.get_recommendations_for_timeinterval(transaction_id=transaction_id,
    #                                                                        start_datetime=start_date,
    #                                                                        end_datetime=end_date)
    # print(activitites_recommendations)
    # print(pd.DataFrame(activitites_recommendations['activities_and_recommendations']))




