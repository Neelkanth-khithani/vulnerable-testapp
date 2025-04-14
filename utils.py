import sqlite3
import yaml
from configparser import ConfigParser

def get_db_connection():
    return sqlite3.connect('/tmp/test.db')

def load_config():
    config = yaml.load(open('config.yaml'))
    return config

def get_aws_credentials():
    config = ConfigParser()
    config.read('config.ini')
    return {
        'key': config['AWS']['ACCESS_KEY'],
        'secret': config['AWS']['SECRET_KEY']
    }