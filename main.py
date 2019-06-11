import os
import shutil
import subprocess

import requests
from boto3.session import Session
from pymongo import MongoClient

from modules.Logger import log
from parser_script import Parsers
from modules.Configuration import getConfig


def download_file(bucket, file_name):
    '''Download file from S3 to local EC2'''
    try:
        downloaded = os.listdir('./downloaded')
    except:
        os.mkdir('downloaded')
        downloaded = os.listdir('./downloaded')

    if file_name in downloaded:
        log('main_parser', 'File is downloaded earlier')
    else:  # Download file from S3
        log('main_parser', 'Downloading file from S3')
        bucket.download_file(file_name, 'downloaded/' + file_name)
        log('main_parser', 'Donwloaded {} DONE'.format(file_name))
        
        extract_downloaded(file_name)  # Extract tar.gz
        log('main_parser', 'Extracted {} DONE'.format(file_name))

        parser = Parsers()
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
        subprocess.run(["tar", "-xf", './downloaded/' + file_name,
                        '-C', 'need_to_parse/'])  # This line is blocking


def main():
    log('main_parser', 'Parser is started')

    config = getConfig()['PARSER_MAIN_S3_CONNECTION']
    DB_NAME_INIT = config['databasename']
    COLLECTION_NAME_INIT = config['collectionname']
    ACCESS_KEY_ID = config['ACCESS_KEY_ID']
    SECRET_ACCESS_KEY = config['SECRET_ACCESS_KEY']
    REGION_NAME = config['REGION_NAME']

    con = MongoClient("mongodb://{}:{}@{}:27017".format(
        config['username'], config['password'], config['databaseaddress']))[DB_NAME_INIT][COLLECTION_NAME_INIT]

    session = Session(
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        region_name=REGION_NAME
    )

    s3 = session.resource('s3')
    bucket = s3.Bucket('tdri-pipeline-testing')

    for record in con.find({'parsed': False}):
        file_name = record['file_name']

        log('main_parser', {
            "message": 'New file is found', "filename": file_name})
        download_file(bucket, file_name)

        log('main_parser', {
            "message": 'firing event to lambda2', "filename": file_name})
        requests.get(
            'https://g6llzc4s2b.execute-api.ap-southeast-1.amazonaws.com/default/lambda2')

        shutil.rmtree("./download", ignore_errors=False, onerror=None)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log('main_parser', {"error": str(e)})
        raise e
