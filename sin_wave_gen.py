# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 09:13:37 2019

#@author: Keith
#"""

import numpy as np
import pandas as pd    

def signal(f, fs, time_window, amplitude, SNR):
   """ f = sin frequency, fs = sampling frequency in Hz, time_duration is \
   time block of sample, 
   and amplitude is in G's, SNR is signal to noise ratio in power"""
   num_samples = int(fs*time_window)
   time_series = list(np.linspace(0,time_window,num=(fs*time_window)))
   # The sampling rate of the analog to digital convert   
   sine_wa = [amplitude*(np.sin(2 * np.pi * f * x/fs)) for x in range(num_samples)]
  
   Anoise = amplitude/(np.sqrt(SNR))
   sigma = Anoise/3
   noise = np.random.normal(0,sigma,num_samples)
   sine_wa = [sum(x) for x in zip(sine_wa,noise)]
   
   sine_wave=pd.DataFrame(zip(time_series,sine_wa),columns=['time(s)','amplitude(G)'])
   
   return sine_wave
#test = sin_wave_gen.signal(10,1024,0.5,4,100)
#plt.scatter(x=test['time(s)'],y=test['amplitude(G)'])