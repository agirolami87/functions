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
import pyarrow.parquet as pq
import pyarrow as pa
import s3fs
from pyarrow.filesystem import S3FSWrapper
from .preprocessor import BaseTransformer

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
    
class ToParquet(BaseTransformer):
    '''
    Denormalize and save as parquet file in COS.
    '''
    
    def __init__(self, sens_pos, X, Y, Z, cos_credentials, output_status):
        self.sens_pos = sens_pos
        self.X = X
        self.Y = Y
        self.Z = Z
        self.cos_credentials= cos_credentials
        self.output_status = output_status
        super().__init__()

    def execute (self, df):
        df = df.copy()
        bucket = 'iotcs-as-bucket'
        path = 's3test-alberto-%s.parquet' %(dt.datetime.now().isoformat())
        bucket_uri = '{bucket}/{path}'.format(**{'bucket':bucket, 'path': path})
        sink = fs.open(bucket_uri, 'wb')
        df2 = []
        for sens in df[self.sens_pos].drop_duplicates():
            df1 = pd.concat([pd.Series([int(element) for list_ in df[df[self.sens_pos]==sens][axis].str.split(',').values for element in list_]).rename(axis) for axis in [self.X,self.Y,self.Z]], axis=1)
            df1[self.sens_pos] = sens
            df2.append(df1)
        df2 = pd.concat(df2, ignore_index=True)
        ta=pa.Table.from_pandas(df2)
        pw = pq.ParquetWriter(sink, schema=ta.schema)
        pw.write_table(ta)
        df[self.output_status]=bucket_uri
        return df  



