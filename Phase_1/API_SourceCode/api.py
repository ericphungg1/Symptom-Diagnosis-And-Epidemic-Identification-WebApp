from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from flask_restx import Api, Resource, reqparse
  
cluster = "mongodb+srv://thumbnails:thumbnails@cluster0.lfkm3.mongodb.net/SENG3011?retryWrites=true&w=majority"
app = Flask(__name__)
client = MongoClient(cluster)

api = Api(app)

db = client.SENG3011

collection = db.SENG3011_collection

#RETRUNS ALL REPORTS IN DATABASE 
@api.route('/find', methods=['GET'])
class MainClass(Resource):
    def get(value):
        query = collection.find({})
        output = {}
        i = 0 
        for x in query:
            output[i] = x
            output[i].pop('_id')
            i+=1
        return jsonify(output)

#THIS ONE FINDS ANY MATCHES IN SPECIFIED FIELD 
@api.route('/find/<argument>/<value>/', methods=['GET'])
class MainClass(Resource):
    def get(argument, value):
        queryObject = {argument: value}
        query = collection.find(queryObject)
        output = {}
        i = 0
        for x in query:
            output[i] = x
            output[i].pop('_id')
            i+=1
        return jsonify(output)

#RETURNS REPORTS MATCHING DISEASE GIVEN 
@api.route('/find/disease/<value>', methods=['GET'])
class MainClass(Resource):
    def get(argument, value):
        query = collection.find( {"reports.diseases.0": value } )
        output = {}
        i = 0
        for x in query:
            output[i] = x
            output[i].pop('_id')
            i+=1
        return jsonify(output)

#RETURNS REPORTS MATCHING KEY TERMS
@api.route('/find/keyterms/<value>/', methods=['GET'])
class MainClass(Resource):
    def get(argument, value):
        query = collection.find( {"reports.diseases.0": value } ) # HOW DO I GET KEY TERMS 
        output = {}
        i = 0
        for x in query:
            output[i] = x
            output[i].pop('_id')
            i+=1
        return jsonify(output)

#RETURNS REPORTS MATCHING LOCATION
@api.route('/find/location/<value>/', methods=['GET'])
class MainClass(Resource):
    def get(argument, value):
        query = collection.find( {"reports.locations.0": value } )
        output = {}
        i = 0
        for x in query:
            output[i] = x
            output[i].pop('_id')
            i+=1
        return jsonify(output)

#RETURNS REPORTS MATCHING START AND END DATE
@api.route('/find/date/<value>/', methods=['GET'])
class MainClass(Resource):
    def get(argument, value):
        query = collection.find( {"reports.event_date.0": value } )
        output = {}
        i = 0
        for x in query:
            output[i] = x
            output[i].pop('_id')
            i+=1
        return jsonify(output)

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0')
