# CRU data processing
### A python script to access, visualize and extract time series of CRU long-term climate data globally, regionally, and at discrete locations.

### CRU average temperature (1900-2020):
<img width="450" src="https://github.com/johannesuhl/cru_data_processing/blob/main/cru_tmp_animated_global2.gif">

These scripts aim to visualize and extract time series of long-term climate data at discrete spatial locations from the CRU TS monthly high-resolution gridded multivariate climate dataset (Harris et al. 2020; https://www.nature.com/articles/s41597-020-0453-3).

```cru_gif.py``` will create the above visualization, and ```extract_cru_data_municipality.py``` will extract CRU time series for specific locations, do some conversions and also visualize the data.

This repository contains a point shapefile holding the centroids of municipalities in Mexico (mex_admbnda_adm2_govmex_20210618_pt.shp, adopted from data obtained at https://data.humdata.org/dataset/mexican-administrative-level-0-country-1-estado-and-2-municipio-boundary-polygons).

CRU data needs to be obtained from https://catalogue.ceda.ac.uk/uuid/c26a65020a5e4b80b20018f148556681 and unzipped in a subfolder of the directory where the script extract_cru_data_municipality.py resides.

```extract=True```:
The script extract_cru_data_municipality.py will read the municipalities shapefile, and create a CSV file containing the CRU temperature estimates for each point in time, for each municipality in Mexico.

```vis=True```:
Optionally, the script will plot the data for each point in time and create an animated GIF.
The user can constrain the visualization to a specific coordinate range (note that these coordinates are image coordinates, not world coordinates):
```
currarr=currarr[mx_subset_imgcoo[0]:mx_subset_imgcoo[1],mx_subset_imgcoo[2]:mx_subset_imgcoo[3]]
```
or to a specific month:
```
if not currdate.month in [8]:
    continue
```

```netcdf2geotiff=True```:By setting netcdf2geotiff=True, the script will export the CRU data to GeoTIFF for a given (or all) point in time.

### CRU temperature data visualized for Mexico only (1900-1910):
<img width="750" src="https://github.com/johannesuhl/cru_data_processing/blob/main/cru_tmp_animated.gif">

### CRU temperature data visualized for the month of August only (1900-2020):
<img width="750" src="https://github.com/johannesuhl/cru_data_processing/blob/main/cru_tmp_animated_August.gif">


