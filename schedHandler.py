import threading
class schedHandler:
    """The schedHandler, handles schedular objects so that updates are formated correctly.
    It provides to:
        Repeat updates if required.
        Remove updates and scheduled events.
        Remove updates once completed
        Handle the sched on another thread to not interupt the flask api.

    """
    def __init__(self,schObj):
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
    def addEvent(self,event,update_interval,update_name,info,*args,**kwargs):
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
        main=self.schObj.enter(update_interval,1,event,argument=(args))
        events = [main]
        if "repeat" in kwargs :
            if kwargs["repeat"] == True:
                repeater=self.schObj.enter(update_interval,2,self.addEvent,argument=(event,24*60*60,update_name,info,args,),kwargs=kwargs)
                events.append(repeater)
        
        info = {"content":info,"title":update_name,"events":events}

        self.schObj.enter(update_interval,3,self.__cleanup,argument=(info,))

        self.events.append(info)
        self.runSched()
    def __cleanup(self,info):
        for item in self.events:
            if info == item:
                self.events.remove(item)
    def getEvents(self):
        """getEvents method

        Returns:
            (list of dictionaries): holding info about events and data pointers
        """
        return self.events
    def removeEvent(self,e):
        """removeEVent method

        Removes event via the event data refrence (this is unique and hence is why it is used)

        Args:
            e (event dict) : The event that should be run after the update_interval

        """
        for item in self.events:
            if e in item["events"]:
                self.events.remove(item)
        self.schObj.cancel(e)
    def runSched(self):
        """runSched method

        Is run whenever a new event is on the sched, if the worker thread is still running the sched no need to change anything
        If the worker thread is finished create a new one to run the sched.  
        """
        if not self.isRunning:
            self.isRunning = True
            self.workerThread = threading.Thread(target=self.__workSched)
            self.workerThread.start()
    def __workSched(self):
        self.schObj.run()
        self.isRunning=False
