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
# A funtion to get the 2-meter temperature (Units: K)
def get_t2m(time_slice, lat, lon):
    return (open_era5("2m_temperature", time_slice=time_slice, lat=lat, lon=lon))

# A funtion to the the TOA incident solar radition (Units: W/m^2)
def get_toa(time_slice, lat, lon):
    return (open_era5("toa_incident_solar_radiation", time_slice=time_slice, lat=lat, lon=lon))

# A funtion to get the total cloud cover (0-1)
def get_cc(time_slice, lat, lon):
    return (open_era5("total_cloud_cover", time_slice=time_slice, lat=lat, lon=lon))

# A funtion load the date into three different variables
def get_era5_variables(time_slice, lat, lon, cache = True):
    fname = f"era_5_{time_slice[0]}_{time_slice[1]}_{lat}_{lon}"
    
    if cache and os.path.exists(fname):
        print ("Loading from cache...")
        return xr.open_dataset(fname + ".nc")
    
    print ("Downloading data set...")
    t2m = load(get_t2m(time_slice, lat, lon))
    toa = load(get_toa(time_slice, lat, lon))
    cc = load(get_cc(time_slice, lat, lon))
    
    ds = xr.Dataset({
        "t2m" : t2m, 
        "toa" : toa, 
        "cc" : cc
    })
    
    if cache:
        ds.to_netcdf(fname + ".nc")
    
    return (ds)


# input dates, lat, long for each variable in get_era5_variables
ds = get_era5_variables(
    time_slice = ("2020-01-01", "2020-01-31"),
    # lat, lon correspond to the state of Kansas
    lat = (37,40),
    lon = (95, 102)
)

t2m = ds["t2m"]
toa = ds["toa"]
cc = ds["cc"]

"""
Part 2:
Analyze data from era5
2 subplots
plot 1: graph of tempereature averaged over a day and TOA radiation
plot 2: graph of total cloud cover and TOA radoation
"""

def avg_values(t2m, toa, cc):
# 2-meter temperature avaerged over latitude and longitude
    t2m_avg = t2m.mean(["latitude", "longitude"]) - 273.15

# TOA radiation averaged over lat/lon
    avg_toa = toa.mean(["latitude", "longitude"])

# total cloud cover averaged over latitude, longitude
    avg_cc = cc.mean(["latitude", "longitude"])

    return(t2m_avg, avg_toa, avg_cc)


def daily_mean(ds):
    return ds.resample(time="1D").mean()

def correlation(ds1, ds2):
    ds1, ds2 = ds1.align(ds2)
    return (float(ds1.corr(ds2)))


def simple_comparison(time_slice, ds1, ds2, label1, label2, title, fig_name):
    plt.figure()
    plt.plot(time_slice, ds1, label = label1)
    plt.plot(time_slice, ds2, label=label2)
    plt.legend(loc="best")
    plt.title(title)
    plt.xlabel("Time")
    plt.savefig(fig_name, dpi=150)
    print(fig_name, " saved")
    plt.show()


if __name__ == "__main__":
    t2m_avg, toa_avg, cc_avg = avg_values(t2m, toa, cc)      
    
    t2m_daily = daily_mean(t2m_avg)
    cc_daily = daily_mean(cc_avg)
    toa_daily = daily_mean(toa_avg)

    corr_temp_cloud = correlation(t2m, cc)
    corr_temp_toa = correlation(t2m, toa)
    corr_toa_cloud = correlation(toa, cc)

    simple_comparison(t2m_daily['time'], t2m_daily, cc_daily, 
                      'Surface Temperature (degC)', 'Cloud Cover',
                      '2m-temperature vs total cloud cover',
                      "t2m_vs_cc.png")
