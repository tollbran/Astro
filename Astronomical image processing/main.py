# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 13:41:31 2021

@author: Tolbran

This is the main module to be run when wanting to analyse the data.
Dependencies: Astropy, Skimage, Scipy/numpy, Matplotlib
"""
# %% Intial imports
import numpy as np
import data_open as dataf
import histogram_gen as histo
import data_analysis as data_a
from astropy.io import fits 


# %% Run this to generates dataFrame
dataFrame = dataf.DataGeneration(fits.open('data/A1_edit_final_V1.fits'))


# %% Generates a histogram of background pixels
dataFrame.convert_2d_1d()
histo.gen_histogram(dataFrame.get_raw_data())
#%% Editing
        
if input('Would you like to remove the specified data in the spreadsheet from your data? y/n :') == 'y':
    dataFrame.cover_circle('data/file_1.xlsx')

if input('Would you like ro crop edges? y/n:') == 'y':
    dataFrame.crop_edges(0,2000,0,2000)
    
while input('Would you like to remove a bleeding effect? y/n') == 'y':
    x_inp_one = int(input('What is the 1st x coord?'))
    x_inp_two = int(input('What is the distance between the next  x coord?'))
    y_inp_one = int(input('What is the y coord?'))
    y_inp_two = int(input('What is the distance between the next  y coord?'))
    dataFrame.cover_rectangle((y_inp_one,x_inp_one),(y_inp_two,x_inp_two))

hdu = fits.PrimaryHDU(dataFrame.astro_flux)
hdu.writeto('data/file.fits')
# %% Main
     
#Variables for you to set
no_std = 5

dataFrame = dataf.DataGeneration(fits.open("data/A1_edit_final_v1.fits"))

dataFrame.source_detection(no_std)
hdu = fits.PrimaryHDU(dataFrame.mask)
hdu.writeto('data/test/filemask.fits')
(dataFrame.sorted_data).to_excel("data/test/file_plot5.xlsx")  

# %% Analaysis

answer = input('Which graph would you like to see? All three cumulative plots: c One cumulative plot d? Type c or d ')

if answer == 'd':
    data_a.magnitude_graph_cumu("data/test/file_plot4.xlsx")
elif answer == 'c':
    data_a.magnitude_graph_cumu3("data/test/file_plot3.xlsx","data/test/file_plot4.xlsx","data/test/file_plot5.xlsx")

#%%
data_a.magnitude_graph_cumu("data/test/file_plot5.xlsx")
