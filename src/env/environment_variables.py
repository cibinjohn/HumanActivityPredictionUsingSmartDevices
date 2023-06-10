import os


class EnvironmentVariables():

    def __init__(self):

        self.model_path = os.getenv("MODEL_PATH","CHECKPOINTS/model_v1.sav")
        self.normalization_file_path = os.getenv("NORMALIZATION_FILE_PATH", "CHECKPOINTS/scalar.pickle")
        self.port = os.getenv("PORT", 7000)
        self.host = os.getenv("HOST", "0.0.0.0")
        self.logfile = os.getenv("LOGFILE", "log.txt")

APPCONFIG = EnvironmentVariables()