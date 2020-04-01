from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Worldometer(db.Model):
    __tablename__ = "worldometer"
    id = db.Column(db.Integer, primary_key = True)
    countrycode = db.Column(db.String(100), unique=True, nullable=False)
    totalcase = db.Column(db.String)
    newcase = db.Column(db.String)
    totaldeath = db.Column(db.String)
    newdeath = db.Column(db.String)
    totalrecovered = db.Column(db.String)
    critical = db.Column(db.String)
    lastupdated = db.Column(db.String)

    def __init__(self, countrycode, totalcase, newcase, totaldeath, newdeath, totalrecovered, critical, lastupdated):
        self.countrycode = countrycode
        self.totalcase = totalcase
        self.newcase = newcase
        self.totaldeath = totaldeath
        self.newdeath = newdeath
        self.totalrecovered = totalrecovered
        self.critical = critical
        self.lastupdated = lastupdated
    

