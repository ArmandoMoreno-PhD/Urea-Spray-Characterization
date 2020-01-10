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

SameNP = True
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
        BgIdx = [k for k, s in enumerate(BgCont) if '.tif' in s and 'ABg' not in s]
        
        for j in range(0,len(BgIdx)):
            if j == 0:
                ABg  = np.double(plt.imread(BgCont[BgIdx[j]]))
            else:
                ABg += np.double(plt.imread(BgCont[BgIdx[j]]))
                
        ABg = (ABg/len(BgIdx))/((2**16)-1)
        
        plt.imsave('ABg.tif',ABg,)
    else:
        ABg = plt.imread('ABg.tif')
        ABg = ABg[:,:,0]/(2**8-1)
        
    os.chdir(TestDir)
    
    #Image Normalization & Subtraction
    os.chdir(DirCont[Idx[i]]+'\\Spray/')
    
    SpCont = os.listdir()
    
    
    #Extract time from Img names
    ImgIdx = [k for k, s in enumerate(SpCont) if '.tif' in s]
    All_Times = np.zeros((len(ImgIdx),))
    for j in range(0,len(ImgIdx)):
        All_Times[j] = int(SpCont[ImgIdx[j]][21:25])
        
    Times = np.unique(All_Times)
    
    for j in range(0,len(Times)):
        Time_Idx = [k for k,s in enumerate(SpCont) if str(int(Times[j])) in s and '.tif' in s]
        
        for k, Time in enumerate(Time_Idx):
            CurImg = np.double(plt.imread(SpCont[Time_Idx[k]]))/(2**16-1)
            CurImg = CurImg - ABg
            tsh    = skimage.filters.threshold_otsu(CurImg)
            CurImg = CurImg > tsh
            
            NozEx = False
            if not NozEx:
                
                if SameNP and j == 0:
                    if SameBG:
                        im = array(Image.open("ConfigImages\\Avg_Bg.tif"))
                    else:
                        im = array(Image.open(bg_Name[0])) 
                        
                    axs = plt.imshow(im)
                    plt.title('Select the nozzle position and the farthest point on the injectors axis')
                    
                    x = ginput(2)
                    print('you clicked:',x)
                    show()
                    close()
                    x = np.ceil(x)
                    x = np.array(x)
                    
                elif not SameNP:
                    
                    if SameBG:
                        im = array(Image.open("ConfigImages\\Avg_Bg.tif"))
                    else:
                        im = array(Image.open(bg_Name[0])) 
                        
                    axs = plt.imshow(im)
                    plt.title('Select the nozzle position and the farthest point on the injectors axis')
                    
                    x = ginput(2)
                    print('you clicked:',x)
                    show()
                    close()
                    x = np.ceil(x)
                    x = np.array(x)
                
            
            
            
            
        
        
        
        
        
        
    
    
        
    
    
    
    