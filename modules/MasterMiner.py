import re
import os
import time
from multiprocessing import Process
from multiprocessing.queues import Empty

from pymongo import MongoClient

from modules.Logger import log
from modules.Configuration import getConfig
from modules.IndustryMiner import IndustryMiner
from modules.ProvinceMiner import ProvinceMiner
from modules.JobadsQueue import JobadsQueue
from exceptions import MiningRequiredFileNotFound

class MasterMiner(object):
    def __init__(self): 
        log("MasterMiner", "Initializing MasterMiner")
        self.miners = { "Industry": IndustryMiner(),
                        "Province": ProvinceMiner() }
        
        config_parsedJobads = getConfig()['PARSEDJOBADS_DATABASE']
        self.parsedJobadsDB = { 'username': config_parsedJobads['Username'], 
                                'password': config_parsedJobads['Password'], 
                                'host': config_parsedJobads['DatabaseAddress'], 
                                'port': '27017', 
                                'databaseName': config_parsedJobads['DatabaseName'], 
                                'collectionName': config_parsedJobads['CollectionName'] }
        
        config_statusdb = getConfig()['S3FILESPARSE_DATABASE']
        self.statusDB = { 'username': config_statusdb['Username'], 
                          'password': config_statusdb['Password'], 
                          'host': config_statusdb['DatabaseAddress'], 
                          'port': '27017', 
                          'databaseName': config_statusdb['DatabaseName'], 
                          'collectionName': config_statusdb['CollectionName'] }
    
    def _getFilename(self):
        '''Find_one from S3FilesParseStatus which is parsed but hasn't been mined'''
        
        mongoURI = "mongodb://{}:{}@{}:{}".format(self.statusDB['username'],
                                                  self.statusDB['password'],
                                                  self.statusDB['host'],
                                                  self.statusDB['port'])
        cnx = MongoClient(mongoURI)[self.statusDB['databaseName']][self.statusDB['collectionName']]
        
        filename = cnx.find_one({ 'parsed': True, 'mined': False })
        
        if(filename is None):
            raise MiningRequiredFileNotFound  #  No file in database that need to be mined
        else:    
            return filename['file_name']      #  use this filename to get jobads
     
    
    def _subprocess_job(self, jobadsQueue):
        mongoURI = "mongodb://{}:{}@{}:{}".format(self.statusDB['username'],
                                                  self.statusDB['password'],
                                                  self.statusDB['host'],
                                                  self.statusDB['port'])
        outputDB = MongoClient(mongoURI)[self.statusDB['databaseName']][self.statusDB['collectionName']]
        
        log("MasterMiner", "[MasterMiner - subprocess {}]  Doing job".format(os.getpid()))
        while(True):
            try:
                jobads = jobadsQueue.get(timeout=5)  #  dequeue jobads from the queue
            except Empty:                            #  Timeout occur
                if(jobadsQueue.finishedAdding):      #  Checkif the queue is already closed (finished adding)
                    break
            else:                                    #  Mine jobads
                #  TODO: mine data 
                #  TODO: insert
                #  TODO: check 
                pass

        log("MasterMiner", "[MasterMiner - subprocess {}]  Finished".format(os.getpid()))
    
    def start(self, num_process=2):
        '''This is the main method. Miner will tap files from database into queue and start mining.'''
        
        log("MasterMiner", "[MasterMiner]  Starting MasterMiner")
        
        #  Create jobads queue
        targetFile = self._getFilename()                                     #  find the file that need to be mined
        
        self.jobadsQueue = JobadsQueue(self.parsedJobadsDB)            #  create jobadsQueue, set credentials
        self.jobadsQueue.tap_database_into_queue(filename=targetFile)  #  start adding jobasd into jobadsQueue
        
        #  Map spawn subprocesses to subscribe queue
        processes = [Process(target=self._subprocess_job, args=(self.jobadsQueue, )) for i in range(num_process)]
        for p in processes:
            p.start()
        
        for p in processes:
            p.join()

        log("MasterMiner", "[MasterMiner]  Finished MasterMiner")