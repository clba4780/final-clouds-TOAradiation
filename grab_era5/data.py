from grab_era5 import list_variables
from grab_era5 import open_era5

# All 200+ variables
for v in list_variables():
    print(v["variable"], f"({v['units']})", v["dims"])

# Filter by keyword
print(list_variables("temperature"))
(list_variables("wind"))
(list_variables("precipitation"))

# TOA Radiation (toa_incident_solar_radiation (J m**-2) ['time', 'latitude', 'longitude'])
toa = open_era5(
    "toa_incident_solar_radiation",                   # variable name
    time_slice=("2010-06", "2010-08"),  # required — always subset before loading
    lat=40.0,                           # scalar → nearest grid point
    lon=-105.0,                         # negative °W fine; converted to 0–360 internally
)

(toa.load()).plot()   # convert K → °C

# Cloud cover (total_cloud_cover ((0 - 1)) ['time', 'latitude', 'longitude'])
cc = open_era5(
    "total_cloud_cover",                   # variable name
    time_slice=("2010-06", "2010-08"),  # required — always subset before loading
    lat=40.0,                           # scalar → nearest grid point
    lon=-105.0,                         # negative °W fine; converted to 0–360 internally
)

(cc.load()).plot()   # convert K → °C

# surface temperature '2m_temperature', 'units': 'K', 'dims': ['time', 'latitude', 'longitude']
st = open_era5(
    "2m_temperature",                   # variable name
    time_slice=("___", "___"),  # required — always subset before loading
    lat=40.0,                           # scalar → nearest grid point
    lon=-105.0,                         # negative °W fine; converted to 0–360 internally
)

(st.load() - 273.15).plot()   # convert K → °C