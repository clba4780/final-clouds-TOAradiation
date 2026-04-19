import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from project.analysis import get_era5_variables


"""
Example 3: Compare each variables at different locations
This example compares two different location, but it can also be used to compare multiple locations or times
1. Load in each location without changing the time period
2. Resample over latitude and longitude
3. Resample over time
4. normalize the Datasets
5. Plot the relationship
"""
# Generating synthetic data because, I am working on getting the actual data an just need a


#Location 1: Kansas
# Load in data and resample
t2m_loc1, toa_loc1, cc_loc1 = get_era5_variables(
    time_slice = ("2026-01-01", "2026-01-03"),
    lat = (37,40),
    lon = (95,102)
)
t2m_loc1 = t2m_loc1.mean(dim = ["latitude, longitude"])
toa_loc1 = toa_loc1.mean(dim = ["latitude, longitude"])
cc_loc1 = cc_loc1.mean(dim=["latitude, longitude"])

t2m_loc1 = t2m_loc1.mean(time="3H")
toa_loc1 = toa_loc1.mean(time="3H")
cc_loc1 = cc_loc1.mean(time="3H")

# Location 2: Florida
t2m_loc2, toa_loc2, cc_loc2 = get_era5_variables(
    time_slice = ("2026-01-01", "2026-01-03"),
    lat = (24,31),
    lon = (80,87)
)

t2m_loc2 = t2m_loc2.mean(dim = ["latitude, longitude"])
toa_loc2 = toa_loc2.mean(dim = ["latitude, longitude"])
cc_loc2 = cc_loc2.mean(dim=["latitude, longitude"])

t2m_loc2 = t2m_loc2.mean(time="3H")
toa_loc2 = toa_loc2.mean(time="3H")
cc_loc2 = cc_loc2.mean(time="3H")


def normalize(x):
    return ((x-(x.mean()))/ x.std())

fig, (ax_t2m, ax_toa, ax_cc) = plt.subplots(3, 1, figsize = (9,5), sharex = True)

# Comparing 2-m temperature 
ax_t2m.plot(t2m_loc1['time'], normalize(t2m_loc1))
ax_t2m.plot(t2m_loc2['time'], normalize(t2m_loc2))
ax_t2m.set_ylabel("Normalized 2-meter temperature (°C)")
ax_t2m.set_title('2-meter Temperature Comparison (Kansas vs. Florida)')
ax_t2m.legend()

# Comparing TOA Radiation 
ax_toa.plot(toa_loc1['time'], normalize(toa_loc1))
ax_toa.plot(toa_loc2['time'], normalize(toa_loc2))
ax_toa.set_ylabel("TOA Incident Solar Radiation (W/m^s)")
ax_toa.set_title('Normalized Top of Atmosphere Incident Solar Radiation (Kansas vs. Florida)')
ax_toa.legend()

# Comparing Cloud Cover
ax_cc.plot(cc_loc1['time'], normalize(cc_loc1))
ax_cc.plot(cc_loc2['time'], normalize(cc_loc2))
ax_cc.set_ylabel("Cloud Cover")
ax_cc.set_title('Normalized Total Cloud Cover (Kansas vs. Florida)')
ax_cc.legend()

plt.tight_layout()
plt.savefig("location_comparison.png", dpi=150)
print ("location_comparison.png saved")
plt.show()