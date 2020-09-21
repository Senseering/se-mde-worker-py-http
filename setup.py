#from src.reader import reader
import requests
from requests.auth import HTTPBasicAuth
import os
import json
import ssl
import time 

# This restores the same behavior as before.


class Worker():
    def __init__(self):
        relPath = os.path.dirname(__file__)
        with open(relPath + "/config.json", 'r') as outfile:
            self.config = json.load(outfile)
            with open( relPath+ self.config["privkey"][1:], 'r') as keyFile:
                    self.config["privkey"] = keyFile.read()
            with open( relPath+ self.config["schema"]["input"][1:], 'r') as inputSchema:
                   self.config["schema"]["input"]=json.load(inputSchema)
            with open( relPath+ self.config["schema"]["output"][1:], 'r') as outputSchema:
                   self.config["schema"]["output"]= json.load(outputSchema)
            
            with open( relPath+ self.config["info"]["worker"]["description"][1:], 'r') as workerInfo:
                   self.config["info"]["worker"]["description"]= workerInfo.read()
            with open( relPath+ self.config["info"]["input"]["description"][1:], 'r') as inputInfo:
                   self.config["info"]["input"]["description"]= inputInfo.read()
            with open( relPath+ self.config["info"]["output"]["description"][1:], 'r') as outputInfo:
                self.config["info"]["output"]["description"]= outputInfo.read()

        self.id_worker = self.config["credentials"].split(":")[0]
        self.apiKey = self.config["credentials"].split(":")[1]
        del self.config["credentials"]

        self.url = self.config["url"]
        del self.config["url"]
        del self.config["settings"]

        self.connected = False

    ## returns next process (hub)
    def connect(self):
        r = requests.post( self.url+"/worker/"+self.id_worker+"/update",
        data=json.dumps(self.config),
        auth=HTTPBasicAuth(self.id_worker, self.apiKey),verify=False, 
        headers = {'Content-Type': 'application/json'})
        if r.status_code == 200:
            self.connected = True
        return r.status_code


    def publish(self,data): 
        toSend = {"data":data}
        #toSend["options"] = {"ttl":100000}
       
        r = requests.post(self.url+"/worker/"+self.id_worker+"/data",
        data=json.dumps(toSend),
        auth=HTTPBasicAuth(self.id_worker, self.apiKey),verify=False, 
        headers = {'Content-Type': 'application/json'})
        return r.status_code