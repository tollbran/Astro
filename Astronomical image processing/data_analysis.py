# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:13:35 2021

@author: Tolbran
"""

import matplotlib.pyplot as plt
import scipy as sp
import pandas as pd
import numpy as np
def magnitude_graph_cumu(excel_file):
    data = pd.read_excel(excel_file)
    mag_column = data.loc[:,'Instrumental Magnitude']
    mag = mag_column.values
    sp.asarray(mag)
    print(mag)
    magn_counter = 0
    euclid_sum = 0
    x =[]
    y=[]
    error = []
    y1=[]
    while magn_counter < 20:
        
        number_count = sp.count_nonzero(mag < magn_counter)
        x.append(magn_counter)
        y.append(sp.log10(number_count))
        #simple poisson statistics for now
        error.append(sp.log10(sp.sqrt(number_count)))
        euclid_num = 0.6*magn_counter - 7.5
        y1.append(euclid_num)
        magn_counter += 0.5
    
    sp.asarray(x)
    sp.asarray(y)
    sp.asarray(y1)
    print(error)
    sp.asarray(error)
    plt.scatter(x,y)
    plt.plot(x,y1,color='r')
    #plt.errorbar(x,y,yerr=error)
    plt.grid()
    plt.xlabel('Magnitude m')
    plt.ylabel('log(N<m)')
    plt.ylim(-3, 6)
    plt.show()
    

def magnitude_graph(excel_file):
    data = pd.read_excel(excel_file)
    error=0.002
    mag_column = data.loc[:,'Instrumental Magnitude']
    mag = mag_column.values
    sp.asarray(mag)
    print(mag)
    magn_counter = 0
    mag = np.round(mag* 2.0)/2
    x =[]
    y=[]
    error = []
    y1=[]
    print(mag)
    while magn_counter < 20:
        euclid_num = 0.6 * magn_counter -6
        entries = np.count_nonzero(mag==magn_counter)
        if magn_counter < 15:
            error.append(0.434*(sp.sqrt(entries)/10))
        else:
            error.append(0)
        print(entries)
        
        y.append(entries)
        y1.append(euclid_num)
        x.append(magn_counter)
        magn_counter += 0.1
        magn_counter=np.round_(magn_counter,1)
        
    
    sp.asarray(x)
    sp.asarray(y)
    sp.asarray(y1)
    sp.asarray(error)
    plt.scatter(x,sp.log10(y))
    plt.plot(x,y1,color='r')
    plt.errorbar(x,sp.log10(y),yerr=error)
    plt.grid()
    plt.xlabel('Magnitude m')
    plt.ylabel('log[N(m)]')
    plt.ylim(-1, 4)
    plt.xlim(10,19)
    plt.show()
