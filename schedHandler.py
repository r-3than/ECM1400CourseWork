"""

This module schedHandler contains a schedHandler object which:
    Handles scheduler objects.
    Adding new events onto the scheduler.
    Removing already queued events on the scheduler.
    Hosts the schedule object on a seperate thread to avoid main.py waiting on the scheduler.

"""

import threading
import logging


class schedHandler:
    """The schedHandler, handles schedular objects so that updates are formated correctly.
    It provides to:
        Repeat updates if required.
        Remove updates and scheduled events.
        Remove updates once completed
        Handle the sched on another thread to not interupt the flask api.

    """

    def __init__(self, schObj : object) -> None:
        """schedHandler __init__ method

        Args:
            schObj (sched.scheduler object): A scheduler object to host events on.
        """
        self.schObj = schObj
        self.isRunning = False
        self.workerThread = threading.Thread(target=self.__workSched)
        self.events = []
        """
        Attributes:
            schObj (sched.scheduler object): The parsed scheduler to handle.
            isRunning (bool): A boolean depicting if the workerThread is still running.
            workerThread (threading.Thread object): The refrence to the worker thread.
            events (list of dictiontaries): holding info about events and data pointers
        """
        logging.info("A schedHandler has been created!")

    def addEvent(
            self,
            event : object,
            update_interval : int,
            update_name : str,
            info : str,
            *args,
            **kwargs) -> None:
        """addEvent method

        Adds events onto the scheduler and handles them for the user.

        Args:
            event (function) : The event that should be run after the update_interval
            update_interval (int): Number of seconds until and updates should be processed.
            update_name (string): The name of the scheduler to help identify them
            repeat (bool): A default bool of False set to true to schedule an update at this time every day.

        """
        repeater = None
        info = str(info)
        main = self.schObj.enter(update_interval, 1, event, argument=(args))
        events = [main]
        if "repeat" in kwargs:
            if kwargs["repeat"]:
                repeater = self.schObj.enter(
                    update_interval, 2, self.addEvent, argument=(
                        event, 24 * 60 * 60, update_name, info, args,), kwargs=kwargs)
                events.append(repeater)

        info = {"content": info, "title": update_name, "events": events}

        self.schObj.enter(update_interval, 3, self.__cleanup, argument=(info,))
        logging.info("Event has been added to the scheduler!")
        self.events.append(info)
        self.runSched()

    def __cleanup(self, info : dict) -> None:
        for item in self.events:
            if info == item:
                self.events.remove(item)

    def getEvents(self) -> list:
        logging.info("Event list has been requested!")
        """getEvents method

        Returns:
            (list of dictionaries): holding info about events and data pointers
        """
        return self.events

    def removeEvent(self, e : tuple) -> None:
        """removeEvent method

        Removes event via the event data refrence (this is unique and hence is why it is used)

        Args:
            e (event dict) : The event that should be run after the update_interval

        """
        for item in self.events:
            if e in item["events"]:
                self.events.remove(item)
                logging.info("Event has been removed.")
        self.schObj.cancel(e)

    def runSched(self) -> None:
        """runSched method

        Is run whenever a new event is on the sched, if the worker thread is still running the sched no need to change anything
        If the worker thread is finished create a new one to run the sched.
        """
        logging.info("Checking if the scheduler is running")
        if not self.isRunning:
            logging.info("Scheduler is not running workerThread starting....")
            self.isRunning = True
            self.workerThread = threading.Thread(target=self.__workSched)
            self.workerThread.start()

    def __workSched(self) -> None:
        logging.info("Worker thread started on the schedule!")
        self.schObj.run()
        self.isRunning = False
        logging.info("Worker thread finished and ready to be reused.")
