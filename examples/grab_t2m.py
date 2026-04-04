"""
Load ERA5 2-metre temperature over Colorado for summer 2010,
average over the spatial box, and plot a time series.

Run:
    python examples/grab_t2m.py
"""

import matplotlib.pyplot as plt

from grab_era5 import load, open_era5

# Open lazily — no data downloaded yet
da = open_era5(
    "2m_temperature",
    time_slice=("2010-06-01", "2010-06-03"),
    lat=(37.0, 41.0),       # Colorado-ish; order doesn't matter
    lon=(-109.0, -102.0),   # negative °W fine; converted to 0–360 internally
)

print("Lazy DataArray before loading:")
print(da, "\n")

# Download the subset and show a progress bar
da = load(da)

# Spatial mean → time series, convert K → °C
ts = da.mean(["latitude", "longitude"]) - 273.15

fig, ax = plt.subplots(figsize=(12, 4))
ts.plot(ax=ax)
ax.set_title("ERA5 2-m Temperature — Colorado box, summer 2010")
ax.set_ylabel("Temperature (°C)")
ax.set_xlabel("Time")
plt.tight_layout()
plt.savefig("era5_t2m_colorado.png", dpi=150)
print("Saved era5_t2m_colorado.png")
plt.show()
