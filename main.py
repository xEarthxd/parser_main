#!/usr/bin/env python
# coding: utf-8

from pymongo import MongoClient
from boto3.session import Session
import os
from parser_script import parsers
import subprocess

def download_file(file_name):
    '''Download file from S3 to local EC2'''
    try:
        downloaded = os.listdir('./downloaded')
    except:
        os.mkdir('download')
        downloaded = os.listdir('./downloaded')

    if file_name in downloaded: 
        pass
    else:  #  Download file from S3
        bucket.download_file(file_name, 'downloaded/' + file_name)
        extract_downloaded(file_name) #  Extract tar.gz
        file_name_parse = file_name.split('.')[0]
        parser = parsers()
        parser.main()
        
def extract_downloaded(file_name):
    '''Extract downloaded file'''
    try:
        parsed = os.listdir('./need_to_parse')
    except:
        os.mkdir('need_to_parse')
        parsed = os.listdir('./need_to_parse')

    if file_name.split('.')[0] in parsed: 
        pass
    else:
#         !tar -xf ../downloaded/{file_name} -C need_to_parse/

        subprocess.run(["tar", "-xf", './downloaded/'+file_name, '-C', 'need_to_parse/'])
    
if __name__ == '__main__':
    ACCESS_KEY_ID = 'AKIAJLKZSYZVQZ2I65SA'
    SECRET_ACCESS_KEY = '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'
    REGION_NAME = 'ap-southeast-1'
    
    session = Session(
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        region_name=REGION_NAME
    )
    
    s3 = session.resource('s3')
    # bucket = s3.Bucket('sea-html')
    bucket = s3.Bucket('earthlambda')
    
    ## Suppose file name is acquired and store in file_name variable ##
    file_name = parsers().get_file_name()
    
    download_file(file_name)
    print(True)

