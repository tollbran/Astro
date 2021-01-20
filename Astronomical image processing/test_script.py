# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 15:07:38 2021

@author: Tolbran
"""

import scipy as sp
import data_open as dataf
import histogram_gen as histo
import data_analysis as data_a
from astropy.io import fits 



# %% Test 1: testing the method that opens fits file and saves to 2D array.

#Pass condition: Flux value at (x,y) = (494,1604) = 3493. Should get this when array called at this positon.

dataFrame = dataf.DataGeneration(fits.open("data/A1_mosaic.fits"))

print(dataFrame.astro_flux[1603][493])

#Pass. Displays 3493, but must remeber to minus one due to array position

# %% Test 2: testing the method that takes a t2D array and coverts it to a 1D one.

#Pass condition: The array must be 1D and sorted. Maximum value in 2D array must be first of 1D

dataFrame = dataf.DataGeneration(fits.open("data/small_test_data.fits"))

dataFrame.convert_2d_1d()
print(sp.amax(dataFrame.astro_flux))
print(dataFrame.raw_data)

#Pass. Both displays 3686

# %% Test 3: testting function that crops the edge of the fits file.

#Pass condition when cropped by 20 pixels each side, the length of dataFrame.astro_flux[0] must decrease by 40

dataFrame = dataf.DataGeneration(fits.open("data/A1_mosaic.fits"))
print(len(dataFrame.astro_flux[0]))

dataFrame.crop_edges(20,2550,0,4611)

print(len(dataFrame.astro_flux[0]))

#Pass. Second 40 pixels less than other
# %% Test 4: testing method to remove a circular radius of data from the fits file.

#Pass condition: A circle of radius 10 at position (150,150) must be generated and values set to 1. Specifided in excel document.

dataFrame = dataf.DataGeneration(fits.open("data/small_test_data.fits"))

dataFrame.cover_circle('data/test_four_circle.xlsx')

hdu = fits.PrimaryHDU(dataFrame.astro_flux)
hdu.writeto('data/test_four_output.fits')

#Pass. Must bear in mind actual value is at (151,151) due to arrays starting at 0.
# %% Test 5: testing method to remove a rectangle of data from results.

#Pass condition: Must create a rectable of data at (100,100) with width and length 10. See in DS9

dataFrame = dataf.DataGeneration(fits.open("data/small_test_data.fits"))

x_inp_one = int(input('What is the 1st x coord?'))
x_inp_two = int(input('What is the distance between the next  x coord?'))
y_inp_one = int(input('What is the y coord?'))
y_inp_two = int(input('What is the distance between the next  y coord?'))
dataFrame.cover_rectangle((y_inp_one,x_inp_one),(y_inp_two,x_inp_two))

hdu = fits.PrimaryHDU(dataFrame.astro_flux)
hdu.writeto('data/test_five_output.fits')

#Pass. Shows above rectangle.
# %% Test 6: testing ability to create a mask with cropped data set as '1'.

#Pass condition: Must be same dimensions are orignal file, however just with all data set to '0' except circle specified in test 4.

dataFrame = dataf.DataGeneration(fits.open("data/A1_mosaic.fits"))
dataFrame.cover_circle('test_four_circle.xlsx')
dataFrame.fill_inital_mask()


hdu = fits.PrimaryHDU(dataFrame.mask)
hdu.writeto('data/test_six_output.fits')

#Pass this circle is seen.
# %% Test 7: Checking that when a pixel is marked on the mask (at cneter of appaeture), it is above a given threshold.

#Pass condition: Run the source detection algortih for small_test_data. Use the generated mask to individually check if each 1 spot has a flux value higher than threshold.

dataFrame = dataf.DataGeneration(fits.open("data/small_test_data.fits"))

apperture_radius = 2.1
no_std = 3

dataFrame.source_detection(apperture_radius,no_std)
  
print(dataFrame.apperture_points)
        

#Pass only fluxes above threshold are marked at center points for the appertures. Threshold is 3460
# %%Test 8: Testing if the mask prevents the system from visiting the data point again.

# %% Test 9: Ensure the system only checks flux values above a certain threshold. (in this case 3460)

'''
Pass condition: Check at last printed position the value of the flux at it. Since the raw_data list is sorted. 
All prior positions will be above this number threshold. Check at values on threshold and one higher to check fully.
'''
apperture_radius = 2.1
no_std = 3

dataFrame = dataf.DataGeneration(fits.open("data/small_test_data.fits"))

dataFrame.source_detection(apperture_radius,no_std)

position_test = input('What is the positon?')
print(dataFrame.raw_data[int(position_test)])

position_test = input('What is the positon?')
print(dataFrame.raw_data[int(position_test)])


# %% Test 10: Ensure the correct flux is calculated when the apperture is over the flux point.

'''
Pass condittion: On small test data there is one point at 3686 flux. Since background is set to 3430 for now. Set no_std to 25 for now. 
Thus this create one apperture in the image centered at (161,139). Manually adding up the radius 3 apperture gives, 47414, taking away background we get
2824. So must get this number.
'''

apperture_radius = 2.1
no_std = 25


dataFrame = dataf.DataGeneration(fits.open("data/small_test_data.fits"))

dataFrame.source_detection(apperture_radius,no_std)
print(dataFrame.sorted_data)
#Pass we do get the same number.
# %% Test 11: Ensure the system runs through all the nonvisted points and saves to excel file

'''
Pass condittion: Since we know that only points visted above a threshold are visted and the correct flux is stored.
The excel file must contain these positions and the flux value printed at each.
'''

apperture_radius = 2.1
no_std = 3


dataFrame = dataf.DataGeneration(fits.open("data/small_test_data.fits"))

dataFrame.source_detection(apperture_radius,no_std)
dataFrame.sorted_data
(dataFrame.sorted_data).to_excel("data/output_test_11.xlsx")  
#Pass all expected values are there.
# %% Test 12 A: Circular galaxy region

'''
Pass condittion: No condition as of yet. Aiming to see the general shape of the graph in these regions
'''
dataFrame = dataf.DataGeneration(fits.open("data/A1_edit_final.fits"))
print(len(dataFrame.astro_flux[0]))

dataFrame.crop_edges(1205,1574,956,1205)

hdu = fits.PrimaryHDU(dataFrame.astro_flux)
hdu.writeto('data/test_circle_galx.fits')

apperture_radius = 2.1
no_std = 3

dataFrame.source_detection(apperture_radius,no_std)
dataFrame.sorted_data
(dataFrame.sorted_data).to_excel("data/circle_gal_test.xlsx")  

data_a.magnitude_graph("data/circle_gal_test.xlsx")

#Graph shown in lab bookf fig.
# %% Test 12 B: A star region

'''
Pass condittion: No condition as of yet. Aiming to see the general shape of the graph in these regions
'''

dataFrame = dataf.DataGeneration(fits.open("data/A1_edit_final.fits"))
print(len(dataFrame.astro_flux[0]))

dataFrame.crop_edges(1691,1971,2380,2716)

hdu = fits.PrimaryHDU(dataFrame.astro_flux)
hdu.writeto('data/test_star_galx.fits')

apperture_radius = 2.1
no_std = 3

dataFrame.source_detection(apperture_radius,no_std)
dataFrame.sorted_data
(dataFrame.sorted_data).to_excel("data/star_galx_test.xlsx")  

data_a.magnitude_graph("data/star_galx_test.xlsx")

# %%

# %%