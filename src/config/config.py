"""Reads the basic configuration for DB and logger"""
import logging
import json
import os

environment = os.environ.get("ENVIRONMENT", "DEV").upper()
if environment == "PROD" or environment == "PRODUCTION" or environment == "PRD":
    config_file = "config.prod.json"
else:
    config_file = "config.stage.json"

with open(config_file) as in_config:
    _config_input = json.load(in_config)

HOSTNAME = _config_input['HOSTNAME']
PORT = _config_input['PORT']
USER = _config_input['USER']
PASS = _config_input['PASS']
DATABASE = _config_input['DATABASE']
USER_TABLE = _config_input['USER_TABLE']
MESSAGE_TABLE = _config_input['MESSAGE_TABLE']
SUBSCRIPTION_TABLE = _config_input['SUBSCRIPTION_TABLE']
USER_URL = _config_input['USER_URL']
MESSAGE_URL = _config_input['MESSAGE_URL']

LOGLEVEL = getattr(logging, _config_input["LOGLEVEL"])
if not isinstance(LOGLEVEL, int):
    LOGLEVEL = logging.INFO