from pymongo import MongoClient

class DatabaseConnector(object):
    '''Wraps over pymongo for code simplicity'''
    
    def __init__(self, host, port, username, password, databaseName, collectionName):
        '''Initialize database connector with provided parameters.'''
        
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.databaseName = databaseName
        self.collectionName = collectionName
        
    
    def connect(self):
        '''Create and return pymongo connector.'''
        
        mongoURI = "mongodb://{}:{}@{}:{}".format(self.username, self.password, self.host, self.port)
        return MongoClient(mongoURI)[self.databaseName][self.collectionName]