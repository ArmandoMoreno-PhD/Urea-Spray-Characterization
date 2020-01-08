# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:36:57 2019

@author: Armando Moreno.
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
#%%Basic image settings for grayscale
mpl.rc('image', cmap='gray')

#%% Options
#Test Directory
TestsDir = 'F:\\01_AEMGdocs\\AE_docs\\2019_UniPG\\SchilierenSlicer'
#Background range
br_i = 0
br_e = 15 
#Same Background for vids
SameBG = True
#Same Nozzle Position
SameNP = True
#Mask Angle
Mask_Angle = 20
#Save images for comparison
SaveIMG = False

#%%Identify all the .cine files inside the test folder
start = timer()
os.chdir(TestsDir)

DirCont = os.listdir()
Idx = [i for i, s in enumerate(DirCont) if os.path.isfile(DirCont[i]) and '.cine' in DirCont[i]]

for i in range(0,len(Idx)):
    
    #Reading the Video in .Cine:
    Vid = pims.Cine(DirCont[Idx[i]])
    
    #Transformation into a numpy array in dorder to work easier with the frames:
    Vid1 = np.double(np.array(Vid))
    
    end = timer()
    print(end-start) 
    #%% 
    start = timer()
    #Background calculation averaging the first n frames without spray:
    
    if SameBG and i == 0:
        
        b = np.mean(Vid1[br_i:br_e],axis =0)
                
        if not os.path.exists('ConfigImages'):
            os.mkdir('ConfigImages')
            
        plt.imsave("ConfigImages\\Avg_Bg.tif",b)
        
    elif not SameBG:
        
        b = np.mean(Vid1[br_i:br_e],axis =0)
                
        if not os.path.exists('ConfigImages'):
            os.mkdir('ConfigImages')
            
        bg_mov  = DirCont[Idx[i]].replace('.cine','')
        bg_Name = ["ConfigImages\\"+ bg_mov +'.tif']
        
        plt.imsave(bg_Name[0],b)

    end = timer()
    print(end-start)                 
    #%% 
    start = timer()
    #Defining nozzle outlet position and furthest penetration point
    
    if SameNP and i == 0:
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
        
    end = timer()
    print(end-start)             
    #%%
    start = timer()
    #Creation of a mask to facilitate the countour detecting:
    
    forma = np.array(Vid1.shape)                    #Extratcs the shape of each frame
    Mask = np.zeros([forma[1],forma[2]])            #Matrix of zeroes
    
    Angle = Mask_Angle                              #Angle (in degrees) from the nozzle exit where the spry is contained
    
    origen = [x[0][1],x[0][0]]                      #Point where the Nozzle exit is
    final  = [x[1][1],x[1][0]]                      #Furthest point to measure the spray penetration
    
    Opening = math.tan(math.radians(Angle/2))       
    
    for j in range(0,int(final[0])):                # Loop that creates the mask
        
        COP = Opening*j
        
        if not (abs(int(origen[1])-int(math.ceil(COP)))  <= 0) or not (abs(int(origen[1])+int(math.ceil(COP))) >= forma[2]):
            
            Mask[j,int(origen[1])-int(math.ceil(COP)):int(origen[1])+int(math.ceil(COP))]=1
        
        else:
            
            Mask[j:,:] = 1
            break

    end = timer()
    print(end-start)         
    #%%
    #DataFrame setup   
    Flag = None
    ContourData = None
    #%%
    start = timer()
    #Beggining of the contour detection algorithm:
    for k in range(0,len(Vid1)):
        
        a = Vid1[k].copy()              #Creation of a copy of the current frame
        Img = (b-a)*Mask                #Background subtraction
        
        Img1 = Img.copy()
        LowerZero = Img1 < 0            #Eliminating the values that are below 0
        Img1[LowerZero] = 0
    
        dynthr = 0.10                   #Defining the dynamic threshold value
        Thr = (Img1.max()-Img1.min())*dynthr+Img1.min()
        
        ThrLow = Img1 < Thr             #Thresholding to binarize the image
        ThrHigh = Img1 >= Thr     
        Img1[ThrHigh] = 1
        Img1[ThrLow] = 0
        
        if k<=20:                       #Erosion-Dilation cycles to remove small particles and smooth the contour
            Img2 = skimage.morphology.opening(Img1)
            Img3 = skimage.morphology.closing(Img2)
        else:
            Img2 = skimage.morphology.opening(Img1)
            Img3 = skimage.morphology.closing(Img2)
            Img2 = skimage.morphology.opening(Img3)
            Img3 = skimage.morphology.closing(Img2)
    
        

        
        labelImg = skimage.morphology.label(Img3)
        Regions = skimage.measure.regionprops(labelImg, cache = False)
        
        if k <= 20:
            for j in range(len(Regions)):
                if Regions[j].centroid[0]-origen[0]>30 or Regions[j].area < 15:
                    Img3[labelImg == Regions[j].label] = 0      #Finds the regions in the initial moments that are to far away from the nozzle to be considered spray.
        elif k > 20:
            labels = [Regions[j].label for j in range(0,len(Regions)) if Regions[j].area <= 100] 
            for j in range(0,len(labels)):
                 Img3[labelImg == labels[j]] = 0                                      
         
        if SaveIMG:
            plt.subplot(141)
            plt.imshow(Img)
            plt.subplot(142)
            plt.imshow(Img1)
            plt.subplot(143)
            plt.imshow(Img2)
            plt.subplot(144)
            plt.imshow(Img3)           
        
        contours = skimage.measure.find_contours(Img3,0.8)
                
        lista = [len(contours[m]) for m,n in enumerate(contours)]
        
        if contours:
            lc = lista.index(max(lista))
            
            if SaveIMG:
                plt.plot(contours[lc][:, 1], contours[lc][:, 0], linewidth=2)    
                plt.subplot(141)
                plt.plot(contours[lc][:, 1], contours[lc][:, 0], linewidth=2)
        else:
            lc = 'NC'
            contours = np.empty((1,2))
            contours.fill(np.nan)
         
        Instants  = ["{0:03}".format(p) for p in range(1,len(Vid1)+1)]
        ImgName   = ['Instant_'+Instants[k]+'.tif']
        FrameName = ['Frame_'+Instants[k]]
        
        if not tuple(ContourData) in locals():
            ContourData  = pd.DataFrame(contours,columns=[np.array([FrameName[0],FrameName[0]]),np.array(['y','x'])])
        elif lc == 'NC': 
            Currentcont  = pd.DataFrame(contours,columns=[np.array([FrameName[0],FrameName[0]]),np.array(['y','x'])])
            ContourData  = pd.concat([ContourData,Currentcont],axis=1)
        else:        
            Currentcont = pd.DataFrame(contours[lc],columns=[np.array([FrameName[0],FrameName[0]]),np.array(['y','x'])]) 
            ContourData  = pd.concat([ContourData,Currentcont],axis=1)
        
        if SaveIMG:
            plt.savefig(ImgName[0])
            #close()
            plt.clf()
            contours    = None
            
        Currentcont = pd.DataFrame()
        
    end = timer()
    print(end-start)         
    #%%    
    ContourData.to_csv('ContourData.csv',sep=',')  
    #%% Penetation and Angle Calculations
    Frames = list(ContourData.columns.levels[0])
    
    for i in range(0,len(Frames)):
         
        #Furthest
        Xdata = ContourData[Frames[i]]['x'][:].dropna(axis = 0).values
        Ydata = ContourData[Frames[i]]['y'][:].dropna(axis = 0).values
        
        #Furthes on axis
        dataFoA = ContourData[ContourData[Frames[i]]['x'] == origen[1]]
         
        if Xdata.size > 0 and Ydata.size > 0:
            ContPen = (((Xdata**2)-(origen[1]**2))+((Ydata**2)-(origen[0]**2)))**(1/2)
            MaxPen  = np.floor(max((((Xdata**2)-origen[1]**2)+((Ydata**2)-(origen[0]**2)))**(1/2)))
             
            FoA = max(dataFoA[Frames[i]]['y'][:])
        else:
            MaxPen = 0
            FoA = 0
        
        tempData = pd.DataFrame({'Furthest':[MaxPen], 'Furthest_on_Axis':[FoA]})
        if not 'Calculations' in locals():   
            Calculations = pd.DataFrame({'Furthest':[MaxPen], 'Furthest_on_Axis':[FoA]})
        else:
            Calculations = pd.concat([Calculations,tempData],ignore_index=True)
        
    
    
    
    