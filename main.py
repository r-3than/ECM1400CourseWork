"""

This module main.py handles the flask connection and serves the webpage to the user.
It serves to:
    Handle displaying data to the user.
    Handle removing news articles.
    Handle adding updates to data or news.
    Handle removing unwanted updates.

"""

import json
import datetime

from werkzeug.utils import redirect
from schedHandler import schedHandler
from covid_news_handling import *
from covid_data_handler import *
from flask import Flask, render_template, request , Markup
import logging
logging.basicConfig(
    filename='out.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')


logging.info('Imports successfully imported with no errors.')

global updates
global nation


# Follow the google style doc strings

nation = json.loads(open("config.json").read())["nation"]

update_covid_data()
update_news()

updates = []

newsHandler = schedHandler(newssched)
covidHandler = schedHandler(covidsched)

app = Flask(__name__)


@app.route("/index")
def index():
    """Main function

    This is the main function that handles
    the flask connection between the api and the client.
    It uses the imported modules to serve the data to the user
    in a nice GUI.

    Returns:
        A rendered template hosted at localhost:5002/index

    """
    logging.info("localhost:5002/index has been requested")
    newCases = 0
    for x in range(0, 7):
        newCases += covid_data[x]["newCasesByPublishDate"]

    nation_data = covid_API_request(nation, "nation")["covidData"]
    nationCases = 0
    for x in range(0, 7):
        nationCases += nation_data[x]["newCasesByPublishDate"]

    # print(request.args)
    # http://127.0.0.1:5002/index?alarm=12%3A03&two=124&repeat=repeat&covid-data=covid-data&news=news
    if "notif" in request.args:
        remove_article(request.args["notif"])
    if "update" in request.args and "two" in request.args:
        content = ""
        currentTime = datetime.datetime.now()
        alarmTime = request.args["update"].split(":")
        wantedTime = currentTime.replace(
            hour=int(
                alarmTime[0]), minute=int(
                alarmTime[1]), second=0)

        if wantedTime < currentTime:
            wantedTime.replace(day=wantedTime.day + 1)

        secondsUntilUpdate = (wantedTime - currentTime).total_seconds()
        #title = request.args["two"]

        repeating = False
        if "repeat" in request.args:
            content = "repeating "
            repeating = True
        if "news" in request.args:
            newscontent = content + "update at " + \
                request.args["update"] + " for news."
            newscontent = list(newscontent)
            newscontent[0] = newscontent[0].upper()
            newscontent = ''.join(newscontent)
            title = "News Data Update:" + request.args["two"] + " "
            events = newsHandler.events
            no_doubles = False
            while no_doubles == False:
                no_doubles = True
                for item in events:
                    eventTitle = item["title"]
                    if title == eventTitle:
                        title += "I"
                        no_doubles = False
            newsHandler.addEvent(
                update_news,
                secondsUntilUpdate,
                title,
                newscontent,
                repeat=repeating)
        if "covid-data" in request.args:

            datacontent = content + "update at " + \
                request.args["update"] + " for covid data."
            datacontent = list(datacontent)
            datacontent[0] = datacontent[0].upper()
            datacontent = ''.join(datacontent)
            title = "Covid Data Update:" + request.args["two"] + " "
            events = covidHandler.events
            no_doubles = False
            while no_doubles == False:
                no_doubles = True
                for item in events:
                    eventTitle = item["title"]
                    if title == eventTitle:
                        title += "I"
                        no_doubles = False
            covidHandler.addEvent(
                update_news,
                secondsUntilUpdate,
                title,
                datacontent,
                repeat=repeating)

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
    # Var decomp
    # updates
    # title
    # location
    # local_7day_infections
    # national_7day_infections
    # nation_location
    # hospital_cases
    # deaths_total
    # news_articles
    # notification
    # favicon
    # image
    updates = []
    updates += covidHandler.getEvents()
    updates += newsHandler.getEvents()

    deaths_total = "Total deaths in " +json.loads(open("config.json").read())["nation"].title() + ": "+ str(nation_data[1]["cumDeaths28DaysByDeathDate"])
    hospital_cases = "Total hospital cases in " +json.loads(open("config.json").read())["nation"].title() + ": "+ str(get_hospital_cases())
    return render_template(
        "index.html",
        updates=updates,
        deaths_total=deaths_total,
        local_7day_infections=newCases, nation_location=nation_data[0]["areaName"],
        national_7day_infections=nationCases, title="Covid Dashboard.",
        location=covid_data[0]["areaName"],
        news_articles=news_articles[0:5],  # limited to 6 items
        image="covidimage.jpg",
        hospital_cases=hospital_cases)




if __name__ == "__main__":
    app.run(port=5000, debug=True)
