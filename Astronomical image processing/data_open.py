# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 15:00:07 2021

@author: Tolbran
"""

from astropy.io import fits 
import scipy as sp

#Opens the data file


class DataGeneration:
    
    def __init__(self, hdulist=fits.open("data/A1_cropped_mosaic.fits")):
        self.hdulist = hdulist
        self.astro_flux = hdulist[0].data
        self.raw_data = []
        self.y_bottom_border = 119
        self.y_top_border =  4518
        self.x_left_border = 98
        self.x_right_border = 2476
        
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
        
    def crop_edges(self, old_data):
        
        '''
        This function crops the edges of the data. ie. it removes all the
        data between the ranges specified by the user. This shouldn't
        need to be used again as I have saved the cropped data as a
        fits file so can be used freely
        
        '''
        
        y_counter = len(old_data) - 1
        x_counter = len(old_data[0]) - 1
        sp.asarray(old_data)
        
        while y_counter != -1:
            if not (self.y_bottom_border <= y_counter <= self.y_top_border):
                #removes the whole rows froma 2D array
                old_data = sp.delete(old_data,y_counter,0)
            y_counter -=1
        
        while x_counter != -1:
            if not (self.x_left_border <= x_counter <= self.x_right_border):
                #removes the whole columns from a 2d array
                old_data = sp.delete(old_data,x_counter,1)
            x_counter -=1
                
        self.astro_flux = old_data
        
    def remove_blooming(self):
        
        
    

