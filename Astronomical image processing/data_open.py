# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 15:00:07 2021

@author: Tolbran
"""

from astropy.io import fits 
import scipy as sp
from skimage.draw import circle
from skimage.draw import rectangle
import pandas as pd
import random
#Opens the data file


class DataGeneration:
    
    def __init__(self, hdulist):
        self.hdulist = hdulist
        self.astro_flux = hdulist[0].data
        self.raw_data = []
        self.apperture_points = []
        self.mask = sp.zeros((len(self.astro_flux),len(self.astro_flux[0])), dtype=int)
        self.sorted_data = pd.DataFrame(columns=['Flux value','x position','y position'])
        #Set for cropping a image could remove these
        self.threshold = 6000 # cut off for deleting data
        self.background_flux = 3430 # settting it to this for now
        self.standard_error = 10
        
    def get_raw_data(self):
        
        return self.raw_data
    
    def convert_2d_1d (self):
    
        '''
        This function loops through a 2D array and takes each element of 
        it to store it in a 1D array for easier processing.
        '''
        new_data = []
        y_counter = 0
        
        while y_counter != len(self.astro_flux):
            x_counter = 0
            while x_counter != len(self.astro_flux[y_counter]):
                new_data.append(self.astro_flux[y_counter][x_counter])
                x_counter += 1
            
            y_counter +=1
        sp.asarray(new_data)
        new_data = sp.sort(new_data)[::-1]
        self.raw_data = new_data
        
    def crop_edges(self, x_left_border,x_right_border,y_bottom_border,y_top_border):
        
        '''
        This function crops the edges of the data. ie. it removes all the
        data between the ranges specified by the user. This shouldn't
        need to be used again as I have saved the cropped data as a
        fits file so can be used freely
        
        '''
        old_data = self.astro_flux
        y_counter = len(old_data) - 1
        x_counter = len(old_data[0]) - 1
        sp.asarray(old_data)
        
        while y_counter != -1:
            if not (y_bottom_border <= y_counter < y_top_border):
                #removes the whole rows froma 2D array
                old_data = sp.delete(old_data,y_counter,0)
            y_counter -=1
        
        while x_counter != -1:
            if not (x_left_border <= x_counter < x_right_border):
                #removes the whole columns from a 2d array
                old_data = sp.delete(old_data,x_counter,1)
            x_counter -=1
                
        self.astro_flux = old_data
        
    def cover_circle(self,excel_file):
        '''
        Function removes a specified region of the data.
        Use to remove the bright suns.
        ''' 
        
        sun_data = pd.read_excel(excel_file)
        
        counter = 0
        
        while counter != len(sun_data['x-pos']):
            x_pos = sun_data['x-pos'][counter]
            y_pos = sun_data['y-pos'][counter]
            #Imposes a circular apperture over the data to be removed
            circ = sun_data['circumference'][counter]
            rr, cc = circle(y_pos, x_pos, circ)
            self.astro_flux[rr, cc] = 1
            counter +=1
            
    def cover_rectangle(self,start,end):
        '''
        Function removes a specified rectangle region of the data.
        Use to remove the bleeding effects.
        '''
        
        rr, cc = rectangle(start, extent=end)
        self.astro_flux[rr, cc] = 1

            
    def fill_inital_mask(self):
        
        '''
        Creates a 2d array full of 0, sets the removed data areas to 1
        initally so the system does not coutn these.
        '''
        
        y_counter = 0
        while y_counter != len(self.astro_flux):
            x_counter = 0
            while x_counter != len(self.astro_flux[y_counter]):
                if self.astro_flux[y_counter][x_counter] == 1:
                    #imposes already check mark on the mask
                    self.mask[y_counter][x_counter] = 1
                x_counter += 1
            
            y_counter +=1
            
    def source_detection(self,apperture_radius, no_std):
        
        '''
        Goes through a !d array storing all the fluxes in the image in order. Finds the position of these fluxes in the file.
        Checks through each position if it has been checked. if it hasn't places a circular apperture of a variable radius over it
        All fluxes in the apperture are added up and stored.
        '''
        
        self.fill_inital_mask()
        self.convert_2d_1d()
        
        position = 0
        center_apperture = 4
        #Used to center the circular apperture in its own 2d array
        
        while self.raw_data[position] > (self.background_flux + no_std*self.standard_error):
            circ_center_val = self.raw_data[position]
            circ_center_pos = sp.where(self.astro_flux==circ_center_val)
            checker = 0
            while checker < len(circ_center_pos[0]):
                rr_apperture, cc_apperture = circle(center_apperture,center_apperture,apperture_radius)
                apperture = sp.zeros((10,10))
                apperture[rr_apperture,cc_apperture] = 1
                apperture_pixel_size = len(sp.where(apperture==1)[0])
                y_cord = circ_center_pos[1][checker]
                x_cord = circ_center_pos[0][checker]
                flux_value = 0
                if 20 < x_cord < (len(self.astro_flux) -20): #4113
                    if 20 < y_cord < (len(self.astro_flux[0])-20):
                        if self.mask[x_cord][y_cord] == 0:
                            #checking not already been counted
                            y_counter = 0
                            x_scan_start = x_cord - center_apperture
                            y_scan_start = y_cord + center_apperture
                            #Sets the start points in the data file for the 'scan'
                            
                            while y_counter < len(apperture):
                                x_counter = 0
                                x_scan_start = x_cord - center_apperture
                                while x_counter < len(apperture[0]):
                                    if apperture[y_counter][x_counter]==1:
                                        if self.astro_flux[x_scan_start][y_scan_start] ==1:
                                            flux_value += self.background_flux + (random.random()*self.standard_error)
                                        flux_value += self.astro_flux[x_scan_start][y_scan_start]
                                        
                                    x_counter +=1
                                    x_scan_start +=1
                                    
                                y_counter+=1
                                y_scan_start -=1
                            
                            average_flux = flux_value - (apperture_pixel_size * self.background_flux)
                            #Stores the data in a panda dataframe.
                            self.sorted_data.loc[-1] =  [average_flux,x_cord,y_cord]
                            self.sorted_data.index =  self.sorted_data.index + 1  
                            self.sorted_data =  self.sorted_data.sort_index()
                            #Creates a circle in the mask to show that have been delt with
                            rr, cc = circle(x_cord,y_cord,apperture_radius)
                            self.mask[rr,cc] = 1
                            self.apperture_points.append(self.raw_data[position])
                            
                checker += 1
            print(self.raw_data[position])
            print("Position is: %d " % (position))
            position += 1
            
            
            
            
        
    

