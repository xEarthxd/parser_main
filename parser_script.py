import os
import hashlib
import datetime

from pymongo import MongoClient

from modules.Configuration import getConfig
from modules.Logger import log

class parsers(object):
    def __init__(self):
        config_init = getConfig()['S3FILESPARSE_DATABASE']
        self.DB_NAME_INIT = config_init['databasename']
        self.COLLECTION_NAME_INIT = config_init['collectionname']
        self.cnx_INIT = MongoClient("mongodb://{}:{}@{}:27017".format(config_init['username'], config_init['password'], config_init['databaseaddress']))

        config_parser = getConfig()['PARSEDJOBADS_DATABASE']
        DB_NAME = config_parser['databasename']
        COLLECTION_NAME = config_parser['collectionname']
        self.cnx = MongoClient("mongodb://{}:{}@{}:27017".format(config_parser['username'], config_parser['password'], config_parser['databaseaddress']))[DB_NAME][COLLECTION_NAME]

        self.parsed_false = self.cnx_INIT[self.DB_NAME_INIT][self.COLLECTION_NAME_INIT].find_one_and_update({'parsed' : False}, {'$set': {'parsed': 'locked'}})
        self.parsing_id = self.parsed_false['_id']
        self.file_to_parse = self.parsed_false['file_name']
        
        self.queue_manager_is_done = False
        self.count_success = 0
        self.count_duplicate = 0
        self.count_error = 0
        self.init_file_name = 'need_to_parse' + '/' + self.file_to_parse.split('.')[0]
        self.main_file_name = self.file_to_parse
        print(True)
    
    def get_file_name(self):
        return self.main_file_name
    
    def find_parser(self, file_name):
        
        from parsers.jobant_parser import jobant_parser
        from parsers.jobbkk_parser import jobbkk_parser
        from parsers.jobsawasdee_parser import jobsawasdee_parser
        from parsers.jobsdb_parser import jobsdb_parser
        from parsers.jobsugoi_parser import jobsugoi_parser
        from parsers.jobth_parser import jobth_parser
        from parsers.jobthai_parser import jobthai_parser
        from parsers.jobthaiweb_parser import jobthaiweb_parser
        from parsers.jobtopgun_parser import jobtopgun_parser
        from parsers.nationejobs_parser import nationejobs_parser
        from parsers.nationejob_parser import nationejob_parser
        from parsers.thaibestjobs_parser import thaibestjobs_parser
        from parsers.workventure_parser import workventure_parser
        from parsers.jobpub_parser import jobpub_parser   
        
        try: 
            parser_name = file_name.split("/")[-2]  #  website name indicated via folder name
        except:
            raise FilenameSplitError
    
        if(parser_name == "jobant"):
            return jobant_parser
        elif(parser_name == "jobbkk"):
            return jobbkk_parser
        elif(parser_name == "jobsawasdee"):
            return jobsawasdee_parser
        elif(parser_name == "jobsdb"):
            return jobsdb_parser
        elif(parser_name == "jobsugoi"):
            return jobsugoi_parser
        elif(parser_name == "jobth"):
            return jobth_parser
        elif(parser_name == "jobthai"):
            return jobthai_parser
        elif(parser_name == "jobthaiweb"):
            return jobthaiweb_parser
        elif(parser_name == "jobtopgun"):
            return jobtopgun_parser
        elif(parser_name == "nationejob"):
            return nationejob_parser
        elif(parser_name == "nationejobs"):
            return nationejobs_parser
        elif(parser_name == "thaibestjobs"):
            return thaibestjobs_parser
        elif(parser_name == "workventure"):
            return workventure_parser
        elif(parser_name == "jobpub"):
            return jobpub_parser
        
    #  Queue_Manager : One queue manager process will recursive read files into queue
    
    #  Job_worker : Each process will parse the document, then insert into database
    def process_job(self, queue, test=False):
#         from MongodbSearcher import MongodbSearcher
#         from ProvinceMiner.miner_script import ProvinceMiner
#         pm = ProvinceMiner()
#         ms = MongodbSearcher("mongodb://tdri:stafftdri@localhost:27017", 
#                      'Company_Search_Index', 
#                      'company_search_index')
        while(True):

            try:
                job = queue.get(block=True, timeout=5)
            except:
                break

            # log('parser_script', "[Worker] Parsing filename ({})".format(job))
            parser = self.find_parser(job)  #  find the parser for that filename

            try:
                parsed_data = parser(job)  #  parse using filename
                hash_company = hashlib.md5(parsed_data['company'].encode()).hexdigest()
                hash_title_th = hashlib.md5(parsed_data['title_th'].encode()).hexdigest()
                hash_description = hashlib.md5(parsed_data['description'].encode()).hexdigest()
                parsed_data['hash'] = hash_company + hash_title_th + hash_description
                parsed_data['mined'] = False
#                 industry_id = ms.search_industry_id(parsed_data['company'])
#                 if(industry_id is not None):
#                     parsed_data['industry_id'] = industry_id
#                 else:
#                     parsed_data['industry_id'] = 'undefined'
                
#                 province = pm.mine_province(parsed_data)
#                 if(province is not None):
#                     parsed_data['province'] = province
#                 else:
#                     parsed_data['province'] = 'undefined'
                
            except:
                # log('parser_script', "[Worker] Filename ({}) gives error".format(job))
                self.count_error += 1
            else:
                # log('parser_script', "[Worker] Inserting filename ({})".format(job))
                self.insert_into_db(parsed_data, job)

            
 
    def insert_into_db(self, parsed_data, job):
        try:
            self.cnx.insert_one(parsed_data)
            # log('parser_script', "[Inserted file ({}) is done]".format(job))
            self.count_success += 1
        except:
            # self.logger.warning("[Worker] Found duplicated file filename ({})".format(job))
            self.count_duplicate += 1
    
    def queue_manager_job(self, starting, queue):
        def list_all_files_into_queue(path_to_folder, queue):
            this_folder = os.listdir(path_to_folder)
            for file in this_folder:
                try: #  This is a folder, recursive case
                    list_all_files_into_queue(path_to_folder + "/" + file, queue)
                except: #  This is a file (base case)
                    queue.put(path_to_folder + "/" + file)  #  put full path into queue

        log('parser_script', "[QueueManager] Starting Queue Manager at folder ./{}/".format(starting))
        list_all_files_into_queue(starting, queue)
        
        self.queue_manager_is_done = True
        queue.close()  #  no more adding data
        self.cnx_INIT[self.DB_NAME_INIT][self.COLLECTION_NAME_INIT].update_one({'_id' :self.parsing_id }, {'$set' : {'parsed' : True, 'mined': False}})
        
        log('parser_script', {'message' : 'Parsed Success', 'success': self.count_success, 'duplicate': self.count_duplicate, 'error': self.count_error, 'time': datetime.datetime.now()})
        print("All jobs are inserted into queue")
        

        
    #  main function : run this cell to start parsing
    def main(self, num_process = 4):
        
        from multiprocessing import Queue, Process
        from pymongo import MongoClient
        from pymongo.errors import DuplicateKeyError

        #  Start queue manager
        queue = Queue(maxsize=10000)
        queueManager = Process(target=self.queue_manager_job, args=(self.init_file_name, queue))
        queueManager.start()

        #  Distribute jobs to workers
        processes = [Process(target=self.process_job, args=(queue, )) for i in range(num_process)]
        for process in processes:
            process.start()
           
        for procees in processes:
            process.join()
        




class ParserNotFoundError(Exception):
    pass

class FilenameSplitError(Exception):
    pass

class NotADirectoryError(Exception):
    pass
    
        
