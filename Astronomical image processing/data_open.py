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
        self.sorted_data = pd.DataFrame(columns=['Flux value','Instrumental Magnitude','x position','y position','Apperture radius'])
        #Set for cropping a image could remove these
        self.threshold = 6000 # cut off for deleting data
        self.background_flux = 3420 # settting it to this for now
        self.standard_error = 13
        self.apperture_size = 0
        
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
        
            
    def source_detection(self,no_std,app_radius):
        
        '''
        Goes through a 1d array storing all the fluxes in the image in order. Finds the position of these fluxes in the file.
        Checks through each position if it has been checked. if it hasn't places a circular apperture of a variable radius over it
        All fluxes in the apperture are added up and stored.
        '''
        
        self.fill_inital_mask()
        self.convert_2d_1d()
        
        entries =0
        #Used to center the circular apperture in its own 2d array
        
        while self.raw_data[0] > (self.background_flux + no_std*self.standard_error):
            circ_center_val = self.raw_data[0]
            circ_center_pos = sp.where(self.astro_flux==circ_center_val)
            #Sets the center of the detector apperture to the first set of co-ordinates at that flux
            checker = 0
            while checker < len(circ_center_pos[0]):
                x_cord = circ_center_pos[1][checker]
                y_cord = circ_center_pos[0][checker] 
                flux_value = 0
                radius = 0
                if 20 < y_cord < (len(self.astro_flux) -20): #Checking that we arent selecting items close to the border
                    if 20 < x_cord < (len(self.astro_flux[0])-20):
                        if self.mask[y_cord][x_cord] == 0: #Check if already been sorted 0 if no
                            current_flux = (self.astro_flux[y_cord][x_cord])
                            while current_flux > (self.background_flux + 0.5*self.standard_error):
                                #Loops until we reach the background flux level
                                if ((x_cord + radius) == len(self.astro_flux[0]-1)):
                                    current_flux = 1 #Breakout clause for now
                                else:
                                    current_flux = self.astro_flux[(y_cord+radius)][(x_cord + radius)]
                                    radius+=1                       
                            #print('Flux: %d, positon x: %d y: %d' %(self.astro_flux[y_cord][x_cord],(x_cord+1),(y_cord+1)))
                            #Used to create a big enough array to store the apperture.
                            rr_apperture, cc_apperture = circle(radius,radius,radius)
                            #Creates a circle with radius and centered at twice the radius
                            apperture = sp.zeros((2*radius,2*radius))
                            apperture[rr_apperture,cc_apperture] = 1
                            #Finds the no of pixels that will be added together
                            apperture_pixel_size = len(sp.where(apperture==1)[0])
                            y_counter = 0
                            #Starting in the top corner of the array
                            x_scan_start = x_cord - radius
                            y_scan_start = y_cord + radius
                            #Sets the start points in the data file for the 'scan'
                            if x_scan_start < len(self.astro_flux[0]):
                                while y_counter < len(apperture):
                                    x_counter = 0
                                    x_scan_start = x_cord - radius
                                    while x_counter < len(apperture[0]):
                                        if apperture[y_counter][x_counter]==1:
                                            if self.astro_flux[y_scan_start][x_scan_start] ==1:
                                                current_pixel = self.background_flux + (random.random()*self.standard_error)
                                            else:
                                                current_pixel = self.astro_flux[y_scan_start][x_scan_start]
                                            flux_value += current_pixel
                                            self.apperture_points.append([y_scan_start,x_scan_start])
                                        
                                        #print('Flux value: %d' % (flux_value))
                                        x_counter +=1
                                        x_scan_start +=1
                                        #print('Flux: %d, positon x: %d y: %d' %(self.astro_flux[y_scan_start][x_scan_start],x_scan_start+1,y_scan_start+1))
                                        
                                    y_counter+=1
                                    y_scan_start -=1
                                #print('Apperture size: %d Pixel Count: %d' % (apperture_pixel_size,pixel_count))
                                #Sets the start points in the data file for the 'scan')
                                #Finds background flux
                                self.apperture_size = apperture_pixel_size
                                average_flux = (flux_value - (apperture_pixel_size * self.background_flux))
                                if radius > 0:
                                    if average_flux > 0:
                                        #Removing fluctuations
                                        mag = -2.5*sp.log10(average_flux) +25.3
                                        #Stores the data in a panda dataframe.
                                        self.sorted_data.loc[-1] =  [average_flux,mag,x_cord+1,y_cord+1,radius]
                                        self.sorted_data.index =  self.sorted_data.index + 1  
                                        self.sorted_data =  self.sorted_data.sort_index()
                                        entries +=1
                                        #Creates a circle in the mask to show that have been delt with
                                rr, cc = circle(y_cord,x_cord,radius)
                                self.mask[rr,cc] = 1
                                print("x: %d, y: %d entires: %d Position: %d" % (x_cord+1,y_cord+1,entries,self.raw_data[0]))
            
                checker += 1
            self.raw_data = sp.delete(self.raw_data, sp.where(self.raw_data == self.raw_data[0]))
   
            
            

            
        
    

