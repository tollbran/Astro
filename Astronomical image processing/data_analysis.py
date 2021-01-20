# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:13:35 2021

@author: Tolbran
"""

import matplotlib.pyplot as plt
import scipy as sp
import pandas as pd

def magnitude_graph(excel_file):
    data = pd.read_excel(excel_file)
    fluxes_column = data.loc[:,'Flux value']
    fluxes= fluxes_column.values
    sp.asarray(fluxes)
    mag = -2.5*sp.log10(fluxes)
    inst_mag = mag + 25.3
    print(inst_mag)
    magn_counter = 0
    x =[]
    y=[]
    y1=[]
    while magn_counter < 20:
        number_count = sp.count_nonzero(inst_mag < magn_counter)
        x.append(magn_counter)
        y.append(sp.log10(number_count))
        euclid_num = 0.6*magn_counter
        y1.append(euclid_num)
        magn_counter += 0.5
    
    sp.asarray(x)
    sp.asarray(y)
    sp.asarray(y1)
    plt.scatter(x,y)
    plt.grid()
    plt.xlabel('Magnitude')
    plt.ylabel('Log of number of counts above this magnitude')
    plt.ylim(-3, 6)
    plt.show()

    #plt.plot(x,sp.log10(y1))