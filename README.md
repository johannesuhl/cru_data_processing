# CRU data processing
A python script to access, visualize and extract time series of CRU long-term climate data at discrete locations.

This script aims to visualize and extract time series of long-term climate data at discrete spatial locations from the CRU TS monthly high-resolution gridded multivariate climate dataset (Harris et al. 2020; https://www.nature.com/articles/s41597-020-0453-3).

This repository contains a point shapefile holding the centroids of municipalities in Mexico (mex_admbnda_adm2_govmex_20210618_pt.shp, adopted from data obtained at https://data.humdata.org/dataset/mexican-administrative-level-0-country-1-estado-and-2-municipio-boundary-polygons).

CRU data needs to be obtained from https://catalogue.ceda.ac.uk/uuid/c26a65020a5e4b80b20018f148556681 and unzipped in a subfolder of the directory where the script extract_cru_data_municipality.py resides.

extract=True:
The script extract_cru_data_municipality.py will read the municipalities shapefile, and create a CSV file containing the CRU temperature estimates for each point in time, for each municipality in Mexico.

Optionally, by setting vis=True, the script will plot the data for reach point in time.
By setting netcdf2geotiff=True, the script will export the CRU data to GeoTIFF for a given (or all) point in time.
