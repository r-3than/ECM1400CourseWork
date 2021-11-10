from uk_covid19 import Cov19API ## python3.9 -m pip install uk-covid19
import json
import sched, time

global covid_data
global newssched
newssched = sched.scheduler(time.time, time.sleep)

def parse_csv_data(csv_filename):
    f = open(csv_filename).read().split("\n") ## open and process file by line
    f.pop(-1) ## Remove Blank line
    return f

def process_covid_csv_data(covid_csv_data):
    last7days_cases = 0 ## Thecases in the last 7 days should be calculated by summing the new cases by specemin date forthe last 7 days ignoring the first entry as the data is incomplete for that day
    current_hospital_cases = int(covid_csv_data[1].split(",")[5]) ##top row of current cases.
    total_deaths = 0
    specimanDataLn = None
    for x in range(1,len(covid_csv_data)-1): ## for general case of finding location of speciman date
        splitByCommaData = covid_csv_data[x].split(",")
        if splitByCommaData[6].isnumeric() and specimanDataLn == None: ## index 6 is where speciman data is kept & is numeric checks for number input
            specimanDataLn = x+1 ## start counting from next line
        if splitByCommaData[4].isnumeric() and total_deaths == 0:
            total_deaths = int(splitByCommaData[4])
        if specimanDataLn != None and total_deaths != 0: break
        
    for x in range(specimanDataLn,specimanDataLn+7):
        splitByCommaData = covid_csv_data[x].split(",")
        last7days_cases += int(splitByCommaData[6])
    return (last7days_cases , current_hospital_cases, total_deaths)

def covid_API_request(location="Exeter",location_type="ltla"):

    
    filt = ['areaType='+location_type,'areaName='+location]

    struc = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "newCasesByPublishDate": "newCasesByPublishDate",
    "cumCasesByPublishDate": "cumCasesByPublishDate",
    "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
    "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate"
    }

    api = Cov19API(filters=filt,structure=struc)
    data = api.get_json()["data"][0:30]
    return data

covid_data = covid_API_request()

def update_covid_data():
    covid_data = covid_API_request()
##covid_API_request()

def schedule_covid_updates(update_interval,update_name,repeat=False):
    newssched.enter(update_interval,1,covid_API_request)
    if repeat : newssched.enter(update_interval,2,lambda : schedule_covid_updates(update_interval=24*60*60,update_name=update_name,repeat=repeat))
    newssched.run()

##schedule_covid_updates(10,"test")
