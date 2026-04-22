import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


from analysis import get_era5_variables

ds = get_era5_variables(
    time_slice = ("2025-06-22", "2025-06-22"),
    # lat, lon correspond to the state of Kansas
    lat = (25, 50),
    lon = (-125, -65), 
    name = '2025_Jun22_contigUS'
)

# take the difference between snsr and snsr_cs to determine the radiative effect of the cloud
ds['cre'] = ds['snsr_cs'] - ds['snsr']

# take the ratio to determine the efficient the solar radiation is
ds['efficiency'] = ds['snsr']/ds['snsr_cs']



fig, ax = plt.subplots(
    figsize=(10, 5),
    subplot_kw={'projection': ccrs.Robinson()}   # 1. Choose map projection
)

# 2. Plot xarray data — always set transform to your data's CRS
ds['cre'].isel(time=0).plot(
    ax=ax,
    transform=ccrs.PlateCarree(),                # data is on regular lat/lon
    cmap='plasma',
    cbar_kwargs={'label': 'Cloud Radiative Effect', 'shrink': 0.7}
)

# 3. Add geographic features
ax.coastlines(linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linewidth=0.5, linestyle='--')
ax.add_feature(cfeature.LAND, facecolor='lightgray', alpha=0.3)
ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)

ax.set_title('Cloud Radiative Effect — Model Day 1', fontsize=13)
plt.tight_layout()
plt.show()
