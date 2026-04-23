import matplotlib.pyplot as plt

from analysis import get_era5_variables

"""
time series of efficiency
"""
ds = get_era5_variables(
    time_slice = ("2025-06-01", "2025-08-31"),
    lat = (),
    lon = (95,102),
    name = "era_5_2026_Jan1-3"
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