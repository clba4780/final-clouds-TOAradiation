import os
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from core import load, open_era5

def get_era5_variables(time_slice, lat, lon, name, cache = True):
    """
    Open ERA5 variables relating to Surfacer Energy Balance and Cloud Effect: 
    - Surface Net Solar Radiation (snsr)
    - Surface Net Solar Radiation Clear Sky (snsr_cs)
    - TOA Incident Solar Radiation (toa)
    - Total Cloud Cover (cc)

    Data are loaded lazily — nothing is downloaded until you call
    ``.compute()`` / ``.load()`` or use the :func:`load` helper.

    Paramaters
    ----------
    time_slice : (start, end)
    lat : latitude
    lon : longitude
    name : name of NetCDF file

    Returns
    ----------
    xr.DataArray
        Lazy DataArray of snsr (W/m^s), snsr_cs (W/m^2), toa (W/m^2), cc (0-1)

    Example 
    ----------
    ds = get_era5_variables(
    time_slice = ("2025-06-22", "2025-06-22"),
    # lat, lon correspond to the contiguous United States
    lat = (25, 50),
    lon = (-125, -65), 
    name = '2025_Jun22_contigUS'
    )
    """
    fname = f"era5_{name}"
    
    if cache and os.path.exists(fname + ".nc"):
        print ("Loading from cache...")
        return xr.open_dataset(fname + ".nc")
    
    print ("Downloading data set...")
    # convert snsr, snsr_cs, and toa to W/km^2 and t2m to Celsius
    snsr = load(open_era5("surface_net_solar_radiation", time_slice, lat, lon))
    snsr_cs = load(open_era5("surface_net_solar_radiation_clear_sky", time_slice, lat, lon))
    cc = load(open_era5("total_cloud_cover",time_slice, lat, lon))
    t2m = load(open_era5("2m_temperature", time_slice, lat, lon)) - 273
    
    ds = xr.Dataset({
        "snsr" : snsr,
        "snsr_cs": snsr_cs, 
        "cc" : cc,
        "t2m" : t2m,
    })
    
    if cache:
        print ("saving dataset...")
        ds.to_netcdf(fname + ".nc")
    
    return (ds['snsr'], ds['snsr_cs'], ds['cc'], ds['t2m'])

def cloud_stats(ds):
    # Cloud radiative effect
    ds['cre'] = (ds['snsr_cs'] - ds['snsr'])
    # Efficiency - how much solar radiation reaches the surface (0-1)
    ds['eff'] = (ds['snsr']/ds['snsr_cs'])

    return ds

def map_features(ax):
    # 3. Add geographic features
    ax.coastlines(linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5, linestyle='--')
    ax.add_feature(cfeature.LAND, facecolor='lightgray', alpha=0.3)
    ax.add_feature(cfeature.STATES, edgecolor = 'gray', linewidth = 0.5, alpha = 0.2)
    ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)


def mapping(title, filename, ds, time = 0, n_rows = 1):
    panels = [
        {
            "data": ds['cre'].isel(time=time),
            "label": "Cloud Radiative Effect (kW/m^2)",
            "subtitle": "Cloud Radiative Effect",
            "cmap": "RdBu_r"
        },
        {
            "data": ds['eff'].isel(time=time),
            "label": "Solar Efficiency",
            "subtitle": "Solar Efficiency", 
            "cmap": "plasma"
        }, 
        {
            "data": ds['t2m'].isel(time=time),
            "label": "2-meter Temperature (°C)",
            "subtitle": "2-meter Temperature",
            "cmap": "coolwarm"
        }
    ]
    n_cols = -(-len(panels)//n_rows)
    
    fig, ax = plt.subplots(
        nrows = n_rows,
        ncols = n_cols,
        figsize = (7*n_cols,4*n_rows),
        subplot_kw={'projection': ccrs.Robinson()},   # 1. Choose map projection
        constrained_layout = True
    )

    axes_flat = list(ax.flat) if hasattr(ax, "flat") else [ax]

    for ax, panel in zip(axes_flat, panels):
        panel['data'].plot(
            ax = ax,
            transform = ccrs.PlateCarree(),
            cmap = panel['cmap'],
            cbar_kwargs = {'label': panel['label'], 'shrink':0.7}
        )
        map_features(ax)
        ax.set_title(panel['subtitle'], fontsize = 10)
    
    fig.suptitle(title, fontsize =15)
    plt.savefig(filename, dpi = 150)
    print (f"{filename} saved")
    plt.show()

    return fig, ax

if __name__ == "__main__":
    ds = get_era5_variables(
        time_slice = ("2025-06-01", "2025-08-31"),
        lat = (25, 50),
        lon = (-125, -65), 
        name = 'summer2025_contigUSA'
    )

    cloud_stats(ds)

    mapping(
        "Cloud, Solar Radiation, & Temperature Analysis - Summer 2025", 
        filename = "analysis",
        ds = ds, 
    )