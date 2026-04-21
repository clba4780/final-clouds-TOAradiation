import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
from analysis import get_era5_variables

"""
Part 2:
Analyze data from era5
2 subplots
plot 1: graph of tempereature averaged over a day and TOA radiation
plot 2: graph of total cloud cover and TOA radoation
"""
ds = get_era5_variables(
    time_slice = ("2026-01-01", "2026-01-03"),
    lat = (37,40),
    lon = (95,102)
)

# calculate the time mean for each grid point
t2m = ds['t2m'].mean(dim = 'time')
toa = ds['toa'].mean(dim = 'time')
cc = ds['cc'].mean(dim = 'time')

# calculate the spatial mean for each time
t2m = ds['t2m'].mean(dim = ['latitude', 'longitude'])
toa = ds['toa'].mean(dim = ['latitude', 'longitude'])
cc = ds['cc'].mean(dim = ['latitude', 'longitude'])


fig, (ax_temp, ax_toa, ax_cc) = plt.subplots(3,1, figsize = (9,5), sharex=True)

ax_temp.plot(t2m["time"], t2m)
ax_temp.set_ylabel("Temperature (degC)")
ax_temp.set_title("2-meter temperature")
ax_temp.grid(True, alpha = 0.3)

ax_toa.plot(toa['time'], toa)
ax_toa.set_ylabel("TOA Incident Solar Radiation (W/m^2)")
ax_toa.set_title("TOA Incident Solar Radiation")
ax_toa.grid(True, alpha=0.3)

ax_cc.plot(cc['time'], cc)
ax_cc.set_ylabel("Total Cloud Cover (0-1)")
ax_cc.set_xlabel("Time")
ax_cc.set_title("TOA Incident Solar Radiation")
ax_cc.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("era5_t2m_toa_cc_comparison.png", dpi = 150)
print("era5_variable_comparison.png saved")
plt.show()