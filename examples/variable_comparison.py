from project import analysis, get_era5_variables

import matplotlib.pyplot as plt

t2m, toa, cc = get_era5_variables(
    time_slice = ("2020-01-01", "2020-01-31"),
    # lat, lon correspond to the state of Kansas
    lat = (37,40),
    lon = (95, 102)
)

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