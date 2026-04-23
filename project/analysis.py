import os
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from grab_era5 import load, open_era5

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
    # lat, lon correspond to the state of Kansas
    lat = (25, 50),
    lon = (-125, -65), 
    name = '2025_Jun22_contigUS'
    )
    """
    fname = f"era_5_{name}"
    
    if cache and os.path.exists(fname + ".nc"):
        print ("Loading from cache...")
        return xr.open_dataset(fname + ".nc")
    
    print ("Downloading data set...")
    snsr = load(open_era5("surface_net_solar_radiation", time_slice, lat, lon))
    snsr_cs = load(open_era5("surface_net_solar_radiation_clear_sky", time_slice, lat, lon))
    toa = load(open_era5("toa_incident_solar_radiation", time_slice, lat, lon))
    cc = load(open_era5("total_cloud_cover",time_slice, lat, lon))
    
    ds = xr.Dataset({
        "snsr" : snsr,
        "snsr_cs": snsr_cs, 
        "toa" : toa, 
        "cc" : cc
    })
    
    if cache:
        print ("saving dataset...")
        ds.to_netcdf(fname + ".nc")
    
    return (ds['snsr'], ds['snsr_cs'], ds['toa'], ds['cc'])



if __name__ == "__main__":
    ds = get_era5_variables(
    time_slice = ("2025-06-01", "2025-08-31"),
    lat = (25, 50),
    lon = (-125, -65), 
    name = 'summer2025_contigUSA'
)

    # take the difference between snsr and snsr_cs to determine the radiative effect of the cloud
    ds['cre'] = (ds['snsr_cs'] - ds['snsr'])/1000

    # take the ratio to determine the efficient the solar radiation is
    ds['efficiency'] = (ds['snsr']/ds['snsr_cs'])

    def mapping(title, filename, label, ds):
        fig, ax = plt.subplots(
            figsize=(10, 5),
            subplot_kw={'projection': ccrs.Robinson()}   # 1. Choose map projection
        )

        # 2. Plot xarray data — always set transform to your data's CRS
        ds['efficiency'].isel(time=0).plot(
            ax=ax,
            transform=ccrs.PlateCarree(),                # data is on regular lat/lon
            cmap='plasma',
            cbar_kwargs={'label': label, 'shrink': 0.7}
        )

        # 3. Add geographic features
        ax.coastlines(linewidth=0.8)
        ax.add_feature(cfeature.BORDERS, linewidth=0.5, linestyle='--')
        ax.add_feature(cfeature.LAND, facecolor='lightgray', alpha=0.3)
        ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)

        # Add state borders
        ax.add_feature(cfeature.STATES, edgecolor = 'gray', linewidth = 0.5, alpha = 0.2)


        ax.set_title(title, fontsize=13)
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        print (f"{filename} saved")
        plt.show()

        return fig,ax

    mapping("Cloud Efficiency Summer 2025",
            "efficiency_contigUS_summer.png",
            "Cloud Efficiency (0-1)" ,
            ds
            )
