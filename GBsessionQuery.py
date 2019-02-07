#def query(machine_ids):
"""
Created on Thursday Feb 7th, 2019
Query to mongoDB to retrieve sessions from mongo based on machine_id with \
analyst results
@author: Keith Menges
"""
from pymongo import MongoClient
from bson.objectid import ObjectId
from HaloGBMachQuery import gear_ids
import pandas as pd
   
host = 'mongodb://kmenges:gV4zhKLhLLoDJYRZ@production-gcp-shard-00-00-kxuwc.gcp\
mongodb.net:27017,production-gcp-shard-00-01-kxuwc.gcp.mongodb.net:27017,\
production-gcp-shard-00-02-kxuwc.gcp.mongodb.net:27017/production?\
ssl=true&replicaSet=production-gcp-shard-0&authSource=admin&readPreference=\
secondary'

client = MongoClient(host=host)
     
#Example session to explore in var explorer
session_ex = client.production.sessions.find_one()
  
# Set filter criteria
# 1 - machine_id
# 2 - analyst approved result
# TO DO # 3 - fault types

#TEMP 
machine_ids = gear_ids
  
session_data = []
for machine_id in machine_ids:
    # for all analyst results
    criteria = {"machineId":ObjectId(machine_id),"results.type":"analyst"}
    # for only GEAR FRICTION analyst results
    criteria2 = {"machineId":ObjectId(machine_id),"results.type":"analyst"\
                 ,'results.components.failure_modes.key':'gear'}
    gear_ses= client.production.sessions.find(criteria2)   
    session_data.append(list(gear_ses)) 

#Create list of ID's
session_list= [] 
for index in range(len(session_data)):
    for index2 in range(len(session_data[index])):
        session_list.append(str(session_data[index][index2]['_id']))

#Create Dataframe of machine links and export as CSV
HaloGBSessions = pd.DataFrame({'session_id':session_list})
HaloGBSessions['link'] = str('https://app.augury.com/#/analyze/') + HaloGBSessions.session_id   
HaloGBSessions.to_csv('/home/keith/Documents/Augury_Code/algo/GearDrive/HaloGBSessions.csv')    


# Close connection to mongo
client.close()

    #return sessionlist;

