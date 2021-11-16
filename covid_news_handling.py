from newsapi import NewsApiClient ##python3.9 -m install newsapi-python
import json , sched ,time
global news_articles
global removed_articles
global covidsched
covidsched = sched.scheduler(time.time, time.sleep)
removed_articles = []


def news_API_request(covid_terms="Covid COVID-19 coronavirus"):
    newsapi = NewsApiClient(api_key=open("apikey.txt").read())
    terms = covid_terms.split(" ")
    all_articles = []
    for term in terms:
        some_articles = newsapi.get_everything(q=term)["articles"]
        all_articles += some_articles
    return all_articles

news_articles=news_API_request()

def remove_article(title):
    removed_articles.append(title)
    for item in news_articles:
        for removed in removed_articles:
            if item["title"] == removed:
                news_articles.remove(item)
                
    


def update_news(*info):
    current_articles = news_API_request()
    for item in current_articles:
        for removed in removed_articles:
            if item == removed:
                current_articles.remove(item)
    news_articles= current_articles

def schedule_covidnews_updates(update_interval,update_name,repeat=False):
    covidsched.enter(update_interval,1,update_news)
    if repeat : covidsched.enter(update_interval,2,schedule_covidnews_updates,argument=(24*60*60,update_name,repeat))
    covidsched.run()
    
##schedule_covidnews_updates(100,"Test")
