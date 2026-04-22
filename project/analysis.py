import os
import xarray as xr
import matplotlib.pyplot as plt
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




"""
Part 2:
Analyze data from era5
2 subplots
plot 1: graph of tempereature averaged over a day and TOA radiation
plot 2: graph of total cloud cover and TOA radoation
"""

# Turn this into a function that takes spatial averages, them temporal averges, then normalize for comparisons
def avg_values(snsr, snsr_cs, toa, cc):
# Surface net solar radiation averaged over latitude and longitude
    snsr_avg = ds['snsr'].mean(["latitude", "longitude"])

#Surface net solar radition clear sky averaged over latutude and longitude
    snsr_cs_avg = ds['snsr_cs'].mean(['latitude', 'longitude'])

# TOA radiation averaged over lat/lon
    avg_toa = ds['toa'].mean(["latitude", "longitude"])

# total cloud cover averaged over latitude, longitude
    avg_cc = ds['cc'].mean(["latitude", "longitude"])

    return(snsr_avg, snsr_cs_avg, avg_toa, avg_cc)


def daily_mean(ds):
    return ds.resample(time="1D").mean()

def correlation(ds1, ds2):
    return (xr.corr(ds1, ds2, dim = None, weights = None))


def simple_comparison(time_slice, ds1, ds2, label1, label2, title, fig_name):
    fig, ax1 = plt.subplots()
    
    ax1.plot(time_slice, ds1, label = label1, color = 'tab:blue')
    ax1.set_xlabel("Time")
    ax1.set_ylabel(label1, color = 'tab:blue')
    ax1.tick_params(axis = 'y', labelcolor = 'tab:blue')
    ax1.legend()

    ax2 = ax1.twinx()
    ax2.plot(time_slice, ds2, label = label2, color = 'tab:red')
    ax2.set_ylabel(label2, color = 'tab:red')
    ax2.tick_params(axis = 'y', labelcolor = 'tab:red')
    ax2.legend()

    plt.title(title)
    plt.savefig(f"{fig_name}.png", dpi = 150)
    plt.show()



if __name__ == "__main__":
    ds = get_era5_variables(
    time_slice = ("2020-01-01", "2020-01-07"),
    # lat, lon correspond to the state of Kansas
    lat = (37,40),
    lon = (95, 102), 
    name = 'oneweek_jan_kansas'
)
    
    snsr_avg, snsr_cs_avg, toa_avg, cc_avg = avg_values(ds['snsr'], ds['snsr_cs'], ds['toa'], ds['cc'])      
    
    snsr_daily = daily_mean(snsr_avg) / 1000
    snsr_cs_daily = daily_mean(snsr_cs_avg) / 1000
    cc_daily = daily_mean(cc_avg)
    toa_daily = daily_mean(toa_avg)

    corr_temp_cloud = correlation(ds['snsr'], ds['cc'])
    corr_temp_toa = correlation(ds['snsr'], ds['toa'])
    corr_toa_cloud = correlation(ds['toa'], ds['cc'])

    simple_comparison(snsr_daily['time'], snsr_daily, snsr_cs_daily, 
                      'Surface Net Solar Radition (W/km^2)', 'Surface Net Solar Radiation Clear Sky (W/km^2)',
                      'Surface Net Solar Radtion vs. Clear Sky Surface Net Solar Raditation',
                      "snsr_vs_snsrcs")
