from flask import Flask, render_template ,redirect,request
import datetime , threading
from covid_data_handler import *
from covid_news_handling import *
global updates
nation="england"

update_covid_data()
update_news()

updates = []

app = Flask(__name__)



@app.route("/index")
def index():
    newCases = 0
    for x in range(0,7):
        newCases += covid_data[x]["newCasesByPublishDate"]
        
    nation_data = covid_API_request("england","nation")
    nationCases = 0
    for x in range(0,7):
        nationCases += nation_data[x]["newCasesByPublishDate"]
    
    #print(request.args) http://127.0.0.1:5002/index?alarm=12%3A03&two=124&repeat=repeat&covid-data=covid-data&news=news
    if "notif" in request.args:
        remove_article(request.args["notif"])
    if "alarm" in request.args and "two" in request.args:
        content = ""
        currentTime = datetime.datetime.now()
        alarmTime = request.args["alarm"].split(":")
        wantedTime = currentTime.replace(hour=int(alarmTime[0]),minute=int(alarmTime[1]))
        repeating = False
        if wantedTime < currentTime:
            wantedTime.replace(day=wantedTime.day+1)

        secondsUntilUpdate = (wantedTime - currentTime).total_seconds()
        title = request.args["two"]
        newsupdater = threading.Thread(target= lambda : schedule_covidnews_updates(secondsUntilUpdate,title,repeat=repeating) )
        dataupdater = threading.Thread(target= lambda : schedule_covid_updates(secondsUntilUpdate,title,repeat=repeating))

        if "repeat" in request.args:
            content = "Repeating "
            repeating = True
        if "news" in request.args and "covid-data" in request.args:
            content += "update at " + request.args["alarm"] + " for news and covid data."
            newsupdater.start()
            dataupdater.start()
        elif "news" in request.args:
            content += "update at " + request.args["alarm"] + " for news."
            newsupdater.start()
        elif "covid-data" in request.args:
            content += "update at " + request.args["alarm"] + " for covid data."
            dataupdater.start()
        else:
            content += "update at " + request.args["alarm"] + " for yourself!"

            

        update = {"title":request.args["two"],"content":content}
        updates.append(update)

    if "alarm_item" in request.args:
        for item in updates:
            if item["title"] == request.args["alarm_item"]:
                updates.remove(item)
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
    ##notification
    return render_template("index.html",updates=updates,local_7day_infections=newCases,nation_location=nation_data[0]["areaName"],national_7day_infections=nationCases,title="Hello World!",location=covid_data[0]["areaName"],news_articles=news_articles,notification={'title':'Test'})


app.run(port=5002,debug=True)