import datetime
from pymongo import MongoClient

from modules.Configuration import getConfig

#  module: file that does the logging activity / message: logging message
def log(module, message):
    config = getConfig()['LOG_DATABASE']
    username = config['Username']
    password = config['Password']
    host = config['DatabaseAddress']
    databaseName = config['DatabaseName']
    collectionName = config['CollectionName']

    mongoURI = "mongodb://{}:{}@{}".format(username, password, host)
    cnx = MongoClient(mongoURI)[databaseName][collectionName]

    cnx.insert_one({ 'module': str(module), 'message': message, 'time': datetime.datetime.now() })

