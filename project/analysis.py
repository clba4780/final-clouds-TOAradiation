from grab_era5 import load, open_era5

import matplotlib.pyplot as plt

"""
Grabbing 2-meter temperature, total incident (SW) radition at TOA , and 
total cloud cover from ERA-5
- Create a function that inputs a time, latitude, and longitude and 
loads the data into seperate variables
- Use a name gaurd to create a simple plot with each variable to test the function
"""


def get_t2m(time_slice, lat, lon):
    da1 = open_era5(
        "2m_temperature", 
        time_slice = time_slice,
        lat = lat, 
        lon = lon
    )
    t2m = da1.load()
    return(t2m)

def get_toa(time_slice, lat, lon):
    da2 = open_era5(
        "toa_incident_solar_radiation", 
        time_slice = time_slice,
        lat = lat,
        lon = lon
    )
    toa = da2.load()
    return (toa)

def get_cc(time_slice, lat, lon):
    da3 = open_era5(
        "total_cloud_cover",
        time_slice = time_slice, 
        lat = lat, 
        lon = lon
    )
    cc = da3.load()
    return(cc)

def get_variables(time_slice, lat, lon):
    t2m = get_t2m(time_slice, lat, lon),
    cc = get_cc(time_slice, lat, lon), 
    toa = get_toa(time_slice, lat, lon)
    return t2m, cc, toa

get_variables(("2020-01-01", "2020-01-31"), (37,40), (95,102))

if __name__ == "__main__":
    t2m_mean = t2m.mean(["latitude", "longitude"]) - 273.15

    fig, ax = plt.subplots(figsize=(12, 4))
    t2m_mean.plot(ax=ax)
    ax.set_title("ERA5 2-m Temperature — Colorado box, summer 2010")
    ax.set_ylabel("Temperature (°C)")
    ax.set_xlabel("Time")
    plt.tight_layout()
    plt.savefig("era5_t2m_colorado.png", dpi=150)
    print("Saved era5_t2m_colorado.png")
    plt.show()
