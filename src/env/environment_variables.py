import os

from src.log.cj_logger import cj_logger


class EnvironmentVariables():

    def __init__(self):

        self.hapd_api_port = os.getenv("HAPD_API_PORT", 7000)
        self.hapd_api_host = os.getenv("HAPD_API_HOST", "0.0.0.0")
        self.sql_port = os.getenv("SQL_PORT", 3010)
        self.sql_host = os.getenv("SQL_HOST", "0.0.0.0")
        self.logfile = os.getenv("LOGFILE", "log.txt")

        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = os.getenv("PORT", 7004)

        cj_logger.info("Environment variables : ")
        cj_logger.info("HAPD_API_HOST : {} ".format(self.hapd_api_host))
        cj_logger.info("HAPD_API_PORT : {} ".format(self.hapd_api_port))


APPCONFIG = EnvironmentVariables()