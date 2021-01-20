# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 13:41:31 2021

@author: Tolbran
"""
# %%
import numpy as np
import data_open as dataf
import histogram_gen as histo
import data_analysis as data_a
from astropy.io import fits 


# %%

dataFrame = dataf.DataGeneration(fits.open("data/A1_edit_final.fits"))


#dataFrame.remove_blooming(dataFrame.astro_flux)
#dataFrame.fill_mask()
#histo.gen_histogram(dataFrame.get_raw_data())

        
if input('Would you like to remove the specified data in the spreadsheet from your data? y/n :') == 'y':
    dataFrame.cover_circle('data/suns_remove.xlsx')
    dataFrame.crop_edges(400,600,1000,1200)

while input('Would you like to remove a bleeding effect? y/n') == 'y':
    x_inp_one = int(input('What is the 1st x coord?'))
    x_inp_two = int(input('What is the distance between the next  x coord?'))
    y_inp_one = int(input('What is the y coord?'))
    y_inp_two = int(input('What is the distance between the next  y coord?'))
    dataFrame.cover_rectangle((y_inp_one,x_inp_one),(y_inp_two,x_inp_two))

# %%
    
#Variables for you to set
apperture_radius = 2.1
no_std = 3

#dataFrame.crop_edges(0,2056,0,2000)

dataFrame.source_detection(apperture_radius,no_std)
hdu = fits.PrimaryHDU(dataFrame.mask)
hdu.writeto('mask.fits')
(dataFrame.sorted_data).to_excel("output_half.xlsx")  

# %%

data_a.magnitude_graph("output_half.xlsx")