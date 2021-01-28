# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:58:51 2021

@author: Tolbran
"""

import matplotlib.pyplot as plt
import scipy as sp
from scipy.stats import norm
import seaborn as sns

def gen_histogram(data):
    # the histogram of the data
    #data_fit = sp.delete(data,sp.where(data==1))
    #data_fit = sp.delete(data_fit,sp.where(data_fit > 3500))
    #n, bins, patches = plt.hist(data, 15, facecolor='green', alpha=0.75)
    sns.distplot(data,kde=False)
    plt.ylabel('Number count')
    plt.xlabel('Gradient')
    plt.grid(True)
    plt.axis([0.53,0.61, 0, 18])
    #mu, std = norm.fit(data_fit)
    #x = sp.linspace(min(data_fit), 3500, 1000)
    #p = norm.pdf(x, mu, std)
    #plt.plot(x, p, 'k', linewidth=2)
    plt.show()
    #print(("mean value: %d STD: %d" % (mu,std)))
    