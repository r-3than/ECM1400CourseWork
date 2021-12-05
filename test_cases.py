from covid_data_handler import parse_csv_data
def test_parse_csv_data():
    data = parse_csv_data("nation_2021-10-28.csv") 
    assert len(data) == 639

test_parse_csv_data()

from covid_data_handler import process_covid_csv_data
def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases, total_deaths = process_covid_csv_data(parse_csv_data("nation_2021-10-28.csv"))
    assert last7days_cases == 240_299 
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

test_process_covid_csv_data()

from schedHandler import *
import sched , time
def test_schedHandler():
    testsched = sched.scheduler(time.time, time.sleep)
    testSchedHandler = schedHandler(testsched)
    assert type(testSchedHandler) == schedHandler
    queuedEvents = testSchedHandler.getEvents()
    assert len(queuedEvents) == 0
    testEvent = test_parse_csv_data
    testSchedHandler.addEvent(testEvent,2,"testEvent","Test") # schedule and event in 2 seconds time
    assert len(queuedEvents) == 1 # check it is in the queue
    time.sleep(3) # sleep for 3 seconds until its done
    assert len(queuedEvents) == 0 # check the event has fired and been cleaned up.
    
    


test_schedHandler()