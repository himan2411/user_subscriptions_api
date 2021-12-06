"""This file creates a mysql driver with required configs"""
import os
import utils
import pymysql
from config.config import HOSTNAME, USER, PASS, PORT, DATABASE 

def create_sql_engine():
    SQL_HOST = os.environ.get('SQL_SERVER') or HOSTNAME
    SQL_USER = os.environ.get('SQL_USER') or USER
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD') or PASS
    SQL_DATABASE = os.environ.get('SQL_DATABASE') or DATABASE
    SQL_PORT = os.environ.get('SQL_DATABASE') or PORT

    # conn = sqlalchemy.create_engine(
    #     f"mysql+mysqldb://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}/{SQL_DATABASE}?charset=utf8mb4",
    #     pool_size=16, max_overflow=16, pool_pre_ping=True, pool_recycle=3600)

    conn = pymysql.connect(host=SQL_HOST, port = SQL_PORT, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
    return conn