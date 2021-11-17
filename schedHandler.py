import threading
class schedHandler:
    def __init__(self,schObj):
        self.schObj = schObj
        self.isRunning = False
        self.workerThread = threading.Thread(target=self.__workSched)
        self.events = []
    def addEvent(self,event,update_interval,update_name,info,*args,**kwargs):
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
        return self.events
    def removeEvent(self,e):
        for item in self.events:
            if e in item["events"]:
                self.events.remove(item)
        self.schObj.cancel(e)
    def runSched(self):
        if not self.isRunning:
            self.isRunning = True
            self.workerThread.start()
    def __workSched(self):
        self.schObj.run()
        self.isRunning=False
