from flask_restful import Resource, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models.codes import dict_code, get_key
from models.covidmodel import *
from models.scrapper import update_database

# instantiate limiter object
limiter = Limiter(
    key_func=get_remote_address,
)

# print the data in json format
def data_template(data, forUpdate=False): 
    country = ""
    if get_key(data.countrycode):
        country = get_key(data.countrycode)
    else:
        country = data.countrycode[:-5]
    
    if forUpdate:
        return {
            "countrycode":data.countrycode,
            "country":country,
            "lastupdated":data.lastupdated,
            "data":{
                    "newcase":data.newcase,                 
                    "newdeath":data.newdeath 
                }
            }
    else:
        return {
            "countrycode":data.countrycode,
            "country":country,
            "lastupdated":data.lastupdated,
            "data":{
                "totalcase":data.totalcase, 
                "newcase":data.newcase,
                "totaldeath":data.totaldeath, 
                "newdeath":data.newdeath, 
                "totalrecovered":data.totalrecovered, 
                "critical":data.critical
            }
        }    

# /countrycode/<string:name>/
class CountryCode(Resource):
    decorators=[limiter.limit("10 per minute;1 per second;600 per hour", error_message="chill!! dude. slow down")]
    def get(self, name): 
        # search country code if available
        data = Worldometer.query.filter_by(countrycode=name).first()
        if data:
            return data_template(data), 200
        return {"message":"Data not found"}, 404

# /country/<string:name>/
class Country(Resource):
    decorators=[limiter.limit("10 per minute;1 per second;600 per hour", error_message="chill!! dude. slow down")]
    def get(self, name): 
        # search country if available
        if name in dict_code:
            ccode = dict_code[name]
            data = Worldometer.query.filter_by(countrycode=ccode).first()
            if data:
                return data_template(data), 200
        return {"message":"Data not found"}, 404

# /all/
class All(Resource):
    # list of all data
    decorators=[limiter.limit("10 per minute;1 per second;600 per hour", error_message="chill!! dude. slow down")]
    def get(self): 
        result = Worldometer.query.all()
        if result:
            listData = []
            for data in result:
                listData.append(data_template(data))
            return {'data': listData}, 200
        return {"message":"Data not found"}, 404

# /updates/
class Updates(Resource):
    decorators=[limiter.limit("10 per minute;1 per second;600 per hour", error_message="chill!! dude. slow down")]
    def get(self):
        result = Worldometer.query.all()
        if result:
            listData = []
            for data in result:
                listData.append(data_template(data, forUpdate=True))
            return {'data': listData}, 200
        return {'message':"Data not found"}, 404

# /update/<string:name>
class CountryUpdates(Resource):
    decorators=[limiter.limit("10 per minute;1 per second;600 per hour", error_message="chill!! dude. slow down")]
    def get(self, name): 
        # search country code if available
        data = Worldometer.query.filter_by(countrycode=name).first()
        if data:
            return data_template(data, forUpdate=True), 200
        return {"message":"Data not found"}, 404

# /update/<string:name>
class CountryUpdates(Resource):
    decorators=[limiter.limit("10 per minute;1 per second;600 per hour", error_message="chill!! dude. slow down")]
    def get(self, name): 
        # search country code if available
        data = Worldometer.query.filter_by(countrycode=name).first()
        if data:
            return data_template(data, forUpdate=True), 200
        return {"message":"Data not found"}, 404
