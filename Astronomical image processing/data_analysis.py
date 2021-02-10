# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:13:35 2021

@author: Tolbran
"""

import matplotlib.pyplot as plt
import scipy as sp
import pandas as pd
import numpy as np
import seaborn as sns

def magnitude_graph_cumu(excel_file):
    data = pd.read_excel(excel_file)
    mag_column = data.loc[:,'Instrumental Magnitude']
    mag = mag_column.values
    sp.asarray(mag)
    print(mag)
    magn_counter = 0
    x =[]
    y=[]
    error = []
    y_fit=[]
    x_fit = []
    while magn_counter < 20:
        
        number_count = sp.count_nonzero(mag < magn_counter)
        x.append(magn_counter)
        y.append(sp.log10(number_count))
        if 13 <= magn_counter <= 16: 
            x_fit.append(magn_counter)
            y_fit.append(sp.log10(number_count))
        
        #simple poisson statistics for now
        error.append(sp.log10(sp.sqrt(number_count)))
        #euclid_num = 0.6*magn_counter - 7.5
        magn_counter += 1
    
    error_up3 = sp.array([0,0,0,0,0,0,0,0,0,0,0,0.10,0.061,0.038,0.023,0.015,0.010,0.006,0.003,0.0015])
    error_down3=sp.array([0,0,0,0,0,0,0,0,0,0,0,0.13,0.071,0.041,0.0245,0.0160,0.0104,0.0064,0.0032,0.0015])
    error_up4 = sp.array([0,0,0,0,0,0,0,0,0,0,0,0.11,0.063,0.04,0.024,0.0168,0.011,0.006,0.002,0.0007])
    error_down4=sp.array([0,0,0,0,0,0,0,0,0,0,0,0.148,0.078,0.045,0.0269,0.0168,0.011,0.0055,0.002,0.001])
    error3 = [error_down3,error_up3]
    error4 = [error_down4,error_up4]
    
    fit,cov =sp.polyfit(x_fit,y_fit,deg=1,w=1/sp.array([0.045,0.0269,0.0168,0.011]),cov=True) 
    func = sp.poly1d(fit)
    sp.asarray(x)
    sp.asarray(y)
    sp.asarray(x_fit)
    sp.asarray(y_fit)
    sp.asarray(error)
    plt.scatter(x,y,color='k',marker='x')
    plt.plot(x_fit,func(x_fit),color='r',ls='--')
    plt.errorbar(x,y,yerr=error4,capsize=2, elinewidth=0.5,fmt='.g')
    plt.grid()
    plt.xlabel('Magnitude')
    plt.ylabel('log(N(<m))')
    plt.ylim(0, 4)
    plt.xlim(10, 20)
    plt.show()
    print('Slope = %.3e Error = %.3e' %(fit[0],cov[0,0]))
    return fit[0]
    
def magnitude_graph_cumu3(excel_file1,excel_file2,excel_file3):
    data1 = pd.read_excel(excel_file1)
    data2 = pd.read_excel(excel_file2)
    data3 = pd.read_excel(excel_file3)
    mag_column1 = data1.loc[:,'Instrumental Magnitude']
    mag1 = mag_column1.values
    sp.asarray(mag1)
    mag_column2 = data2.loc[:,'Instrumental Magnitude']
    mag2 = mag_column2.values
    sp.asarray(mag2)
    mag_column3 = data3.loc[:,'Instrumental Magnitude']
    mag3 = mag_column3.values
    sp.asarray(mag3)
    magn_counter = 0
    x =[]
    xerr=sp.array([11,12,13,14,15,16,17,18,20])
    y1=[]
    y2=[]
    y3=[]
    yline=[]

    y_fit1=[]
    y_fit2=[]
    y_fit3=[]
    x_fit = []
    while magn_counter < 20:
        number_count1 = sp.count_nonzero(mag1 < magn_counter)
        number_count2 = sp.count_nonzero(mag2 < magn_counter)
        number_count3 = sp.count_nonzero(mag3 < magn_counter)
        x.append(magn_counter)
        y1.append(sp.log10(number_count1))
        y2.append(sp.log10(number_count2))
        y3.append(sp.log10(number_count3))
        if 13 <= magn_counter <= 17: 
            x_fit.append(magn_counter)
            y_fit1.append(sp.log10(number_count1))
            y_fit2.append(sp.log10(number_count2))
            y_fit3.append(sp.log10(number_count3))
        #simple poisson statistics for now
        #error.append(sp.log10(sp.sqrt(number_count)))
        euclid_num = 0.6*magn_counter - 5.5
        yline.append(euclid_num)
        magn_counter += 1
    
    fit1,cov1 =sp.polyfit(x_fit,y_fit1,deg=1,w=[1,1,1,1,1],cov=True) 
    func1 = sp.poly1d(fit1)

    sp.asarray(x)
    sp.asarray(y1)
    sp.asarray(y2)
    sp.asarray(y3)
    sp.asarray(x_fit)
    sp.asarray(y_fit1)
    sp.asarray(y_fit2)
    sp.asarray(y_fit3)
    sp.asarray(yline)
    error_up3 = sp.array([0,0,0,0,0,0,0,0,0,0,0,0.10,0.061,0.038,0.023,0.015,0.010,0.006,0.003,0.0015])
    error_down3=sp.array([0,0,0,0,0,0,0,0,0,0,0,0.13,0.071,0.041,0.0245,0.0160,0.0104,0.0064,0.0032,0.0015])
    error_up4 = sp.array([0,0,0,0,0,0,0,0,0,0,0,0.11,0.063,0.04,0.024,0.0168,0.011,0.006,0.002,0.0007])
    error_down4=sp.array([0,0,0,0,0,0,0,0,0,0,0,0.148,0.078,0.045,0.0269,0.0168,0.011,0.0055,0.002,0.001])
    error_up5 = sp.array([0,0,0,0,0,0,0,0,0,0,0,0.11,0.066,0.042,0.025,0.0165,0.01,0.0045,0.0013,0.0005])
    error_down5=sp.array([0,0,0,0,0,0,0,0,0,0,0,0.147,0.078,0.046,0.0268,0.0172,0.0102,0.0046,0.0013,0.0005])
    error3 = [error_down3,error_up3]
    error4 = [error_down4,error_up4]
    error5 = [error_down5,error_up5]
    
    #fig, axs = plt.subplots(1, 3,sharey=True)
    #plt.scatter(x,y1,marker='^',color='b',alpha=0.5)
    plt.errorbar(x,y1,yerr=error3,capsize=2, elinewidth=0.5,fmt='.b')
    plt.ylim(0.5,4)
    plt.xlim(10,20)
    plt.ylabel('log(N(<m))')
    plt.xlabel('Calibrated magnitude')
    plt.grid()
    #plt.scatter(x,y2,marker='o',color='g',alpha=0.5)
    plt.errorbar(x,y2,yerr=error4,capsize=2, elinewidth=0.5,fmt='.g')
    #plt.scatter(x,y3,marker='s',color='r',alpha=0.5)
    plt.errorbar(x,y3,yerr=error5,capsize=2, elinewidth=0.5,fmt='.r')
    plt.legend(['3σ threshold','4σ threshold','5σ threshold'],loc=4)
    plt.show()
    #print('Slope = %.3e' %(fit[0]))
    #return fit[0]

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
