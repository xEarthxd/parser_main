from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import get_file_name
### MongoDB Section ###
DB_NAME = 'test2'
COL_NAME = 'test2'

connection = MongoClient('mongodb://tdri:stafftdri@localhost:27017')
db = connection[DB_NAME][COL_NAME]

app = Flask(__name__)
api = Api(app)

file_name_temp = {}
## parser = reqparse.RequestParser()

class insertDB(Resource):
    def get(self):
        return file_name_temp

    def post(self):
        ##  args = parser.parse_args()
        test = 'Description'
        file_name_temp['First'] = test
        db.insert_one(file_name_temp)
        return {'Status':'Done'}

class extractor(Resource):
    def get(self, file_name):
        return get_file_name.download_file(file_name)

api.add_resource(insertDB, '/db_insert')
api.add_resource(extractor, '/extract/<file_name>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)