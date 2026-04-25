import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from analysis import get_era5_variables

"""
Example 1: Create a scatterplot comparing the 
Total Cloud Cover to the Net Surface Solar Radiation over different regions. 
"""

# load variables from era5
ds = get_era5_variables(
    time_slice= ("2025-06-01", "2025-08-31"),
    lat = (25,50), 
    lon = (-125, -65),
    name = "summer2025_contigUS"
)

# cloud statistics
cre = ds['snsr_cs'] - ds['snsr']
ds['eff'] = (ds['snsr']/ds['snsr_cs']).clip(0,1)
eff = ds['eff']
cc = ds['cc']

times = ds['time'].values
months = ds['time'].dt.month.values.flatten()

# Take the spatial mean then flatten
cc = ds['cc'].mean(dim = ['latitude', 'longitude']).values.flatten()
eff = ds['eff'].mean(dim = ['latitude', 'longitude']).values.flatten()

# boolean mask to filter out invalid data
mask = np.isfinite(cc) & np.isfinite(eff)
cc = cc[mask]
eff = eff[mask]
months = months[mask]


if len(cc) <2:
    print ("Skipping: not enough data")

else:
# resample to avoid overplotting for large arrays
# keeps only 30% of points without removing any of the data 
    resample = np.random.choice(len(cc), size=max(2,int(len(cc)*0.3)), replace = False)
    # use the same resample for both so the points still match
    # (makes the scatter plot cleaner for long term analysis)
    cc = cc[resample]
    eff = eff[resample]
    months = months[resample]

fig, ax = plt.subplots(figsize=(8,5))


# Color by month instead of repeating cc on color axis
cmap = cm.get_cmap('plasma', 3)
sc = ax.scatter(cc, eff, c=months, cmap=cmap, vmin = 6, vmax =8, alpha=0.5, s=15, edgecolors='none')

cbar = fig.colorbar(sc, ax=ax, ticks=[6, 7, 8])
cbar.set_label("Month")
cbar.ax.set_yticklabels(['Jun', 'Jul', 'Aug'])

    # Regression line
m, b = np.polyfit(cc, eff, 1)
x_line = np.linspace(cc.min(), cc.max(), 100)
ax.plot(x_line, m * x_line + b, 'r--', linewidth=1.5, label=f'Trend (slope={m:.2f})')

plt.xlabel("Total Cloud Cover (fraction)")
plt.ylabel("Solar Efficiency (snsr/snsr_cs)")
plt.title("Cloud Cover vs Solar Efficiency")
plt.grid(alpha = 0.2)

plt.tight_layout()
plt.savefig("relationship.png", dpi = 150)
print ("relationship.png saved")
plt.show()
