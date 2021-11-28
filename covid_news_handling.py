"""

This module covid_news_handling handles news updates.
It serves to:
    Request fresh news data.
    Remove articles
    Schedule news updates. 

"""

from newsapi import NewsApiClient ##python3.9 -m install newsapi-python
import json , sched ,time , logging
global news_articles
global removed_articles
global covidsched
covidsched = sched.scheduler(time.time, time.sleep)
removed_articles = []


def news_API_request(covid_terms=json.loads(open("config.json").read())["news_terms"]):
    """news_API_request function

    This function takes in covid_terms and returns a list of dictionaries of news articles with those terms.

    Args:
        covid_terms (string): A string with terms seperated by a white space to search for news articles for.

    Returns:
        list: Returns a list of news articles.
        e.g [{article1},{article2},{article3},... etc ]

    """
    try:
        logging.info("Trying to fetch data with apikey")
        newsapi = NewsApiClient(api_key=open("apikey.txt").read())
    
        terms = covid_terms.split(" ")
        all_articles = []
        for term in terms:
            some_articles = newsapi.get_everything(q=term)["articles"]
            all_articles += some_articles
        return all_articles
    except:
        logging.warning("INVAILD API KEY PLEASE CHANGE IN apikey.txt")
        return []

news_articles=news_API_request()

def remove_article(title):
    """remove_article function

    This function takes in a title of an article and removes it form the current list of shown articles.
    It will also save the title of the article to an array so in future updates they will not show

    Args:
        title (string) : The title of an article.

    Returns:
        None
    """
    logging.info("Removing article -" + title + "-.")
    removed_articles.append(title)
    for item in news_articles:
        for removed in removed_articles:
            if item["title"] == removed:
                news_articles.remove(item)
                
    


def update_news(covid_terms=json.loads(open("config.json").read())["news_terms"]):
    """update_news function

    This function takes in covid_terms and fetches an updated news
    and removes any unwanted articles from the list removed_articles and will
    set global var news_articles to these fetched articles.

    Args:
        None

    Returns:
        None: However global var news_articles is updated.


    """
    logging.info("Updating articles")
    current_articles = news_API_request(covid_terms=covid_terms)
    for item in current_articles:
        for removed in removed_articles:
            if item == removed:
                current_articles.remove(item)
    news_articles= current_articles

def schedule_covidnews_updates(update_interval,update_name,repeat=False):
    """schedule_covidnews_updates function

    This function is a secheduler function which serves add an update to news on a scheduler.

    Args:
        update_interval (int): Number of seconds until and updates should be processed. 
        update_name (string): The name of the scheduler to help identify them
        repeat (bool): A default bool of False set to true to schedule an update at this time every day.

    Returns:
        None

    """
    logging.info("News will be updated in "+update_interval+" seconds.")
    covidsched.enter(update_interval,1,update_news)
    if repeat : covidsched.enter(update_interval,2,schedule_covidnews_updates,argument=(24*60*60,update_name,repeat))
    covidsched.run()
    
##schedule_covidnews_updates(100,"Test")
