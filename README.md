# grab-era5

A lightweight Python package for accessing [ERA5 reanalysis](https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5) data via the [ARCO-ERA5](https://github.com/google-research/arco-era5) dataset on Google Cloud Storage. No account or credentials required — the bucket is publicly accessible.

Data are opened **lazily** via [Zarr](https://zarr.dev/) and [xarray](https://docs.xarray.dev/), so you only download the chunks you actually use. The entire ERA5 dataset lives in a **single consolidated zarr store**, so there is no per-file overhead regardless of how long a time range you request.

> **Data source:** `gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3`  
> Maintained by Google Research. Coverage: 1940–present, updated monthly.

---

## Installation

```bash
pip install -e .
```

Requires Python ≥ 3.10. Core dependencies (`xarray`, `zarr`, `gcsfs`, `numpy`) are installed automatically. For plotting:

```bash
pip install -e ".[plot]"
```

---

## Quick start

### List available variables

```python
from grab_era5 import list_variables

# All 200+ variables
for v in list_variables():
    print(v["variable"], f"({v['units']})", v["dims"])

# Filter by keyword
list_variables("temperature")
list_variables("wind")
list_variables("precipitation")
```

### Load a variable

```python
from grab_era5 import open_era5

da = open_era5(
    "2m_temperature",                   # variable name
    time_slice=("2010-06", "2010-08"),  # required — always subset before loading
    lat=40.0,                           # scalar → nearest grid point
    lon=-105.0,                         # negative °W fine; converted to 0–360 internally
)

(da.load() - 273.15).plot()   # convert K → °C
```

`open_era5` returns a lazy `xr.DataArray`. Nothing is downloaded until you call `.load()` or `.compute()`.

---

## Spatial selection

### `lat` / `lon` argument forms

| Form | Behaviour |
|------|-----------|
| `scalar` (e.g. `40.0`) | Nearest grid point |
| `tuple` (e.g. `(37.0, 41.0)`) | Bounding range |
| `slice` (e.g. `slice(37.0, 41.0)`) | Bounding range (same as tuple) |
| `None` | No spatial subsetting |

ERA5 **latitude decreases** from 90 (North Pole) to −90 (South Pole). You can always pass values in natural geographic order — `(south, north)` or `(north, south)` both work correctly.

---

## Pressure-level variables

Variables like `geopotential`, `temperature`, `u_component_of_wind`, etc. have a `level` dimension (hPa). Use the `level` parameter to select one or more levels:

```python
da = open_era5(
    "geopotential",
    time_slice=("2010-01", "2010-03"),
    level=500,                        # single level in hPa
    lat=(20.0, 60.0),
    lon=(-130.0, -60.0),
)

# Multiple levels
da = open_era5("temperature", ("2000", "2000"), level=[1000, 850, 500, 250])
```

Available levels: 1, 2, 3, 5, 7, 10, 20, 30, 50, 70, 100, 125, 150, 175, 200, 225, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000 hPa.

---

## Grid

| Property | Value |
|----------|-------|
| Spatial resolution | 0.25° (~31 km) |
| Latitude range | 90 → −90 (decreasing) |
| Longitude range | 0 → 359.75 (0–360) |
| Time resolution | Hourly |
| Coverage | 1940–present |
| Pressure levels | 37 (1–1000 hPa) |

---

## Examples

```bash
# Print all available variables (optionally filter by keyword)
python examples/list_all_variables.py
python examples/list_all_variables.py temperature

# Load 2-m temperature over Colorado, plot a time series, save a PNG
python examples/grab_t2m.py
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `xarray` | Multi-dimensional arrays and lazy I/O |
| `zarr` | Zarr store backend |
| `gcsfs` | Anonymous Google Cloud Storage access |
| `numpy` | Array operations |
| `matplotlib` *(optional)* | Plotting |
