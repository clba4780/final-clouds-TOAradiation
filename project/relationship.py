import matplotlib.pyplot as plt
import numpy as np
"""
from project.analysis import get_era5_variables

ds = get_era5_variables(
    time_slice= ("2026-01-01", "2026-01-02"),
    lat = (37,40), 
    lon = (95,102)
)

t2m = ds["t2m"]
toa = ds["toa"]
cc = ds["cc"]

"""

""" Synthetic Tester Data 
Goal: figure out how to import from my data then
 take spatial and temporal avg and plot"""
# Time axis (e.g., 3 days hourly)
n = 72
time = np.arange(n)

# Simulate TOA radiation (peaks during "day", zero at "night")
toa = np.maximum(0, 800 * np.sin(2 * np.pi * time / 24))

# Simulate cloud cover (random but somewhat smooth)
np.random.seed(0)
cc = np.clip(0.5 + 0.3 * np.sin(2 * np.pi * time / 24 + 1) + 0.2 * np.random.randn(n), 0, 1)

# Simulate temperature:
# depends on radiation, reduced by clouds, plus some lag + noise
t2m = 0.02 * toa * (1 - cc) + 2 * np.sin(2 * np.pi * (time - 3) / 24) + np.random.randn(n)




plt.scatter(toa, t2m, c=cc, cmap='viridis')
plt.xlabel("TOA Incident Solar Radiation (W/m^2)")
plt.ylabel("2-meter Temperature (degC)")
plt.colorbar(label = "Cloud Cover")
plt.title("TOA Incident Solar Radiation vs 2-meter temperture")

plt.savefig("relationship.png", dpi = 150)
plt.show()
print ("relationship.png saved")
