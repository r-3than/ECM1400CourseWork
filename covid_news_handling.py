from newsapi import NewsApiClient ##python3.9 -m install newsapi-python
import json
## API KEY = 83888054770e425ab871a38966d67404
def news_API_request(covid_terms="Covid COVID-19 coronavirus"):
    newsapi = NewsApiClient(api_key='83888054770e425ab871a38966d67404')
    terms = covid_terms.split(" ")
    all_articles = []
    for term in terms:
        some_articles = newsapi.get_everything(q=term)["articles"]
        all_articles += some_articles
    return all_articles
    

news_API_request()