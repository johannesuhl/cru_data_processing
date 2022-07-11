# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 16:22:57 2021

@author: Johannes H. Uhl, University of Colorado Boulder, USA.
"""

import os,sys
import numpy as np
import pandas as pd
import geopandas as gp
import xarray as xr
import datetime
from matplotlib import pyplot as plt
import subprocess
from osgeo import gdal
import imageio
import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Arial"
matplotlib.rcParams['font.family'] = "sans-serif"
plt.rcParams['figure.autolayout'] = True

cru_var = 'tmp' #temperature variable

filenames = []
infile='NETCDF:"'+r'.\cru_ts4.05.1901.2020.%s.dat.nc\cru_ts4.05.1901.2020.%s.dat.nc":%s' %(cru_var,cru_var,cru_var)
ds=gdal.Open(infile)
arr=ds.ReadAsArray()

timevalues=ds.GetMetadata()['NETCDF_DIM_time_VALUES'][1:-1].split(',')
timevalues=[int(x) for x in timevalues]

startdate = datetime.datetime.strptime("01/01/1900", "%m/%d/%Y")
datetime_vals=[(startdate+datetime.timedelta(days=x)) for x in  timevalues]

cmap = matplotlib.cm.get_cmap("turbo").copy()
cmap.set_bad('black')

#cmap = matplotlib.cm.get_cmap("Greys_r").copy()
#cmap.set_bad('black')

epochs=len(timevalues)
for t in np.arange(0,epochs):
    currarr=arr[t,:,:]
    #currarr[currarr>9e+36]=np.nan  
    
    currarr[currarr>9e+36]=-np.nan  
    #currarr[currarr<=25]=0        
    #currarr[currarr>25]=30       
    
    currdate=datetime_vals[t]
    
    #if not currdate.month in [2,4,6,8,10,12]:
    #    continue
    
    currdate_fmt = '%s/%s/%s' %(currdate.year,str(currdate.month).zfill(2),str(currdate.day).zfill(2))
    currdate_fmt2 = '%s-%s' %(str(currdate.month).zfill(2),currdate.year)
    fig,ax=plt.subplots(figsize=(6,3.5))
    img=ax.imshow(currarr,cmap=cmap,vmin=-30,vmax=30)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('Data source: CRU TS monthly high-resolution gridded multivariate climate dataset\n Visualization: Johannes H. Uhl, University of Colorado Boulder (USA), 2022.', fontsize=9)
    ax.set_title('Average monthly temperature [°C] from 1901 to 2020\n'+currdate_fmt2, fontsize=15)
    #ax.set_title('Average monthly temperature >25°C \nfrom 1901 to 2020 (%s)' %currdate_fmt2, fontsize=15)

    cbar = fig.colorbar(img,fraction=0.02)
    cbar.set_ticklabels(['{0:+}'.format(int(xx)) if xx!=0 else int(xx) for xx in cbar.ax.get_yticks()]) ## add sign to colorbar ticks

    #from : https://stackoverflow.com/questions/19219963/align-ticklabels-in-matplotlib-colorbar
    ticklabs = cbar.ax.get_yticklabels()
    cbar.ax.set_yticklabels(ticklabs,ha='right')
    cbar.ax.yaxis.set_tick_params(pad=20)

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    #plt.show() 
    filename = '%s.png' %currdate_fmt.replace('/','')
    fig.tight_layout(pad=0)
    fig.savefig(filename,pad_inches = 0)
    plt.close()
    filenames.append(filename) 
    print(currdate_fmt)
    # if t>20:
    #     break
    
# build gif
with imageio.get_writer('cru_tmp_animated_global2.gif', mode='I',duration=0.001) as writer:
    for filename in filenames:
        if os.path.exists(filename):
            image = imageio.imread(filename)
            #image = image[:,:,0] ##greyscale
            writer.append_data(image)
    
# Remove files
for filename in set(filenames):
    if os.path.exists(filename):
        os.remove(filename)
