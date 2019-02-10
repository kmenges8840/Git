# -*- coding: utf-8 -*-
"""
Library that creates vibration wave forms for use in development work

#@author: Keith
#"""

import numpy as np
import pandas as pd    

def sine(f, fs, time_window, amplitude, SNR):
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
   
   sine_wave=pd.DataFrame(zip(time_series,sine_wa),columns=['time_s','amplitude_g'])
   
   return sine_wave
   
def composite_wave(*args):
    """ Function takes in any number of waveforms of equivalent length, adds
    their amplitudes to form composite waveform and returns the same as a
    pandas dataframe with 2 columns, first is time, second is amplitude. TWF
    inputs must be in form of 2 column array or pandas dataframe with time as
    first column and amplitude as the second column. 
    Waveforms can be in any units, no scaling or transforms are performed """
    
    for i in args:
        if type(i) == np.ndarray:
            labels = list(i.dtype.names)
            i = pd.DataFrame(i,columns=[labels])
            
        elif type(i) == pd.core.frame.DataFrame: 
            labels = list(i.columns.values)

    n_rows = len(args[0])
    n_cols = 2
    composite = pd.DataFrame(np.zeros((n_rows, n_cols)),columns=labels)

    for j in np.arange(len(args)):
        composite = composite.add(args[j])
        
    composite[labels[0]] = composite[labels[0]].divide(len(args))
    
    return composite
    
        
