from flask import Flask, render_template ,redirect,request

from covid_data_handler import *
from covid_news_handling import *

nation="england"





app = Flask(__name__)



@app.route("/index")
def index():
    update_covid_data()
    update_news()
    newCases = 0
    for x in range(0,7):
        newCases += covid_data[x]["newCasesByPublishDate"]
        
    nation_data = covid_API_request("england","nation")
    nationCases = 0
    for x in range(0,7):
        nationCases += nation_data[x]["newCasesByPublishDate"]
    
    print(request.args)
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
    return render_template("index.html",local_7day_infections=newCases,updates="",nation_location=nation_data[0]["areaName"],national_7day_infections=nationCases,title="Hello World!",location=covid_data[0]["areaName"],news_articles=news_articles,notification={'title':'Test'})


app.run(port=5002,debug=True)