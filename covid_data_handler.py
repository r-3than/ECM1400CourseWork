"""

This module covid_data_handler handles data updates.
It serves to:
    Request fresh covid data.
    Format data to be representable.
    Schedule covid data updates.

"""

from uk_covid19 import Cov19API  # python3.9 -m pip install uk-covid19
import json
import sched
import time
import logging

global covid_data
global newssched
newssched = sched.scheduler(time.time, time.sleep)


def parse_csv_data(csv_filename):
    """parse_csv_data function

    This function takes in a csv file and formates it correctly from the spec.

    Args:
        csv_filename (string) : Path to csv file with name e.g "~/Documents/mycoviddata.csv"

    Returns:
        list: Lines of the csv.


    """
    logging.info("Parsing csv data")
    f = open(csv_filename).read().split("\n")  # open and process file by line
    f.pop(-1)  # Remove Blank line
    return f


def process_covid_csv_data(covid_csv_data):
    """process_covid_csv_data Function

    This function takes in covid_csv_data and calculates 3 fields:
        - Cumulative new cases over seven days.
        - Current hospital cases (Those in hostipal due to covid)
        - Total deaths (in the data parsed)

    Args:
        covid_csv_data (list) : Formated csv_data by line

    Returns:
        tuple: A tuple containing 3 data entrys, last seven day cases, current hosptital cases and total deaths. (In that order)


    """
    logging.info("Processing covid data.")
    logging.info("Fields calculated:")
    last7days_cases = 0  # Thecases in the last 7 days should be calculated by summing the new cases by specemin date forthe last 7 days ignoring the first entry as the data is incomplete for that day
    # top row of current cases.
    current_hospital_cases = int(covid_csv_data[1].split(",")[5])
    logging.info("  current_hospital_cases :" + str(current_hospital_cases))
    total_deaths = 0
    specimanDataLn = None
    for x in range(
            1,
            len(covid_csv_data) -
            1):  # for general case of finding location of speciman date
        splitByCommaData = covid_csv_data[x].split(",")
        # index 6 is where speciman data is kept & is numeric checks for number
        # input
        if splitByCommaData[6].isnumeric() and specimanDataLn is None:
            specimanDataLn = x + 1  # start counting from next line
        if splitByCommaData[4].isnumeric() and total_deaths == 0:
            total_deaths = int(splitByCommaData[4])
        if specimanDataLn is not None and total_deaths != 0:
            break
    logging.info("  total_deaths :" + str(total_deaths))
    for x in range(specimanDataLn, specimanDataLn + 7):
        splitByCommaData = covid_csv_data[x].split(",")
        last7days_cases += int(splitByCommaData[6])

    logging.info("  last7days_cases :" + str(last7days_cases))

    return (last7days_cases, current_hospital_cases, total_deaths)


def covid_API_request(
    location=json.loads(
        open("config.json").read())["location"], location_type=json.loads(
            open("config.json").read())["location_type"]):
    """covid_API_request function

    This function takes in a location and location type and requests
    to the UK covid API for covid data about that region.
    -- Please note that depending on location type different kinds of data may / may not be available for use

    Args:
        location (string): Location must conform with the uk-covid data API and location_type var. More info here : (https://coronavirus.data.gov.uk/details/developers-guide/main-api)
        location_type (string): Please note that the values of the location_type variable are case-sensitive and must follow:
            overview
                Overview data for the United Kingdom
            nation
                Nation data (England, Northern Ireland, Scotland, and Wales)
            region
                Region data
            nhsRegion
                NHS Region data
            utla
                Upper-tier local authority data
            ltla
                Lower-tier local authority data

    Returns:
        list : a list of vaild & formated covid data entries from the covid api data from the uk gov.


    """

    filt = ['areaType=' + location_type, 'areaName=' + location]

    struc = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
        "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate"
    }

    api = Cov19API(filters=filt, structure=struc)
    data = api.get_json()["data"][0:30]
    return {"covidData":data}


def get_hospital_cases(
        location=json.loads(
            open("config.json").read())["nation"],
        location_type="nation"):
    """get_hospital_cases Function

    This function takes the location and location_type

    Args:
       location (string): Location must conform with the uk-covid data API and location_type var. More info here : (https://coronavirus.data.gov.uk/details/developers-guide/main-api)
        location_type (string): Please note that the values of the location_type variable are case-sensitive
        Unlike covid_API_request hospital cases data field only is provided in these 3 fields and they can only be used:
            overview
                Overview data for the United Kingdom
            nation
                Nation data (England, Northern Ireland, Scotland, and Wales)
            nhsRegion
                NHS Region data

    Returns:
        int: and integer value representing the most upto date data field containing hospital cases.


    """
    filt = ['areaType=' + location_type, 'areaName=' + location]
    struc = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "hospitalCases": "hospitalCases"
    }
    logging.info("Getting hospital cases from:" + str(location))
    api = Cov19API(filters=filt, structure=struc)
    temp = api.get_json()["data"][0:30]
    logging.info("Latest entry is from:" +
                 temp[0]["date"] +
                 ". With " +
                 str(temp[0]["hospitalCases"]) +
                 " hospital cases.")
    return temp[0]["hospitalCases"]


covid_data = covid_API_request()["covidData"]


def update_covid_data():
    """get_hospital_cases Function

    This function is used to update covid_data globally as a proxy for a scheduler.

    Args:
        None:

    Returns:
        None: (However updates covid_data)

    """
    logging.info("Trying to update covid data!")
    covid_data = covid_API_request()["covidData"]
# covid_API_request()


def schedule_covid_updates(update_interval, update_name, repeat=False):
    """schedule_covid_updates function

    This function is a secheduler function which serves add an update covid data on a scheduler.

    Args:
        update_interval (int): Number of seconds until and updates should be processed.
        update_name (string): The name of the scheduler to help identify them
        repeat (bool): A default bool of False set to true to schedule an update at this time every day.

    Returns:
        None

    """
    logging.info(
        "Covid data will be updated in " +
        str(update_interval) +
        " seconds.")
    newssched.enter(update_interval, 1, covid_API_request)
    if repeat:
        newssched.enter(
            update_interval,
            2,
            lambda: schedule_covid_updates(
                update_interval=24 * 60 * 60,
                update_name=update_name,
                repeat=repeat))
    newssched.run()

# schedule_covid_updates(10,"test")
