# *****************************************************************************
# Â© Copyright IBM Corp. 2018.  All Rights Reserved.
#
# This program and the accompanying materials
# are made available under the terms of the Apache V2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
# *****************************************************************************

import os
import urllib3
import json
import numpy as np
import pandas as pd
import numbers
import datetime as dt
from iotfunctions.preprocessor import BaseTransformer

PACKAGE_URL = 'git+https://github.com/agirolami87/functions.git'

class TiltCalc(BaseTransformer):
    '''
    Calculates tilt values from acc values.
    '''
    url = PACKAGE_URL
    
    def __init__(self, input_item, output_item_x,output_item_y):
                
        self.input_item = input_item
        self.output_item_x = output_item_x
        self.output_item_y = output_item_y
        super().__init__()

    def execute(self, df):
        df = df.copy()
        a=df[self.input_item].str.split('\[|,|\]').values
        for r,c in enumerate(a):
            df.loc[r,self.output_item_x] = np.arcsin(float(c[1])/9.8)
            df.loc[r,self.output_item_y] = np.arcsin(float(c[2])/9.8)
        return df

class TiltCalcString(BaseTransformer):
    '''
    Calculates tilt values from acc values.
    '''
    url = PACKAGE_URL
    
    def __init__(self, input_item, output_item):
                
        self.input_item = input_item
        self.output_item = output_item
        super().__init__()

    def execute(self, df):
        df = df.copy()
        a=df[self.input_item].str.split('\[|,|\]').values
        for r,c in enumerate(a):
            df.loc[r,self.output_item] = '['+str(np.arcsin(float(c[1])/9.8))+','+str(np.arcsin(float(c[2])/9.8))+']'
        return df



