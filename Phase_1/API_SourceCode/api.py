from sqlite3 import DateFromTicks
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from pymongo import MongoClient
from flask_restx import Api, Resource, reqparse
import time
import datetime
import re
  
cluster = "mongodb+srv://thumbnails:thumbnails@cluster0.lfkm3.mongodb.net/SENG3011?retryWrites=true&w=majority"
app = Flask(__name__)
client = MongoClient(cluster)

api = Api(app)

db = client.SENG3011

collection = db.SENG3011_collection

# timestamp when end user access endpoints
timeStamp = time.time()
date = datetime.datetime.fromtimestamp(timeStamp).strftime("%Y-%m-%d %H:%M:%S")

logSnippet = {
    'team_name': 'Thumbnails',
    'access_time': date,
    'data_source': 'CDC Current Outbreak List'
}

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
        timeStamp = time.time()
        logSnippet['access_time'] = date = datetime.datetime.fromtimestamp(timeStamp).strftime("%Y-%m-%d %H:%M:%S")
        response = {'data': output, 'log': logSnippet}
        return jsonify(response)

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
        timeStamp = time.time()
        logSnippet['access_time'] = date = datetime.datetime.fromtimestamp(timeStamp).strftime("%Y-%m-%d %H:%M:%S")
        response = {'data': output, 'log': logSnippet}
        return jsonify(response)

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
        timeStamp = time.time()
        logSnippet['access_time'] = date = datetime.datetime.fromtimestamp(timeStamp).strftime("%Y-%m-%d %H:%M:%S")
        response = {'data': output, 'log': logSnippet}
        return jsonify(response)

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
        timeStamp = time.time()
        logSnippet['access_time'] = date = datetime.datetime.fromtimestamp(timeStamp).strftime("%Y-%m-%d %H:%M:%S")
        response = {'data': output, 'log': logSnippet}
        return jsonify(response)

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
        timeStamp = time.time()
        logSnippet['access_time'] = date = datetime.datetime.fromtimestamp(timeStamp).strftime("%Y-%m-%d %H:%M:%S")
        response = {'data': output, 'log': logSnippet}
        return jsonify(response)

#RETURNS REPORTS MATCHING START AND END DATE
@api.route('/find/date/<value>/', methods=['GET'])
class MainClass(Resource):
    def get(argument, value):        
        dates = value.split("&")

        # Checks if dates are seperated by an &
        if (len(dates) != 2):
            return make_response(jsonify("ERROR: Please enter dates seperated by a '&'"),400)
        
        # Checks if dates are of format: YYYY-MM-DDTHH:mm:ss
        for date in dates:
            if not dateFormatCheck(date):
                return make_response(jsonify("ERROR: Please enter dates in correct format: “yyyy-MM-ddTHH:mm:ss”"),400)
            
            if not dateFutureCheck(date):
                return make_response(jsonify("ERROR: Please enter in valid start and end dates. Dates cannot be future dates."),400)
              
        d1 = dateFormatCheck(dates[0])
        d2 = dateFormatCheck(dates[1])

        if not dateOrderCheck(d1,d2):
            return make_response(jsonify("ERROR: Please enter valid start and end dates. Start date must not be after end date"),400)


        query = collection.find({})
        output = {}
        i = 0
        for x in query:
            date = x.pop('date_of_publication')
            if checkDateRange(date, d1,d2):
                output[i] = x
                output[i].pop('_id')
                i+=1
        timeStamp = time.time()
        logSnippet['access_time'] = date = datetime.datetime.fromtimestamp(timeStamp).strftime("%Y-%m-%d %H:%M:%S")
        response = {'data': output, 'log': logSnippet}
        return jsonify(response)

def dateFormatCheck(date):
    try:
        dateObject = datetime.datetime.strptime(date,'%Y-%m-%dT%H:%M:%S')
    except:
        return False
    return dateObject
        
def dateOrderCheck(d1,d2):
    print(d1,d2,d1<d2)
    if (d1 >= d2):
        return False
    return True

def dateFutureCheck(date):
    d1 = dateFormatCheck(date)
    if d1 > datetime.datetime.now():
        return False
    return True

def checkDateRange(date,d1,d2):
    temp_date = re.sub(r"[: ]","-",date)
    temp_date = re.sub(r"x","",temp_date)
    temp_date = re.sub(r"(--)","",temp_date)
    temp_date = re.sub(r"-$","",temp_date)
    elements = temp_date.split("-")
    if (len(elements) == 3):
        d3 = datetime.datetime.strptime(temp_date,'%Y-%m-%d')
    elif (len(elements) == 5):
        d3 = datetime.datetime.strptime(temp_date,'%Y-%m-%d-%H-%M')
    else:
        return False
    
    if not ((d1 <= d3) and (d3 <= d2)):
       return False
    
    return True

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

        
if __name__ == '__main__':
    app.run(host='0.0.0.0')
