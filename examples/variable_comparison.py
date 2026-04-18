from grab_era5 import load, open_era5
from project.analysis import get_era5_variables

import matplotlib.pyplot as plt

"""
Part 2:
Analyze data from era5
2 subplots
plot 1: graph of tempereature averaged over a day and TOA radiation
plot 2: graph of total cloud cover and TOA radoation
"""
t2m, toa, cc = get_era5_variables(
    time_slice = ("2026-01-01", "2026-01-03"),
    lat = (37,40),
    lon = (95,102)
)


fig, (ax_temp, ax_cc) = plt.subplots(2,1, figsize = (9,5), sharex=True)

ax_temp.plot(t2m["time"], t2m)
ax_temp.set_ylabel("Temperature (degC)")
ax_temp.set_xlabel("Time")
ax_temp.set_title("2-meter temperature")
ax_temp.grid(True, alpha = 0.3)

ax_cc.plot(toa['time'], toa)
ax_cc.set_ylabel("TOA Incident Solar Radiation (W/m^s)")
ax_cc.set_xlabel("Time")
ax_cc.set_title("TOA Incident Solar Radiation")
ax_cc.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("era5_t2m_toa_cc_comparison.png", dpi = 150)
print("era5_t2m_toa_comparison.png saved")
plt.show()