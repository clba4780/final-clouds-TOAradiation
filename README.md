# Cloud cover effect on surface solar radition and 2m temperature

A lightweight python package that compares net surface solar radiation and surface solar radiaition under clear sky conditions. This packages take data from era5 reanalysis and import the necesaryy variables into a NetCDF File. Once loaded the package will out put a series of plots and maps analyszing the relationship between cloud cover, surface radiation, and temperature. 

This is useful because...

# background


# installation

```
pip install -e .
```
for plotting support
```
pip install -e ".[plot]"
```

# quickstart
```
from grab_era5 import load, open_era5
from project import get_era5_variables

# 1. Open era5 and download the variables: 2-meter temperature (2m_temperature), TOA incident solar radition (toa_incident_solar_radiation), and total cloud cover (total_cloud_cover). 

# The function get_era5_variables loads all three variables into a NetCDF file then sesperates them for analysis
ds = get_era5_variables(
    time_slice = ("2020-01-01", "2020-02-01"),
    # lat, lon correspond to the state of Kansas
    lat = (37,40)
    lon = (95, 102)
)
```