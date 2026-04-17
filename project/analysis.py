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

# 2-meter temperature avaerged over latitude and longitude
ts = t2m.mean(["latitude", "longitude"]) - 273.15

# TOA radiation averaged over lat/lon
avg_toa = toa.mean(["latitude", "longitude"])

# total cloud cover averaged over latitude, longitude
avg_cc = cc.mean(["latitude", "longitude"])


fig, (ax_temp, ax_cc) = plt.subplots(2,1, figsize = (9,5), sharex=True)

ax_temp.plot(t2m["time"], ts)
ax_temp.set_ylabel("Temperature (degC)")
ax_temp.set_xlabel("Time")
ax_temp.set_title("2-meter temperature vs TOA incident solar radiation")
ax_temp.grid(True, alpha = 0.3)

ax_cc.plot(cc['time'], avg_cc)
ax_cc.set_ylabel("Percent cloud cover")
ax_cc.set_xlabel("Time")
ax_cc.set_title("Total Cloud Cover vs TOA Incident Solar Radiation")
ax_cc.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("era5_t2m_toa_cc_comparison.png", dpi = 150)
print("era5_t2m_toa_cc_comparison.png saved")
plt.show()