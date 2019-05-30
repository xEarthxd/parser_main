#!/usr/bin/env python
# coding: utf-8

from pymongo import MongoClient
from boto3.session import Session
import os
from parser_script import parsers
import subprocess
from modules.Logger import log
import requests


def download_file(bucket, file_name):
    '''Download file from S3 to local EC2'''
    try:
        downloaded = os.listdir('./downloaded')
    except:
        os.mkdir('downloaded')
        downloaded = os.listdir('./downloaded')

    if file_name in downloaded:
        log('main_parser', 'File is downloaded earlier')
        pass
    else:  # Download file from S3
        log('main_parser', 'Downloading file from S3')
        bucket.download_file(file_name, 'downloaded/' + file_name)
        log('main_parser', 'Donwloaded {} DONE'.format(file_name))
        extract_downloaded(file_name)  # Extract tar.gz
        log('main_parser', 'Extracted {} DONE'.format(file_name))
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
        subprocess.run(["tar", "-xf", './downloaded/' +
                        file_name, '-C', 'need_to_parse/'])

def main():
    from pymongo import MongoClient
    from modules.Configuration import getConfig

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
    # bucket = s3.Bucket('sea-html')
    bucket = s3.Bucket('earthlambda')

    file_name = con.find_one({'parsed': False})['file_name']
    log('main_parser', {"message": 'New file is found', "filename": file_name})

    download_file(bucket, file_name)
    requests.get(
        'https://1rymu04g2k.execute-api.ap-southeast-1.amazonaws.com/default/lambda2')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log('main_parser', {"error": str(e)})