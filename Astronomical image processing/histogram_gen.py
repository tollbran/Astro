# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:58:51 2021

@author: Tolbran
"""

import matplotlib.pyplot as plt
import scipy as sp
from scipy.stats import norm

def gen_histogram(data):
    # the histogram of the data
    data_fit = sp.delete(data,sp.where(data==1))
    data_fit = sp.delete(data_fit,sp.where(data_fit > 3500))
    n, bins, patches = plt.hist(data, 10000, normed=1, facecolor='green', alpha=0.75)
    plt.xlabel('Flux')
    plt.ylabel('Probability of a pixel at a certain flux')
    plt.title('Histogram showing the probability of pixels at each flux')
    plt.grid(True)
    plt.axis([3000,4000, 0, 0.04])
    mu, std = norm.fit(data_fit)
    x = sp.linspace(min(data_fit), 3500, 1000)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    plt.show()
    print(("mean value: %d STD: %d" % (mu,std)))
    