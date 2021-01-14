# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 15:00:07 2021

@author: Tolbran
"""

from astropy.io import fits 
import scipy as sp

#Opens the data file


class DataGeneration:
    
    def __init__(self, hdulist=fits.open("data/A1_mosaic.fits")):
        self.hdulist = hdulist
        self.astro_flux = hdulist[0].data
        self.raw_data = []
        
    def get_raw_data(self):
        
        return self.raw_data
    
    def convert_2d_1d (self,old_data):
    
        '''
        This function loops through a 2D array and takes each element of 
        it to store it in a 1D array for easier processing.
        '''
        new_data = []
        y_counter = 0
        
        while y_counter != len(old_data):
            x_counter = 0
            while x_counter != len(old_data[y_counter]):
                new_data.append(old_data[y_counter][x_counter])
                x_counter += 1
            
            y_counter +=1

        self.raw_data = new_data
        
    

