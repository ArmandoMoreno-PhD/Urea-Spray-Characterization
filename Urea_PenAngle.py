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

TestDir = 'F:\\01_AEMGdocs\\AE_docs\\2019_UniPG\\MieScattering\\Bosch 8514448 AI 04' 
os.chdir(TestDir)

DirCont = os.listdir()
Idx = [i for i, s in enumerate(DirCont) if 'Scala' not in s]

for i in range(0,len(Idx)):
    
    os.chdir(DirCont[i]+'\\Background/')
    BgCont = os.listdir()
    BgIdx = [i for i, s in enumerate(BgCont) if '.tif' in s]
    
    for j in range(0,len(BgIdx)):
        plt.imread(BgCont[BgIdx[j]])
        
    
    
    
    