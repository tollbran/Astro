# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 13:41:31 2021

@author: Tolbran
"""
import data_open as dataf
import histogram_gen as histo

dataFrame = dataf.DataGeneration()
dataFrame.convert_2d_1d(dataFrame.astro_flux)

histo.gen_histogram(dataFrame.get_raw_data())
