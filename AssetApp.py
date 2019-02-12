# -*- coding: utf-8 -*-
"""
Asset Approval Tool
Reads a CSV or XLS/X file, extracts asset information, analyzes the information
to determine if the asset is Halo compatible and then returns a new file
with summary of results
"""

import pandas as pd
import Tkinter, tkFileDialog

# Import File function
#---------------------------------------------------------------------------
# INPUTS: Path and filename, via file dialog 
# for xls/x files, sheet number can also be specified but has to be done so manually

# Open file via dialog
root = Tkinter.Tk()
file_path = str(tkFileDialog.askopenfilename())
root.destroy()

# set sheet number for xls files, default is first sheet (0)
sheet = 0

# Check if xls/x or csv and import using appropriate module
try:
    if '.csv' in file_path:
        rawtable = pd.read_csv(file_path,skip_blank_lines=True)
    elif '.xls' in file_path:
        rawtable = pd.read_excel(file_path,sheet_name=sheet)
       
    print("Raw Input Table Information:\n")
    print(rawtable.info())
    
except:
    print('No such file or directory! \n Please confirm file name and location')
    print('Remember the file needs to be of type CSV or XLS/X')



# Transform Table function
#------------------------------------------------------------------------------

# List of column labels we want to keep
labels = ['asset','name','model','make','mfg','manuf','vendor',
          'speed','rpm','type','style','design','supplier',
          'equipment','equip','motor','duty','cycle','capacity','size','hp',
          'item','desc','service','class']

#Create new table with only columns where column label matches labels list
simptable = rawtable.loc[:, rawtable.columns.str.contains(('|'.join(labels)),case=False)]
simptable = simptable.loc[:, ~simptable.columns.str.contains('^Unnamed')]


#Analyze Table function
#------------------------------------------------------------------------------

#Replace all missing values with missing string and Convert all entries to lower case strings
simptable.fillna(value='missing',inplace=True)
simptable = simptable.applymap(str)
simptable = simptable.applymap(lambda s:s.lower())

#join all elements into one big ass string per row
simptable = simptable.iloc[:,:].apply(lambda x: ''.join(x), axis=1)
simptable = simptable.to_frame()

#Add empty columns to table
simptable['Aprpts']=''
simptable['DQpts']=''
simptable['Approval']=''
simptable['Product']=''
simptable['searchlink']=''

#Check for keyword disqualifiers and approval words and total them up
# TO DO V2 - Create permanent list files for DQ and App using Augury db
# TO DO V2 - Create matching function that matches approvable make/models
# TO DO V2 - Create Summary output information for totals/types, .value_counts() method

dq = ['robot','servo','stepper','reciprocating','reciproc','diaphragm','piston','engine',
      'metering','diesel','vilters','vilter','roof top unit','rtu','forge','actuator',
      'submer','scroll','peristaltic','steam trap','spirax']

App = ['centrifugal','goulds','ansi','b&g','gosset','chill','cool','trane','screw','gearbox',
       'air han','ahu','york','mcquay','carrier','griswold','grundfos','boiler feed','tower',
       'gear','continuous','blower','vacuum','draft','howden','twin city','psg',
       'atlas','bornemann','magnatex','rotary lobe','netzsch','flowserve','cp pumpen',
       'richter','roots','twin screw','durco','sihi','travaini','gould']

for i,v in simptable.iterrows():
    countdq = 0
    countApp = 0
    for word in dq:
        if word in simptable.loc[i,0]:
            countdq += 1
        simptable.loc[i,'DQpts']   = countdq 
    for word in App:
        if word in simptable.loc[i,0]:
            countApp += 1
        simptable.loc[i,'Aprpts']   = countApp     

#Approval logic and product assignment

for i,v in simptable.iterrows():
    dqsum = simptable.loc[i,'DQpts']
    appsum = simptable.loc[i,'Aprpts']
    if (dqsum > appsum):
         simptable.loc[i,'Approval'] = 'Disqualified'
    elif (appsum == dqsum): 
         simptable.loc[i,'Approval'] = 'More information necessary'
    elif (appsum == 1) and (dqsum == 0):
         simptable.loc[i,'Approval'] = 'More information necessary'
    else: 
         simptable.loc[i,'Approval'] = 'Preliminary approval'
         simptable.loc[i,'Product'] = 'Halo'      
    
# Output new file function
#------------------------------------------------------------------------------

# concatenate approval columns with raw input table         
result = pd.concat([rawtable, simptable.iloc[:,1:]], axis=1)

glink='https://www.google.com/search?q=' 
result['searchlink']= glink + result.iloc[:,1]  + '&rlz'      

#create output path and filename which is original file plus Prelim and date
from datetime import date
import os
fp = (os.path.splitext(file_path)[0])
output_path = fp + 'Prelim' + str(date.today()) + '.csv'


result.to_csv(output_path)





