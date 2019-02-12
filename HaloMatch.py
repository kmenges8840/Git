# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 10:21:28 2018

Takes in Dataframe list of assets and checks to see if Augury already has installed 
Halo on this exact make and model of machine. Returns a vector (single column) 
of True / False

@author: Keith Menges
"""

# Import modules and csv list from Sisense of Halo machine/make/models
import pandas as pd
import re
import numpy as np

RawRef = pd.read_csv('HaloMachineMakesandModels.csv')
print(RawRef.info())

#Remove any duplicates and rows with N/A string in either make or Model, convert 
# all entries to lower case strings
RawRef = RawRef.drop_duplicates()
RawRef = RawRef.dropna()
RawRef = RawRef.applymap(str)
RawRef = RawRef.applymap(lambda s:s.lower())


Ref = RawRef[RawRef['model'] != "n\\a"]
print(Ref.info())

# Remove rows based on disqualifiers in specific type
Ref = Ref[Ref['specifictype'] != "recip compressor"]

# TO DO - Format the make/model columns to make string compares easier


# TO DO - Create alternative make/model string formats and append them to the row



# TO DO - Check new ref list versus old ref list and append any new entries into
# the permanent approved list

# TO DO - Create "permanent" list of approvable Makes/Models by creating a 
# csv in the spyder folder

#TO DO - Create method to manually append new makes/models to the permanent list
# Choose manual entry or automatic scan paths


# TO DO V2 - Create matching function that takes in string(s) and searches 
# approvable make/model

