import matplotlib.pyplot as plt
import numpy as np
from analysis import get_era5_variables

ds = get_era5_variables(
    time_slice= ("2025-06-01", "2025-08-31"),
    lat = (25,50), 
    lon = (-125, -65),
    name = "summer2025_contigUS"
)

ds['eff'] = (ds['snsr']/ds['snsr_cs'])

# Find the mean over time
cc = ds['cc'].mean(dim = 'time')
eff = ds['eff'].mean(dim = 'time')

# flatten from a multi-dimensional xarray dataset to a 1d numpy array
cc = cc.values.flatten()
eff = eff.values.flatten()

# boolean mask to filter out invalid data
mask = np.isfinite(cc) & np.isfinite(eff)

cc = cc[mask]
eff = eff[mask]


plt.scatter(cc, eff, c = cc, cmap = 'viridis', alpha = 0.3, s = 10)
plt.xlabel("Total Cloud Cover")
plt.ylabel("Surface Net Solar Radiation")
plt.colorbar(label = "Cloud Cover")
plt.title("Cloud Cover vs Efficiency")

plt.tight_layout()
plt.savefig("relationship.png", dpi = 150)
plt.show()
print ("relationship.png saved")
