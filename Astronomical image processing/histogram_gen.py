# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:58:51 2021

@author: Tolbran
"""

import matplotlib.pyplot as plt
import scipy as sp

def gen_histogram(data):
    # the histogram of the data
    
    n, bins, patches = plt.hist(data, 20000, normed=1, facecolor='green', alpha=0.75)
    plt.xlabel('Flux')
    plt.ylabel('Probability of a pixel at a certain flux')
    plt.title('Histogram showing the probability of pixels at each flux')
    plt.grid(True)
    plt.axis([10000,40000, 0, 0.01])
    plt.show()
    