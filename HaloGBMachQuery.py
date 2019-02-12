
"""
Created on Tue Feb  5 13:00:24 2019

Query to mongoDB to retrieve machine ID for all machines with Gear Drives that are\
not Halo X or Demo machines

@author: Keith Menges
"""
from pymongo import MongoClient
import pandas as pd

host = 'mongodb://kmenges:gV4zhKLhLLoDJYRZ@production-gcp-shard-00-00-kxuwc.gcp\
mongodb.net:27017,production-gcp-shard-00-01-kxuwc.gcp.mongodb.net:27017,\
production-gcp-shard-00-02-kxuwc.gcp.mongodb.net:27017/production?\
ssl=true&replicaSet=production-gcp-shard-0&authSource=admin&readPreference=\
secondary'

client = MongoClient(host=host)

# Save a list of names of the databases managed by client
db_names = client.list_database_names()
#print(db_names)

# Save a list of names of the collections managed by the database
coll_names = client.production.list_collection_names()
#print(coll_names)

#List of component types
com_types_ex = client.production.component_types.find_one()
machines_ex = client.production.machines.find_one()
session_ex = client.production.sessions.find_one()
distinct_comp = client.production.component_types.distinct("name")

# Set filter criteria
# 1 - Remove all scope machines
# 2 - Only machines with component 2 equal to gearbox
# 3 - No Demo machines
# 4 - No Halo X Machines
criteria = {"continuous":True, 'components.1.type' : "gearbox",'containedIn.company.name':{"$ne":"Demo"}\
,"tags":{"$ne":"halo_x"}}
#criteria_aug = {"continuous":False, 'components.1.type' : "gearbox"}

# Find machines matching criteria
#TO DO - filter out Halo X tagged machines
halo_gear = client.production.machines.find(criteria)
#aug_gear = client.production.machines.find(criteria_aug)
num_halo_gear = halo_gear.count()
#num_aug_gear = aug_gear.count()

#print summary of search results
print("\nThere are currently " + str(num_halo_gear) + " Non Demo,Non Research Halo machines with gearboxes\n")
#print("There are currently " + str(num_aug_gear) + " scope machines with gearboxes\n")

halo_gear_data = list(halo_gear) 
#aug_gear_data = list(aug_gear) 

#Create list of ID's
global gear_ids 
gear_ids = [] 
for index in range(len(halo_gear_data)):
        gear_ids.append(str(halo_gear_data[index]['_id']))

#Create Dataframe of machine links and export as CSV
HaloGBMachines = pd.DataFrame({'machine_id':gear_ids})
HaloGBMachines['link'] = str('https://app.augury.com/#/machines/') + HaloGBMachines.machine_id    
HaloGBMachines.to_csv('/home/keith/Documents/Augury_Code/algo/GearDrive/HaloGBmach.csv')              


# Close connection to mongo
client.close()
 

