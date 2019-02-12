# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 11:33:34 2018

Script takes in basic meta data from machines with gear drives and estimates
the potential gear mesh frequencies 

@author: Keith Menges
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# TO DO - Read Input Meta Data from machine header info
# Manual entry for now
HP = 10
inputRPM = 1450
ratio=21.15
linefreq = 60

# Basic Gear Calculations
outputRPM = inputRPM / ratio            #output speed
inTorque = (HP*inputRPM/5252)
outTorque=(HP*inputRPM/5252)*ratio      #output torque in Ft-Lbs

# Determine likely number of stages
if ratio <= 5.9:
    stages = 1 
elif (ratio > 5.9 and ratio <= 18):
    stages = 2
elif (ratio >18 and ratio <= 129):
    stages = 3
else:
    stages = 4

# For Multistage gearboxes, estimate individual actual stage ratios
# Linear interpolation knowing that stage ratios generally decrease from first
ratioeven = ratio**(1./stages)
stagelist = list(range(1,stages+1))
slope=0.5                                   # estimate based on engineering refs
b = ratioeven + (slope*(0.5*stages+0.5))
ratios =  map(lambda x: (-slope*x + b),stagelist)
ratios = list(np.around(np.array(ratios),3))        

# Determine English or Metric Units and Calculate Module or Diametral Pitch
# Convert modules from mm per tooth to diampitch in 1/in
if linefreq == 50: 
    diampitch = 25.4 / np.array([0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.60,0.65,0.7,0.75,0.8,0.85,0.9,1
                             ,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3,3.5,3.75,4,4.5,5,6,6.5,7,8,9,10,11,12
                             ,14,16,18,20,25,28,32,36,40,45,50])
else: 
    diampitch = np.array([2,2.25,2.5,3,4,5,6,8,10,12,16,20,24,32,40,48,64,96,120,150,200])

# Estimate Housing Width based on Horsepower, Torque, Ratio, and input RPM
# NEEDS UPDATING - LOWER and UPPER LIMIT Bounds
Width = 2  

# Estimate pinion diameter from first stage ratio and width of housing
piniondiam = Width / (1+ratios[0]) 

# Estimate nominal PLV 
nomPLV = 0.262*inputRPM*piniondiam
    
# TO DO - Compute range of Pitch Line velocities from approximate sizes of Pitch Diameter

plv = pd.DataFrame(range(2000,2600,1))
plv.columns = ['PLVinFPM']
pitchd = (plv) / (.262*inputRPM)

# Create 2D array of possible Teeth Number 
# N = diampitch / pitchd or diampitch multiplied by 1/pitchd
pitchd = 1/pitchd

N = np.outer(pitchd,diampitch)          # multiply each value in each row by each value in each column
N = pd.DataFrame(N)
N = N.loc[(N!=0).any(1)]                # drop rows with zeros
N = N.join(plv)                         # add PLV value column to N

# Remove values that are not near to whole numbers
mask = np.absolute(N - N.round(decimals=0)) < 0.09 
Nreal = N[mask]
Nreal = Nreal.round(decimals=0)

# Remove values that violate minimum design criteria - for reducers only
# Pinion Teeth must be greater than 12, less than 300 
# prime numbers of teeth above 100 are undesirable

# Prime Number Generator
def primes(n): # simple Sieve of Eratosthenes 
   odds = range(3, n+1, 2)
   sieve = set(sum([range(q*q, n+1, q+q) for q in odds],[]))
   return [2] + [p for p in odds if p not in sieve]

primefilt = primes(200)[25:]        # list of primes above 100
# Filtering tooth counts based on known engineering practices
mask2 = Nreal.isin(primefilt)
mask2 = np.invert(mask2)            # invert so mask only keeps if Not in list

Nreal = Nreal[mask2]                # Remove any that are prime numbers above 100

mask3 = Nreal >= 8
Nreal = Nreal[mask3]                # keeps values above or equal to 8
mask4 = Nreal <= 300
Nreal = Nreal[mask4]                #keeps values below or equal to 300
Nreal = Nreal.apply(pd.to_numeric,downcast = 'integer')

Nfinal = Nreal.apply(pd.value_counts).fillna(0)     #count frequency of tooth counts
Nfinal['total'] = Nfinal.sum(axis=1)                  # add sum column

NewIndex = pd.to_numeric(list(Nfinal.index),downcast = 'integer') #fuckery 
Counts = pd.to_numeric(list(Nfinal.total), downcast = 'integer')   # more fuckery 

Toothy = pd.DataFrame(Counts,index=NewIndex)


# TO DO - Create Tooth count plots and summary information
Toothy.plot(kind='bar')






# Create lists of known gear ratios from common GB mfgs
Falk = {
        'single':(1.84,2.03,2.25,2.49,2.76,3.05,3.38,3.74,4.13,4.57,5.06,5.60),
        'double':(5.6,6.2,6.86,7.59,8.4,9.3,10.29,11.39,12.61,13.95,15.44,17.09
                  ,18.91,20.93,23.16,25.63,28.36,31.39,34.74),
        'triple':(23.16,25.63,28.36,31.39,34.74,38.44,42.54,47.08,52.11,57.66,
                  63.82,70.62,78.16,86.50,95.73,105.9,117.2,129.7,143.6,
                  158.9,175.9,194.6,215.4),
        'quadruple':(105.9,117.2,129.7,143.6,158.9,175.9,194.6,215.4,238.4,263.8,
                     291.9,323.1,357.5,395.7,437.9)}

#TO DO - Estimate Gearmesh Frequencies for all combinations
   


# Print Summary info to shell
print('Likely number of stages is:' + str(stages))




