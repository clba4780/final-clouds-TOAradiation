from grab_era5 import load, open_era5

import matplotlib.pyplot as plt

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
def get_era5_variables(time_slice, lat, lon):
    t2m = load(get_t2m(time_slice, lat, lon))
    toa = load(get_toa(time_slice, lat, lon))
    cc = load(get_cc(time_slice, lat, lon))
    return (t2m, toa, cc)

# input dates, lat, long for each variable in get_era5_variables
t2m, toa, cc = get_era5_variables(
    time_slice = ("2020-01-01", "2020-01-31"),
    # lat, lon correspond to the state of Kansas
    lat = (37,40),
    lon = (95, 102)
)

"""
Part 2:
Analyze data from era5
2 subplots
plot 1: graph of tempereature averaged over a day and TOA radiation
plot 2: graph of total cloud cover and TOA radoation
"""

def avg_values():
# 2-meter temperature avaerged over latitude and longitude
    ts = t2m.mean(["latitude", "longitude"]) - 273.15

# TOA radiation averaged over lat/lon
    avg_toa = toa.mean(["latitude", "longitude"])

# total cloud cover averaged over latitude, longitude
    avg_cc = cc.mean(["latitude", "longitude"])

    return(ts, avg_toa, avg_cc)


def daily_mean(ds):
    return ds.resample(time="1D").mean()

def correlation(ds1, ds2):
    return (float(ds1.corr(ds2)))

def simple_comparison(time_slice, ds1, ds2, label1, label2, title, fig_name):
    plt.figure()
    plt.plot(time_slice, ds1, label = label1)
    plt.plot(time_slice, ds2, label=label2)
    plt.legend(loc="best")
    plt.title(title)
    plt.xlabel("Time")
    plt.save(fig_name, dpi=150)
    print(fig_name, " saved")
    plt.show()


if __name__ == "__main__":
    daily_mean(t2m)
    daily_mean(cc)

    correlation(t2m, cc)

    simple_comparison(t2m['time'], t2m, cc, 
                      '2m-temperature', 'total cloud cover',
                      '2m-temperature vs total cloud cover',
                      "t2m_vs_cc.png")
