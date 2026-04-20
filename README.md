# TOA, 2-meter temperature, cloud cover comparison

A lightweight python package that compares TOA incident solar radiation, 2-meter temperature and cloud cover using observations from ERA-5 reanalysis. 

# background
2-meter temperature, cloud cover, and top-of-atmosphere (TOA) incident solar radition are key variables important for undstanding how incoming shortwave (SW) radiation from the Sun influence the surface of the Earth. 

TOA incident solar radiation represents the amount of energy reaching the top of the atmosphere, which is then modulated by the  cloud cover over a region. By comparing these variables, this packages analyzes how cloud cover and incoming solar radiation impact surface temperature. 

# installation

```
pip install -e .
```
for plotting support
```
pip install -e ".[plot]"
```

# quickstart
```
from grab_era5 import load, open_era5
from project import get_era5_variables

# 1. Open era5 and download the variables: 2-meter temperature (2m_temperature), TOA incident solar radition (toa_incident_solar_radiation), and total cloud cover (total_cloud_cover). 

# The function get_era5_variables loads all three variables into a NetCDF file
ds = get_era5_variables(
    time_slice = ("2020-01-01", "2020-02-01"),
    # lat, lon correspond to the state of Kansas
    lat = (37,40)
    lon = (95, 102)
)

# Seperate the varibles from the larger dataset (ds) into seperate variables to manipulate 
t2m = ds["t2m"]
toa = ds["toa"]
cc = ds["cc"]

# compute simple analysis for one location
# UPDATE THEN ADD SIMPLE ANALYSIS 