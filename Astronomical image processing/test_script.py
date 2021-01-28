# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 15:07:38 2021

@author: Tolbran
"""

import scipy as sp
from skimage.draw import circle
import data_open as dataf
import histogram_gen as histo
import random
import data_analysis as data_a
from astropy.io import fits 
import os


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
(dataFrame.sorted_data).to_excel("data/test/test11/sorted_data.xlsx")  
#Pass all expected values are there.
# %% Test 12 A: Circular galaxy region

'''
Pass condittion: No condition as of yet. Aiming to see the general shape of the graph in these regions
'''
dataFrame = dataf.DataGeneration(fits.open("data/A1_edit_final.fits"))
print(len(dataFrame.astro_flux[0]))

dataFrame.crop_edges(1205,1574,956,1205)

hdu = fits.PrimaryHDU(dataFrame.astro_flux)
hdu.writeto('data/test/test12A/data.fits')

apperture_radius = 2.1
no_std = 3

dataFrame.source_detection(apperture_radius,no_std)
dataFrame.sorted_data
(dataFrame.sorted_data).to_excel("data/test/test12A/sorted_data.xlsx")  

data_a.magnitude_graph("data/test/test12A/sorted_data.xlsx")

#Graph shown in lab bookf fig.
# %% Test 12 B: A star region

'''
Pass condittion: No condition as of yet. Aiming to see the general shape of the graph in these regions
'''

dataFrame = dataf.DataGeneration(fits.open("data/A1_edit_final.fits"))
print(len(dataFrame.astro_flux[0]))

dataFrame.crop_edges(1691,1971,2380,2716)

hdu = fits.PrimaryHDU(dataFrame.astro_flux)
hdu.writeto('data/test/test12B/data.fits')

apperture_radius = 2.1
no_std = 3

dataFrame.source_detection(apperture_radius,no_std)
dataFrame.sorted_data
(dataFrame.sorted_data).to_excel("data/test/test12B/sorted_data.xlsx")  

data_a.magnitude_graph("data/test/test12B/sorted_data.xlsx")

# %% Test 13:

apperture_radius = 4
no_std = 3


dataFrame = dataf.DataGeneration(fits.open("data/small_test_data.fits"))

dataFrame.source_detection(apperture_radius,no_std)
dataFrame.sorted_data
(dataFrame.sorted_data).to_excel("data/test/test13/sorted_data.xlsx")  
hdu = fits.PrimaryHDU(dataFrame.mask)
hdu.writeto('data/test/test13/mask.fits')

# %% Test 14: Summing up an artifically generated gaussian array correctly.


'''
Pass condittion: Flux value g from algorithm must equal to one manually summed.
'''

x, y = sp.meshgrid(sp.linspace(-1,1,50), sp.linspace(-1,1,50))
d = sp.sqrt(x*x+y*y)
sigma, mu = 1.0, 0.0
g = (sp.exp(-( (d-mu)**2 / ( 2.0 * sigma**2 ) ) ))*3600


hdu = fits.PrimaryHDU(g)
hdu.writeto('data/test/test14/file14.fits')

dataFrame = dataf.DataGeneration(fits.open("data/test/test14/file14.fits"))

no_std = 3
dataFrame.source_detection(no_std)

hdu = fits.PrimaryHDU(dataFrame.mask)
hdu.writeto('data/test/test14/maskfits')
dataFrame.sorted_data.to_excel("data/test/test14/sorted_data.xlsx")  

flux = 0
#print(dataFrame.apperture_points)

for point in dataFrame.apperture_points:
    #print('x: %d y: %d flux: %d' % (point[1]+1,point[0]+1,dataFrame.astro_flux[point[0]][point[1]]))
    flux += dataFrame.astro_flux[point[0]][point[1]]
    
print(dataFrame.apperture_size)
true_flux = flux - (dataFrame.apperture_size * 3420)
print('true flux value is: %d' %(true_flux))

#Pass all expected values are there.
#%% Test 15:Seeing which value of radius gives the best fit to equation (2) ie, gradient of 0.6

'''
Pass condittion: Combination which gets closet to 0.6 would 'in theory' (and I stress this) 
be the best fit to the simple equation (2)
'''

radius = 7
no_std = 3

dataFrame = dataf.DataGeneration(fits.open("data/A1_edit_final.fits"))
dataFrame.source_detection(no_std,radius)
(dataFrame.sorted_data).to_excel("data/test/test15/file_test%d.xlsx" % (radius))
data_a.magnitude_graph_cumu("data/test/test15/file_test%d.xlsx" % (radius))

# No result. Decided that trying to massage our results to find the best radius was not properly reflective of method.
# %% Test 16 A: testing apremade galaxy image with a known distribution. test A puts these gsources in a fixed regular positon


'''
Pass condittion: Should aim to expect a value of approx 0.6 if system works correctly.
'''

#gausian generation
x, y = sp.meshgrid(sp.linspace(-1,1,10), sp.linspace(-1,1,10))
d = sp.sqrt(x*x+y*y)
sigma, mu = 1.0, 0.0
g = (sp.exp(-( (d-mu)**2 / ( 2.0 * sigma**2 ) ) ))

#magnitudes to be generated in gaussian form
mag = sp.array([12,13,14,15,16])
flux = 10**((mag - 25.3)/-2.5)

files = sp.zeros((4000,2000))
counts = [4,16,63,250,1000]
 

x_pos=30
y_pos =30
mag_counter = 0
while mag_counter < len(counts):
    norm=0
    norm = sp.sum(g)
    g1 = (g*flux[mag_counter])/norm
    no_entries = 0
    while no_entries < counts[mag_counter]:
        y_counter = 0
        while y_counter < len(g1):
            x_counter = 0
            while x_counter < len(g1[0]):
                files[y_counter+y_pos][x_counter+x_pos] = g1[y_counter][x_counter]
                x_counter+=1
            y_counter +=1
        if x_pos < (len(files[0])-60):
            x_pos +=30
        else:
            x_pos = 30
            y_pos += 50
        no_entries += 1
        
    mag_counter +=1
    
files = files + 3420
#hdu = fits.PrimaryHDU(files)
#hdu.writeto('data/test/test16A/data.fits')


no_std = 3
dataFrame = dataf.DataGeneration(fits.open("data/test/test16A/data.fits"))
dataFrame.source_detection(no_std,10)
hdu = fits.PrimaryHDU(dataFrame.mask)
hdu.writeto('data/test/test16A/mask.fits')
(dataFrame.sorted_data).to_excel("data/test/test16A/sorted_data.xlsx")
data_a.magnitude_graph_cumu("data/test/test16A/sorted_data.xlsx")
#Pass get a result of approx 0.062, considering the shape of the source is square, this flucation is epxected.

#%% test 16 B: Scattering the sources at random

#gausian generation
x, y = sp.meshgrid(sp.linspace(-1,1,10), sp.linspace(-1,1,10))
d = sp.sqrt(x*x+y*y)
sigma, mu = 1.0, 0.0
g = (sp.exp(-( (d-mu)**2 / ( 2.0 * sigma**2 ) ) ))

#magnitudes to be generated in gaussian form
mag = sp.array([12,13,14,15,16])
flux = 10**((mag - 25.3)/-2.5)

files = sp.zeros((4000,2000))
counts = [4,16,63,250,1000]
 


mag_counter = 0
while mag_counter < len(counts):
    norm=0
    norm = sp.sum(g)
    g1 = (g*flux[mag_counter])/norm
    no_entries = 0
    while no_entries < counts[mag_counter]:
        y_counter = 0
        x_pos = random.randint(40,1960)
        y_pos = random.randint(40, 3960)
        while y_counter < len(g1):
            x_counter = 0
            while x_counter < len(g1[0]):
                files[y_counter+y_pos][x_counter+x_pos] = g1[y_counter][x_counter]
                x_counter+=1
            y_counter +=1
        no_entries += 1
        
    mag_counter +=1
    
files = files + 3420
hdu = fits.PrimaryHDU(files)
hdu.writeto('data/test/test16B/data.fits')


no_std = 3
dataFrame = dataf.DataGeneration(fits.open("data/test/test16B/data.fits"))
dataFrame.source_detection(no_std,10)
hdu = fits.PrimaryHDU(dataFrame.mask)
hdu.writeto('data/test/test16B/mask.fits')
(dataFrame.sorted_data).to_excel("data/test/test16B/sorted_data.xlsx")
data_a.magnitude_graph_cumu("data/test/test16B/sorted_data.xlsx")

#%% test 16 C: Scattering the sources at random with random radius

import scipy as sp
from skimage.draw import circle
import data_open as dataf
import histogram_gen as histo
import random
import data_analysis as data_a
from astropy.io import fits 
import os

#magnitudes to be generated in gaussian form
mag = sp.array([12,13,14,15,16])
flux = 10**((mag - 25.3)/-2.5)

files = sp.zeros((4000,2000))
counts = [4,16,63,250,1000]
 
def makeGaussian(size, fwhm, center=None):
    """ Make a square gaussian kernel.

    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.
    """

    x = sp.arange(0, size, 1, float)
    y = x[:,sp.newaxis]

    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]

    return sp.exp(-4*sp.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)

count = 0
gradient = []
while count < 50:
    mag = sp.array([12,13,14,15,16])
    flux = 10**((mag - 25.3)/-2.5)
    files = sp.zeros((4000,2000))
    counts = [4,16,63,250,1000]
    mag_counter = 0
    while mag_counter < len(counts):
        no_entries = 0
        while no_entries < counts[mag_counter]:
            norm=0
            y_counter = 0
            x_pos = random.randint(40,1960)
            y_pos = random.randint(40, 3960)
            radius = random.randint(6,20)
            #gausian generation
            #x = sp.linspace(-1,1,10)
            #y = sp.linspace(-1,1,10)
            #x1, y1 = sp.meshgrid(x, y)
            #d = sp.sqrt(x*x+y*y)
            g = makeGaussian(radius,(radius/2))
            norm = sp.sum(g)
            g1 = (g*flux[mag_counter])/norm
            while y_counter < len(g1):
                x_counter = 0           
                while x_counter < len(g1[0]):
                    files[y_counter+y_pos][x_counter+x_pos] = g1[y_counter][x_counter]
                    x_counter+=1
                y_counter +=1
            no_entries += 1
        mag_counter +=1
        
    files = files + 3420
    hdu = fits.PrimaryHDU(files)
    hdu.writeto('data/test/test16C/data%d.fits' % (count))
    
    
    no_std = 3
    dataFrame = dataf.DataGeneration(fits.open('data/test/test16C/data%d.fits' % (count)))
    dataFrame.source_detection(no_std,10)
    #hdu = fits.PrimaryHDU(dataFrame.mask)
    #hdu.writeto('data/test/test16C/mask.fits')
    (dataFrame.sorted_data).to_excel("data/test/test16C/file_test%d.xlsx" % (count))
    
    gradient.append(data_a.magnitude_graph_cumu("data/test/test16C/file_test%d.xlsx" % (count)))
    count +=1

grad = sp.asarray(gradient)
print(sp.mean(grad))
# %%
histo.gen_histogram(grad)