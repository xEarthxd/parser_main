import re, time
from multiprocessing import Process

from modules.Logger import log
from modules.DatabaseConnector import DatabaseConnector

class JobadsQueue(object):
    '''JobadsQueue find jobads that haven't been parsed in the database and insert into Queue.'''
    
    def __init__(self, connectionCredentials):
        from multiprocessing import Queue
        
        log("MasterMiner", "Initializing JobadsQueue")
        self.queue = Queue(1000)    #  init queue and set maxsize to 1000
        self.finishedAdding = False     #  flag if queue is finished adding
        
        self.inputDB = DatabaseConnector(**connectionCredentials).connect()   #  create connection to parsed jobads database (input)
        
    def tap_database_into_queue(self, filename):
        '''Tap jobads which parsed from arg: filename into the Queue.'''
        foldername = filename.split('.')[0]  #  remove .tar.gz from filename to get foldername
        
        folderNameCriteria = re.compile(".*{}.*".format(foldername))
        jobads = self.inputDB.find({ "file_name": folderNameCriteria })  #  string contain filename
        log("MasterMiner", "[JobadsQueue]  Found {} unmined jobads from {}".format(jobads.count(True), foldername))
        
        #  asynchrounously add jobads into queue
        self.adderProcess = Process(target=self._from_cursor_into_queue, args=(jobads, self.queue))  
        self.adderProcess.run()
        
    def _from_cursor_into_queue(self, cursor, queue):
        '''This method runs in subprocess'''
        
        log("MasterMiner", '[JobadsQueue - subprocess]  Adding jobads')
        for jobads in cursor:
            queue.put(jobads)
        
        time.sleep(0.1)     #  Stabilize non blocking put (make sure all are put)
        
        self.finishedAdding = True   
        
        log("MasterMiner", '[JobadsQueue - subprocess]  Finished adding jobads, queue is closed')
    
    def get(self, *arg, **kwarg):
        return self.queue.get(*arg, **kwarg)
    
    def empty(self):
        return self.queue.empty()

        