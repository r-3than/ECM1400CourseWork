from flask import Flask, render_template,request
import datetime  ,json
from covid_data_handler import *
from covid_news_handling import *
from schedHandler import schedHandler
global updates

global nation


### Follow the google style doc strings

nation=json.loads(open("config.json").read())["nation"]

update_covid_data()
update_news()

updates = []

newsHandler = schedHandler(newssched)
covidHandler = schedHandler(covidsched)

app = Flask(__name__)



@app.route("/index")
def index():
    """
    This is the main function that handles
    the flask connection between the api and the client.

    Returns:
        A rendered template hosted at localhost:5002/index

    """
    newCases = 0
    for x in range(0,7):
        newCases += covid_data[x]["newCasesByPublishDate"]
        
    nation_data = covid_API_request(nation,"nation")
    nationCases = 0
    for x in range(0,7):
        nationCases += nation_data[x]["newCasesByPublishDate"]
    
    #print(request.args) http://127.0.0.1:5002/index?alarm=12%3A03&two=124&repeat=repeat&covid-data=covid-data&news=news
    if "notif" in request.args:
        remove_article(request.args["notif"])
    if "update" in request.args and "two" in request.args:
        content = ""
        currentTime = datetime.datetime.now()
        alarmTime = request.args["update"].split(":")
        wantedTime = currentTime.replace(hour=int(alarmTime[0]),minute=int(alarmTime[1]))
        
        if wantedTime < currentTime:
            wantedTime.replace(day=wantedTime.day+1)

        secondsUntilUpdate = (wantedTime - currentTime).total_seconds()
        #title = request.args["two"]
        
        
        repeating = False
        if "repeat" in request.args:
            content = "repeating "
            repeating = True
        if "news" in request.args:
            newscontent = content + "update at " + request.args["update"] + " for news."
            newscontent = list(newscontent)
            newscontent[0] = newscontent[0].upper()
            newscontent = ''.join(newscontent)
            title = "News Data Update:"+request.args["two"]+ " "
            events = newsHandler.events
            no_doubles = False
            while no_doubles == False:
                no_doubles = True
                for item in events:
                    eventTitle = item["title"]
                    if title == eventTitle:
                        title += "I"
                        no_doubles = False
            newsHandler.addEvent(update_news,secondsUntilUpdate,title,newscontent,repeat=repeating)
        if "covid-data" in request.args:
            
            datacontent = content + "update at " + request.args["update"] + " for covid data."
            datacontent = list(datacontent)
            datacontent[0] = datacontent[0].upper()
            datacontent = ''.join(datacontent)
            title = "Covid Data Update:"+request.args["two"]+ " "
            events = covidHandler.events
            no_doubles = False
            while no_doubles == False:
                no_doubles = True
                for item in events:
                    eventTitle = item["title"]
                    if title == eventTitle:
                        title += "I"
                        no_doubles = False
            covidHandler.addEvent(update_news,secondsUntilUpdate,title,datacontent,repeat=repeating)

    if "update_item" in request.args:

        updates = covidHandler.getEvents()
        for item in updates:
            if item["title"] == request.args["update_item"]:
                queueEvents = item["events"]
                for e in queueEvents:
                    covidHandler.removeEvent(e)

        updates = newsHandler.getEvents()
        for item in updates:
            if item["title"] == request.args["update_item"]:
                queueEvents = item["events"]
                for e in queueEvents:
                    newsHandler.removeEvent(e)
                

        

    #last7DaysInfections = int(covid_data[2]["cumCasesByPublishDate"]) - int(covid_data[8]["cumCasesByPublishDate"])
    ## Var decomp
    ## updates
    ## title
    ## location
    ## local_7day_infections
    ## national_7day_infections
    ## nation_location
    ## hospital_cases
    ## deaths_total
    ## news_articles
    ## notification
    ## favicon
    ## image
    updates = []
    updates += covidHandler.getEvents()
    updates += newsHandler.getEvents()

    return render_template(
    "index.html",
    updates=updates,
    deaths_total=nation_data[1]["cumDeaths28DaysByDeathDate"],
    local_7day_infections=newCases,nation_location=nation_data[0]["areaName"],
    national_7day_infections=nationCases,title="Hello World!",
    location=covid_data[0]["areaName"],
    news_articles=news_articles,
    image="covidimage.jpg",
    hospital_cases=get_hospital_cases())

if __name__ == "__main__":
    app.run(port=5002,debug=True)