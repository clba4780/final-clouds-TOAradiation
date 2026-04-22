import matplotlib.pyplot as plt
import numpy as np
from analysis import get_era5_variables

ds = get_era5_variables(
    time_slice= ("2025-06-01", "2025-08-31"),
    lat = (25,50), 
    lon = (-125, 165),
    name = "era5_summer2025_contigUS"
)

# scatter plot for cloud cover and sw surface radiation
cc = ds['cc'].mean(dim = 'time')
snsr = ds['snsr'].mean(dim = 'time')


plt.scatter(cc, snsr, alpha = 0.3)
plt.xlabel("Total Cloud Cover")
plt.ylabel("Surface Net Solar Radiation")
plt.colorbar(label = "Cloud Cover")
plt.title("Cloud Cover vs Solar Radiation")

plt.savefig("relationship.png", dpi = 150)
plt.show()
print ("relationship.png saved")
