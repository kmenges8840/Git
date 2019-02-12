# -*- coding: utf-8 -*-
"""
Library of vibration analysis related functions. Does not duplicate other 
functions already found in numpy, scipy, etc. 

"""

import numpy as np
import pandas as pd

def twf_scale(twf,units=ips2,output=g):
    """ Function takes in a time wave form as either a numpy array or pandas
    dataframe with the first column as time in seconds and second column 
    as value. Can accept any type of engineering unit and convert to any other 
    that represents the same characteristic. Default arguments are ips**2 for 
    input units and G's for output units. Note *** IT DOES NOT INTEGRATE OR 
    DIFFERENTIATE. See twf_transform() for that functionality. Returns a 2 
    column dataframe with specifid engineering units for amplitude. """
    
    # TO DO - check if array or dataframe
    if type(twf) == np.ndarray:
        labels = list(twf.dtype.names)
        twf = pd.DataFrame(twf,columns=[labels])
    
    elif type(twf) == pd.core.frame.DataFrame: 
        labels = list(twf.columns.values)

    # TO DO - build list of engineering unit conversions
    conversions = pd.read_csv('eng_uni_conv')
    
    
    # TO DO - Rescale using scalar broadcasting
    