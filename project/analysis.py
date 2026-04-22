import os
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from grab_era5 import load, open_era5

"""
Part 1:
Grabbing 2-meter temperature, total incident (SW) radition at TOA , and 
total cloud cover from ERA-5
- Create a function that inputs a time, latitude, and longitude and 
loads the data into seperate variables
Paramaters:
- Time period: time_slice
    ("start_year-start_month-start_date", "end_year-end_month-end_date")
    (0000-00-00)
- Latitude: lat
    Input latitude range
- Longitude: lon
    Input longitude range
"""

# A funtion load the date into three different variables
def get_era5_variables(time_slice, lat, lon, name, cache = True):
    fname = f"era_5_{name}"
    
    if cache and os.path.exists(fname + ".nc"):
        print ("Loading from cache...")
        return xr.open_dataset(fname + ".nc")
    
    print ("Downloading data set...")
    snsr = load(open_era5("surface_net_solar_radiation", time_slice, lat, lon))
    snsr_cs = load(open_era5("surface_net_solar_radiation_clear_sky", time_slice, lat, lon))
    toa = load(open_era5("toa_incident_solar_radiation", time_slice, lat, lon))
    cc = load(open_era5("total_cloud_cover",time_slice, lat, lon))
    
    ds = xr.Dataset({
        "snsr" : snsr,
        "snsr_cs": snsr_cs, 
        "toa" : toa, 
        "cc" : cc
    })
    
    if cache:
        print ("saving dataset...")
        ds.to_netcdf(fname + ".nc")
    
    return (ds['snsr'], ds['snsr_cs'], ds['toa'], ds['cc'])



ds = get_era5_variables(
    time_slice = ("2025-06-22", "2025-06-22"),
    # lat, lon correspond to the state of Kansas
    lat = (25, 50),
    lon = (-125, -65), 
    name = '2025_Jun22_contigUS'
)

# take the difference between snsr and snsr_cs to determine the radiative effect of the cloud
ds['cre'] = ds['snsr_cs'] - ds['snsr']

# take the ratio to determine the efficient the solar radiation is
ds['efficiency'] = ds['snsr']/ds['snsr_cs']


def mapping(title, ):
    fig, ax = plt.subplots(
        figsize=(10, 5),
        subplot_kw={'projection': ccrs.Robinson()}   # 1. Choose map projection
    )

    # 2. Plot xarray data — always set transform to your data's CRS
    ds['cre'].isel(time=0).plot(
        ax=ax,
        transform=ccrs.PlateCarree(),                # data is on regular lat/lon
        cmap='plasma',
        cbar_kwargs={'label': 'Cloud Radiative Effect', 'shrink': 0.7}
    )

    # 3. Add geographic features
    ax.coastlines(linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5, linestyle='--')
    ax.add_feature(cfeature.LAND, facecolor='lightgray', alpha=0.3)
    ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)

    ax.set_title('Cloud Radiative Effect — Model Day 1', fontsize=13)
    plt.tight_layout()
    plt.savefig()
    plt.show()
