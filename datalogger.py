from __future__ import print_function
from datetime import datetime
from datetime import date
import os
import json


class log:
    defaultFile = "performanceLog.json"
    def __init__(self,filename=defaultFile):
        #Find absolute path on current machine
        self.abs_path = os.path.join(os.path.dirname(__file__), filename)

    def logData(self,contact_list, connectionStatus, notification_status, ListStatus, listProcessingSuccessful=False):
        toStr = lambda t: "False" if(t==False) else "True"
        #Create log
        rdate = str(date.today())
        tempLog = {"Run Date": (str(rdate)+" @" + str(datetime.now().time())),
               "List Processing Successful": toStr(listProcessingSuccessful),
               "Connection Status": connectionStatus,
               "Contacted Individuals": contact_list,
               "Successful Notification": notification_status,
               "List Status": ListStatus,
               "DataLogged":True,
               }

        #Read current logs
        with open(self.abs_path, 'r') as f:
            currentLogs = json.load(f)

        #Log data using a stack like set up
        #pushing the newest log on the top and dropping the oldest one
        currentLogs = self.pushLog(currentLogs,newLog=tempLog)

        #Write logs to text file for easy viewing
        self.writeLogsToFile(currentLogs)

        #Rewrite logs
        with open(self.abs_path, 'w') as f:
            json.dump(currentLogs, f)

    def pushLog(self,currentLog,newLog):
        for i, e in reversed(list(enumerate(currentLog["Logs"]))):
            if i == 0:
                #after shifting old logs add new data
                currentLog["Logs"][i]=newLog
            else:
                #shift old logs
                currentLog["Logs"][i]=currentLog["Logs"][i-1]
        #return modified json structure
        return(currentLog)

    def createNewLog(self,numLogs = 5, logStructure= {"Connection Status" : {},"DataLoaded":False}, filename='debugLog.json'):
        try:
            logList = [logStructure for i in range(0,numLogs)]
            tempDic = {"Logs" : logList}
            with open(filename, "wb") as f:
                f.truncate(0)   #clear file data if it already exits
                json.dump(tempDic,f)
            return True #log created
        except:
            return False #Failed to create log

    def writeLogsToFile(self,Logs):
        firstLine= "See PerformanceLog.josn for contacted individuals and further information.\n"
        with open("logs.txt", "w") as f:
            f.truncate(0)
            f.write(firstLine)
            num = 0
            for log in Logs["Logs"]:
                if(log["DataLogged"]):
                    f.write("Log "+str(num+1)+":\n"+self.logToString(log)+"\n")
                    num+=1

    def logToString(self,log):
        #if any connection failed report connection status as false
        connection_status = str(log["Connection Status"]["email"] and log["Connection Status"]["gDrive"] and log["Connection Status"]["phone"])

        processing_success = log["List Processing Successful"]

        runDate = log["Run Date"]

        notify_success = str(log["Successful Notification"])

        return("Run on: " + runDate + " => [Connection Status: "+connection_status+", Processing Successful: "+processing_success+", List Status: "+log["List Status"]+", Notification Status: "+notify_success+"]")


#Test process when run directly
if __name__ == "__main__":
    log = log()
    contact = {
      "Email_Contacts": [
        "cutinoj@mail.gvsu.edu",
        "joseph.cutino@psware.com",
  	  "matt.mead@psware.com"
      ],
      "Phone_Contacts": [
        "5863821908",
  	  "2315573223"
      ]
    }
    status ={'gDrive': True, 'email': True, 'phone': True}
    log.logData(listProcessingSuccessful = "Valid",contact_list=contact, connectionStatus=status, notification_status=True, ListStatus="OutOfDate")

    #test create log
    log.createNewLog(numLogs=5, logStructure = {"Connection Status": status}, filename='testlog.json')
