#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 19:20:15 2019

@author: ghosty
"""

import os
from datetime import datetime
import pytz
import h5py
import csv
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
#read filename
stamp = '1541962108935000000_167_838.h5'
filename = stamp
stamp = stamp[0:19]
stamp = int(stamp)/10**9

#convert time
dt = datetime.fromtimestamp(stamp)
tz=pytz.timezone('CET')
utc_dt = dt.astimezone(pytz.utc)
cern_dt = dt.astimezone(tz)
print('UTC: '+str(utc_dt))
print('CERN: '+str(cern_dt))


#read hdf5 file
try:
    os.rename("/home/ghosty/gsoc/python_awake/1541962108935000000_167_838.h5", "/home/ghosty/gsoc/python_awake/1541962108935000000_167_838.hdf5")
    f = h5py.File("/home/ghosty/gsoc/python_awake/1541962108935000000_167_838.hdf5", 'r')
    os.rename("/home/ghosty/gsoc/python_awake/1541962108935000000_167_838.hdf5", "/home/ghosty/gsoc/python_awake/1541962108935000000_167_838.h5")
except:
    f = h5py.File("/home/ghosty/gsoc/python_awake/1541962108935000000_167_838.hdf5", 'r')
    
def foo(name, obj):
   print(name, obj)
   return None

dd=[]
#csv file headers
row = ['Groups', ' Dataset Name', ' Size', 'Shape', 'Type']
dd.append(row)
#function to check if a detaset has been encountered, if true, append its attributes to a list
def extract(name, node):
    if isinstance(node, h5py.Dataset):
        temp = []
        temp.append(name)
        xx = name.split('/')
        temp.append(xx[-1])
        size = node.size
        temp.append(str(size))
        shape = node.shape
        temp.append(str(shape))
        try:
            dtype = str(node.dtype)
            temp.append(str(dtype))
        except:
            1==1
        dd.append(temp)
    return None


f.visititems(extract)
#write the data to a csv file
with open('data.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(dd)
    
    
    
#reading the image data
dp = f['/AwakeEventData/XMPP-STREAK/StreakImage/streakImageData'] 
dh = f['/AwakeEventData/XMPP-STREAK/StreakImage/streakImageHeight']
dw = f['/AwakeEventData/XMPP-STREAK/StreakImage/streakImageWidth']

dp = dp[...]
dh = dh[...]
dw = dw[...]

dp = np.reshape(dp,(int(dh),int(dw)))

dp = scipy.signal.medfilt(dp)
plt.imshow(dp)
plt.imsave('img.png',dp)

