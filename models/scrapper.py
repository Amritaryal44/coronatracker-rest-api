from bs4 import BeautifulSoup
import requests
import datetime

# for mapping into country codes 
from models.codes import dict_code

# for database works
from models.covidmodel import *

def scrap_worldometer():
    html_doc = requests.get("https://www.worldometers.info/coronavirus/").text
    soup = BeautifulSoup(html_doc, 'html.parser')

    # table containing data
    table = soup.find(id='main_table_countries_today')

    # maping headings in our database format i.e. dictionary keys
    dict_headers = ["totalcase", "newcase", "totaldeath", "newdeath", "totalrecovered", "critical"]

    # all data
    countries = []
    Data = table("tr")[1:]
    for dat in Data:
        td = dat("td")[:8]
        info = list(map(lambda tag: tag.text, td))
        info.pop(6)
        country = info.pop(0)
        if country in dict_code:
            code = dict_code[country]
        else:
            ## what to do when new country comes
            code = country+"[new]"
        info_dict = {dict_headers[i]:x for x, i in zip(info, range(len(info)))}
        info_dict["countrycode"] = code
        my_date = datetime.datetime.now()
        info_dict["lastupdated"] = my_date.isoformat()
        countries.append(info_dict)
    return countries

def update_database():
    countries = scrap_worldometer()
    i = 0
    for country in countries:
        i += 1
        country_db = Worldometer.query.filter_by(countrycode=country["countrycode"]).first()
        if country_db:
                # COUNTRY IN DATABASE AND NEW DATA HAS ARRIVED
                updater(country_db, country)
        else:
            # -- COUNTRY NOT IN DATABASE
            new_db = Worldometer(**country)
            db.session.add(new_db)
            db.session.commit()
        print(str(len(countries)-i)+" remaining")

def updater(old_db, country):
    if old_db.countrycode != country["countrycode"] or old_db.totalcase != country["totalcase"] or old_db.newcase != country["newcase"] or old_db.totaldeath != country["totaldeath"] or old_db.newdeath != country["newdeath"] or old_db.totalrecovered != country["totalrecovered"] or old_db.critical != country["critical"] or old_db.lastupdated != country["lastupdated"]:
        old_db.countrycode = country["countrycode"]
        old_db.totalcase = country["totalcase"]
        old_db.newcase = country["newcase"]
        old_db.totaldeath = country["totaldeath"]
        old_db.newdeath = country["newdeath"]
        old_db.totalrecovered = country["totalrecovered"]
        old_db.critical = country["critical"]
        old_db.lastupdated = country["lastupdated"]
        db.session.commit()