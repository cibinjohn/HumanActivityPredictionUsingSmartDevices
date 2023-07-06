"""To create mariadb session"""
import os

from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Mariadb
DB_USER = os.environ.get("SQL_USER","root")
DB_PASS = os.environ.get("SQL_PASS","password")
DB_HOST = os.environ.get("SQL_HOST","localhost")
DB_NAME = os.environ.get("SQL_DB_NAME","HumanActivityPredictionsDB")
DB_PORT = os.environ.get("SQL_PORT", "3310")
DB_TYPE = os.environ.get("SQL_DB_TYPE", "mysql")
DB_DRIVER = os.environ.get("SQL_DB_DRIVER", "pymysql")
POOL_SIZE = os.environ.get("SQL_DB_POOL_SIZE", 100)
MAX_OVERFLOW = os.environ.get("SQL_DB_MAX_OVERFLOW", 50)
POOL_TIMEOUT = os.environ.get("SQL_DB_POOL_TIMEOUT", 300)

Base = declarative_base()


def check_database_in_server(db_name):
    """create database if not exist"""
    inspect_engine = inspect(db_engine)
    db_list = inspect_engine.get_schema_names()
    if db_name not in db_list:
        db_engine.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")


try:
    db_url = f"{DB_TYPE}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}"
    db_engine = create_engine(db_url)
    check_database_in_server(db_name=DB_NAME)
    engine = create_engine(f"{db_url}/{DB_NAME}", pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW,
                           pool_recycle=180,
                           #convert_unicode=True,
                           echo=False, echo_pool=True,
                           pool_timeout=POOL_TIMEOUT)

    print("connected")
except Exception as e:
    engine = None
    print("DB engine create error %s" % e)


class DbSessionMaker:
    @staticmethod
    def create_db_engine(db_name):
        """

        :return:
        """
        global engine
        global db_engine
        if not engine or engine.url.database != db_name:
            db_engine = create_engine(db_url)
            check_database_in_server(db_name)
            engine = create_engine(f"{db_url}/{db_name}", pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW,
                                   pool_recycle=180, convert_unicode=True, echo=False, echo_pool=True,
                                   pool_timeout=POOL_TIMEOUT)
        _session_factory = sessionmaker(bind=engine)
        _session_factory.expire_on_commit = False
        Base.metadata.create_all(bind=engine)
        print(engine.pool.status())
        return engine, _session_factory

    def get_new_db_session(self, db_name=None):
        """

        :return:
        """
        test_env = os.environ.get("CE_TEST_ENV")
        db_name = "test_database" if test_env == "True" else db_name or os.environ.get("CE_MARIADB_NAME")
        self.engine, _session_factory = self.create_db_engine(db_name)
        return self.engine, _session_factory()
