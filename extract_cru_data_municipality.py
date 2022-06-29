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

##1) unzip CRU temperature data file in the workshop folder, which I obtained from here: https://catalogue.ceda.ac.uk/uuid/c26a65020a5e4b80b20018f148556681
##2) You need to have now a subfolder ./cru_ts4.05.1901.2020.tmp.dat.nc in the folder where this script resides

## shapefile with municipalities centroids in wgs84 lat,lon:
mex_muni_centr_shp=r'mex_admbnda_adm2_govmex_20210618_pt.shp'
cru_vars=['tmp'] #temperature variable
region='Chiapas' #region of interest
   
## read municipalities shapefile
gdf=gp.read_file(mex_muni_centr_shp)
gdf=gdf[gdf.mex_admb_7==region].reset_index()
gdf['lat']=gdf.geometry.y
gdf['lon']=gdf.geometry.x

## control variables for individual code blocks:
vis=True ### requires gdal, optional code to visualize the data, 
## optionally for a subset, for each point in time, and creates an animated gif.

extract=False ### writes out municipality level data to csv file for each point in time.

netcdf2geotiff=False### requires gdal, optional code to export one or all epochs to geotiff

if vis:######################################################
    from osgeo import gdal
    import imageio
    mx_subset_imgcoo=[110,150,120,200] ### Mexico bounding box
    filenames = []
    for var in cru_vars:
        infile='NETCDF:"'+r'.\cru_ts4.05.1901.2020.%s.dat.nc\cru_ts4.05.1901.2020.%s.dat.nc":%s' %(var,var,var)
        ds=gdal.Open(infile)
        arr=ds.ReadAsArray()
        
        timevalues=ds.GetMetadata()['NETCDF_DIM_time_VALUES'][1:-1].split(',')
        timevalues=[int(x) for x in timevalues]
        
        startdate = datetime.datetime.strptime("01/01/1900", "%m/%d/%Y")
        datetime_vals=[(startdate+datetime.timedelta(days=x)) for x in  timevalues]
        
        epochs=len(timevalues)
        for t in np.arange(0,epochs):
            currarr=arr[t,:,:]
            currarr[currarr>9e+36]=0           
            currarr=currarr[mx_subset_imgcoo[0]:mx_subset_imgcoo[1],mx_subset_imgcoo[2]:mx_subset_imgcoo[3]] 
            
            currdate=datetime_vals[t]
            currdate_fmt = '%s/%s/%s' %(currdate.year,currdate.month,currdate.day)
            
            fig,ax=plt.subplots()
            img=ax.imshow(currarr,cmap='nipy_spectral',vmin=0,vmax=30)
            ax.set_xlabel('Data source: CRU TS monthly high-resolution gridded multivariate climate dataset', fontsize=7)
            plt.title('Average temperature '+currdate_fmt)
            fig.colorbar(img,fraction=0.025)
            plt.show() 
            filename = '%s.png' %currdate_fmt.replace('/','')
            fig.savefig(filename)
            plt.close()
            filenames.append(filename)            
            
    # build gif
    with imageio.get_writer('cru_tmp_animated.gif', mode='I') as writer:
        for filename in filenames:
            if os.path.exists(filename):
                image = imageio.imread(filename)
                writer.append_data(image)
        
    # Remove files
    for filename in set(filenames):
        if os.path.exists(filename):
            os.remove(filename)

if extract:######################################################
    for var in cru_vars:
        alloutdf=pd.DataFrame()
        
        ##get CRU data from netcdf file using xarray:
        currdir='./cru_ts4.05.1901.2020.%s.dat.nc' %var
        os.chdir(currdir)
        nc_file='cru_ts4.05.1901.2020.%s.dat.nc' %(var)
        NC = xr.open_dataset(nc_file)
        
        ##for each municipality, get full time series:
        total=len(gdf)
        for i,row in gdf.iterrows():
            lat=row.lat
            lon=row.lon
            muni_id=row.mex_admb_3
            muni_name=row.mex_admb_2
            dsloc = NC.sel(lat=lat,lon=lon,method='nearest')
            currvalues = dsloc[var].values 
            alldates=[np.datetime_as_string(x.values)[:10].replace('-','') for x in NC.time]
            currdf=pd.DataFrame(data=currvalues).transpose()
            currdf.columns=['%s_%s' %(var,x) for x in alldates]
            currdf['muni_name']=muni_name
            currdf['muni_id']=muni_id
            currdf['lat']=lat
            currdf['lon']=lon
            alloutdf=alloutdf.append(currdf)            
            print(i,total,var,muni_name,muni_id,lat,lon)
                
        ##write results (temperature time series per municipality in region of interest) to csv file:
        alloutdf.to_csv('../muni_centroid_cru_%s_%s.csv' %(var,region),index=False,encoding='ISO-8859-1')            
         
    
if netcdf2geotiff: #########################################################
    from osgeo import gdal
    mx_subset_imgcoo=[110,150,120,200] ### Mexico bounding box

    date_of_interest = datetime.datetime(1970, 10, 16, 0, 0)
      
    for var in cru_vars:
        infile='NETCDF:"'r'.\cru_ts4.05.1901.2020.%s.dat.nc\cru_ts4.05.1901.2020.%s.dat.nc":%s' %(var,var,var)
        ds=gdal.Open(infile)
        arr=ds.ReadAsArray()
        
        timevalues=ds.GetMetadata()['NETCDF_DIM_time_VALUES'][1:-1].split(',')
        timevalues=[int(x) for x in timevalues]
        
        startdate = datetime.datetime.strptime("01/01/1900", "%m/%d/%Y")
        datetime_vals=[(startdate+datetime.timedelta(days=x)) for x in  timevalues]
        
        epochs=len(timevalues)
        for t in np.arange(0,epochs):
            currarr=arr[t,:,:]
            currarr[currarr>9e+36]=0
                        
            currdate=datetime_vals[t]
            
            ### comment to export all points in time #####
            if not currdate==date_of_interest:
                continue
            ##############################################

            currdate_fmt = '%s_%s_%s' %(currdate.year,currdate.month,currdate.day)

            outRaster='cru_%s_%s.tif' %(var,currdate_fmt)
            data=currarr        
            geo_transform=ds.GetGeoTransform()
            projection=ds.GetProjection()

            driver = gdal.GetDriverByName('GTiff')
            rows, cols = data.shape
            DataSet = driver.Create(outRaster, cols, rows, 1, gdal.GDT_Float32)
            DataSet.SetGeoTransform(geo_transform)
            DataSet.SetProjection(projection)
            DataSet.GetRasterBand(1).WriteArray(currarr)                
            DataSet = None
            del DataSet

            outname_lzw=outRaster.replace('.tif','_lzw.tif')
            gdal_translate = r'gdal_translate %s %s -co COMPRESS=LZW' %(outRaster,outname_lzw)
            #print(gdal_translate)
            response=subprocess.check_output(gdal_translate, shell=True)
            #print(response)
            os.remove(outRaster)
            os.rename(outname_lzw,outRaster)
            print(var,currdate_fmt)  
            plt.imshow(currarr,cmap='nipy_spectral')
            break
