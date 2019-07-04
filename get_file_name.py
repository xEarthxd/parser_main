from pymongo import MongoClient
from boto3.session import Session
import os
from parser_script import parsers
import subprocess

### S3 Bucket Connection ###

ACCESS_KEY_ID = 'AKIAJLKZSYZVQZ2I65SA'
SECRET_ACCESS_KEY = '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'
REGION_NAME = 'ap-southeast-1'

session = Session(
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)

s3 = session.resource('s3')
bucket = s3.Bucket('tdri-sea-html')

### MongoDB Connection ###

connection = MongoClient('mongodb://tdri:stafftdri@localhost:27017')
db = connection['test']['test']

### Download file from S3 to EC2 ###
def download_file(file_name):
    downloaded = os.listdir('../downloaded')

    if file_name in downloaded: 
        pass
    else:
        bucket.download_file(file_name, '../downloaded/' + file_name)
        extract_downloaded(file_name)

### Extracting ZIP ###
def extract_downloaded(file_name):
    parsed = os.listdir('./need_to_parse/')
    if file_name.split('.')[0] in parsed: 
        pass
    else:
        subprocess.run(['tar', '-xf', '../downloaded/'+file_name, '-C', 'need_to_parse/'])
#         !tar -xf ../downloaded/{file_name} -C need_to_parse/
#         print('file_name
    
        

    