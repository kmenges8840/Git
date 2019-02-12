#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 16:32:21 2019

@author: keith
"""

from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId

host = 'mongodb://kmenges:gV4zhKLhLLoDJYRZ@production-gcp-shard-00-00-kxuwc.gcp\
mongodb.net:27017,production-gcp-shard-00-01-kxuwc.gcp.mongodb.net:27017,\
production-gcp-shard-00-02-kxuwc.gcp.mongodb.net:27017/production?\
ssl=true&replicaSet=production-gcp-shard-0&authSource=admin&readPreference=\
secondary'

client = MongoClient(host=host)

known_sess = "5bd9c5e0fab14e00017af6fc"
known_mach = "5b92a79f6bf4f9000147355b"
# Save a list of names of the databases managed by client
db_names = client.list_database_names()
#print(db_names)

# Save a list of names of the collections managed by the database
coll_names = client.production.list_collection_names()
#print(coll_names)

#List of component types
com_types_ex = client.production.component_types.find_one()
com_diag = client.production.component_diagnoses.distinct('diagnosis')
machines_ex = client.production.machines.find_one({'_id':ObjectId(known_mach)})
session_ex = client.production.sessions.find_one({'_id':ObjectId(known_sess)})
distinct_comp = client.production.component_types.distinct("name")