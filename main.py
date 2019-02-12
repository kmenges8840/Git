#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 15:20:42 2019

@author: keith
"""

import pandas as pd
import numpy as np
import playground.sin_wave_gen as sin_wave_gen



twf = sin_wave_gen.sine(59,4096,1,2,50)
units = ips2
output = g

# TO DO - check if array or dataframe
if type(twf) == np.ndarray:
    labels = list(twf.dtype.names)
    twf = pd.DataFrame(twf,columns=[labels])

elif type(twf) == pd.core.frame.DataFrame: 
    labels = list(twf.columns.values)

# TO DO - build list of engineering unit conversions
conversions = pd.read_csv('eng_uni_conv')
