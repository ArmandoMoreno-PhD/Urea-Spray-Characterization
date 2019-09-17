# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 22:34:24 2019

@author: BigBoss
"""

#%% Packages used for the image processing.

import os
import math
import pims
import skimage
import numpy             as np
import pandas            as pd
import matplotlib        as mpl
import matplotlib.pyplot as plt

#from skimage import morphology
from pylab   import *
from PIL     import Image
from skimage import morphology
from timeit  import default_timer as timer
#%%
mpl.rc('image', cmap='gray')


TestDir = 'O:\\2019_Perugia\\2019_UniPG\\MieScattering\\Bosch 8514448 AI 04'          #@CMT
TestDir = 'F:\\01_AEMGdocs\\AE_docs\\2019_UniPG\\MieScattering\\Bosch 8514448 AI 04'  #@Home

os.chdir(TestDir)

DirCont = os.listdir()
Idx = [i for i, s in enumerate(DirCont) if 'Scala' not in s]

for i in range(0,len(Idx)):
    #Background Average Image maker:
    os.chdir(DirCont[Idx[i]]+'\\Background/')
    BgCont = os.listdir()
    
    if not  os.path.isfile('ABg.tif'):
        BgIdx = [i for i, s in enumerate(BgCont) if '.tif' in s]
        
        for j in range(0,len(BgIdx)):
            if j == 0:
                ABg  = np.double(plt.imread(BgCont[BgIdx[j]]))
            else:
                ABg += np.double(plt.imread(BgCont[BgIdx[j]]))
                
        ABg = (ABg/len(BgIdx))/((2**16)-1)
        
        plt.imsave('ABg.tif',ABg)
    else:
        ABg = plt.imread('ABg.tif')
        ABg = ABg[:,:,0]/(2**8-1)
        
    os.chdir(TestDir)
    
    #Image Normalization, Subtraction and Normalization
    os.chdir(DirCont[Idx[i]]+'\\Spray/')
    
    SpCont = os.listdir()
    
    ImgIdx = [i for i, s in enumerate(SpCont) if '.tif' in s]
    
    All_Times = np.zeros((len(ImgIdx),))
    
    for j in range(0,len(ImgIdx)):
        All_Times[j] = int(SpCont[ImgIdx[j]][21:25])
        
    Times = np.unique(All_Times)
    
    for j in range(0,len(Times)):
        Time_Idx = [i for i,s in enumerate(SpCont) if str(int(Times[j])) in s and '.tif' in s]
        
        
        
        
        
        
    
    
        
    
    
    
    