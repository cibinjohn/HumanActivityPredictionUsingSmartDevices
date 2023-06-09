import os


class EnvironmentVariables():

    def __init__(self):

        self.model_path = os.getenv("MODEL_PATH")
        self.normalization_file_path = os.getenv("NORMALIZATION_FILE_PATH", None)
        self.port = os.getenv("PORT", 7000)
        self.host = os.getenv("HOST", "0.0.0.0")
        self.logfile = 'log.txt'

APPCONFIG = EnvironmentVariables()