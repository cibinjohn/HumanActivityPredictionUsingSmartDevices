import os


class EnvironmentVariables():

    def __init__(self):

        self.model_path = os.getenv("MODEL_PATH","CHECKPOINTS/final_model.sav")
        self.port = os.getenv("PORT", 7000)
        self.host = os.getenv("HOST", "0.0.0.0")
        self.logfile = os.getenv("LOGFILE", "log.txt")

        self.mysql_database_user = os.getenv('db_root_user', 'root')
        self.mysql_database_password = os.getenv('db_root_password', 'super-secret-password')
        self.mysql_database_db = os.getenv('db_name', 'HumanActivityPredictionsDB')

        # self.mysql_database_host = os.getenv('MYSQL_SERVICE_HOST', 'localhost')
        self.mysql_database_host = os.getenv('MYSQL_SERVICE_HOST', 'localhost')
        self.mysql_database_port = int(os.getenv('MYSQL_SERVICE_PORT', 3310))

APPCONFIG = EnvironmentVariables()
