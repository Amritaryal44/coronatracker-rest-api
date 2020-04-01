import os

from flask import Flask, render_template, url_for
from flask_restful import Api
import threading
import atexit

from resource.details import *
from models.covidmodel import *

POOL_TIME = 180 #Seconds i.e 5 minutes

# lock to control access to variable
dataLock = threading.Lock()
# thread handler
scrapthread = threading.Thread()

def create_app():
    app = Flask(__name__)

    def interrupt():
        global scrapthread
        print("exit")
        scrapthread.cancel()

    def scrap():
        global scrapthread
        with dataLock:
        # threading job to be done here i.e. for updating database
            with app.app_context():
                update_database()
            print("Now waiting for next thread...")
        # Set the next thread to happen
        scrapthread = threading.Timer(POOL_TIME, scrap, ())
        scrapthread.start()   

    def scrapStart():
        # for initializing the thread
        global scrapthread
        # creating the thread
        scrapthread = threading.Timer(POOL_TIME, scrap, ())
        scrapthread.start()

    # Initiate
    scrapStart()
    # When Flask (SIGTERM) is killed, it clears the trigger for the next thread
    atexit.register(interrupt)
    return app

#app is created after starting the thread
app = create_app() 

api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# sqlalchemy operations
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET')

# initializing app for limiter (in detail.py)
limiter.init_app(app)

@app.errorhandler(404)
def ratelimit_handler(e):
    return {"message":"nothing here dude."}, 404


@app.route('/codes')
def codes():
    return render_template('codes.html', mydict = dict_code)

@app.route('/')
def index():
    return render_template('index.html')

api.add_resource(CountryCode, '/countrycode/<string:name>')
api.add_resource(Country, '/country/<string:name>')
api.add_resource(All, '/all')
api.add_resource(Updates, '/updates')
api.add_resource(CountryUpdates, '/updates/<string:name>')

if __name__=='__main__':
    app.run()
