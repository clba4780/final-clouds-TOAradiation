import sys
import logging
import os

# Suppress gRPC/gcsfs fork warnings that clutter student output
os.environ.setdefault("GRPC_VERBOSITY", "ERROR")
logging.getLogger("absl").setLevel(logging.ERROR)

import numpy as np
import xarray as xr

_ZARR_URL = "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3"
_STORAGE_OPTIONS = {"token": "anon"}

# Module-level cache so the zarr store is only opened once per session
_DS_CACHE = None


def _get_dataset() -> xr.Dataset:
    global _DS_CACHE
    if _DS_CACHE is None:
        _DS_CACHE = xr.open_zarr(
            _ZARR_URL,
            storage_options=_STORAGE_OPTIONS,
            consolidated=True,
            chunks={},
        )
    return _DS_CACHE


def open_era5(
    variable: str,
    time_slice: tuple,
    lat: float | tuple | slice | None = None,
    lon: float | tuple | slice | None = None,
    level: int | list[int] | None = None,
) -> xr.DataArray:
    """Open ERA5 data from the ARCO-ERA5 zarr archive on Google Cloud Storage.

    Data are loaded lazily — nothing is downloaded until you call .compute()
    or .load().  The full dataset is a single zarr store, so opening it is
    fast regardless of the time range requested.

    Parameters
    ----------
    variable : str
        Variable name, e.g. ``"2m_temperature"`` or ``"total_precipitation"``.
        Use ``list_variables()`` to see all options with units.
    time_slice : (start, end)
        ISO date strings, e.g. ``("2010-06", "2010-08")`` or ``("2000", "2010")``.
        Required — ERA5 is hourly and global; always subset before loading.
    lat : float, (south, north), or slice, or None
        Latitude selection.  Scalar → nearest grid point.  Tuple or slice →
        bounding range (values may be given in either order).
        ERA5 latitude runs 90 → −90; this is handled internally.
    lon : float, (west, east), or slice, or None
        Longitude. Negative °W values are accepted and converted to 0–360.
    level : int or list[int] or None
        Pressure level(s) in hPa (e.g. ``500``, ``[850, 500, 250]``).
        Only applies to pressure-level variables such as ``"temperature"``,
        ``"geopotential"``, ``"u_component_of_wind"``, etc.
        Ignored for surface variables.

    Returns
    -------
    xr.DataArray
        Lazy DataArray.  Call ``.load()`` to download.

    Examples
    --------
    2-metre temperature at a point::

        da = open_era5("2m_temperature", ("2010-06", "2010-08"), lat=40.0, lon=-105.0)
        (da.load() - 273.15).plot()   # convert K → °C

    Surface pressure over a box, convert to hPa::

        da = open_era5("surface_pressure", ("2000", "2000"),
                       lat=(37.0, 41.0), lon=(-109.0, -102.0))
        (da.load() / 100).mean(["latitude", "longitude"]).plot()

    500 hPa geopotential::

        da = open_era5("geopotential", ("2010-01", "2010-03"), level=500,
                       lat=(20.0, 60.0), lon=(-130.0, -60.0))
        da.mean("time").plot()
    """
    ds = _get_dataset()

    if variable not in ds:
        raise ValueError(
            f"'{variable}' not found. Call list_variables() to see options."
        )

    da = ds[variable]

    # Time selection
    da = da.sel(time=slice(*time_slice))

    # Pressure-level selection (only for vars with a 'level' dimension)
    if level is not None and "level" in da.dims:
        if isinstance(level, int):
            da = da.sel(level=level)
        else:
            da = da.sel(level=level)

    # Spatial selection
    da = _sel_spatial(da, lat, lon)

    return da


def list_variables(filter: str | None = None) -> list[dict]:
    """Return all available ERA5 variables with dimensions and units.

    Parameters
    ----------
    filter : str or None
        Optional substring to filter variable names, e.g. ``"temperature"``,
        ``"wind"``, ``"precipitation"``.

    Returns
    -------
    list of dict with keys ``variable``, ``units``, ``dims``.

    Examples
    --------
    >>> for v in list_variables("temperature"):
    ...     print(v["variable"], f"({v['units']})")
    """
    ds = _get_dataset()
    result = [
        {
            "variable": v,
            "units": ds[v].attrs.get("units", ""),
            "dims": list(ds[v].dims),
        }
        for v in sorted(ds.data_vars)
        if filter is None or filter.lower() in v.lower()
    ]
    return result


def load(da: xr.DataArray, desc: str | None = None) -> xr.DataArray:
    """Download a lazy DataArray and show a progress bar.

    Use this instead of ``.load()`` or ``.compute()`` for friendlier output.

    Parameters
    ----------
    da : xr.DataArray
        Lazy DataArray returned by ``open_era5``.
    desc : str or None
        Label shown next to the progress bar. Defaults to the variable name.

    Returns
    -------
    xr.DataArray
        The same DataArray with data fully loaded into memory.

    Examples
    --------
    ::

        da = open_era5("2m_temperature", ("2010-06", "2010-08"), lat=40.0, lon=-105.0)
        da = load(da)
        da.plot()
    """
    from dask.diagnostics import ProgressBar

    label = desc or da.name or "Downloading ERA5"
    print(label)
    with ProgressBar(dt=0.5):
        return da.compute()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _sel_spatial(da: xr.DataArray, lat, lon) -> xr.DataArray:
    """Subset a DataArray on ERA5's regular lat/lon grid.

    ERA5 latitude **decreases** from 90 to -90, so range slices must be
    (max, min).  This is handled automatically — pass values in any order.
    """
    if lat is not None:
        if np.isscalar(lat):
            da = da.sel(latitude=float(lat), method="nearest")
        elif isinstance(lat, slice):
            lo = float(lat.start) if lat.start is not None else -90.0
            hi = float(lat.stop) if lat.stop is not None else 90.0
            da = da.sel(latitude=slice(max(lo, hi), min(lo, hi)))
        else:
            lo, hi = float(lat[0]), float(lat[1])
            da = da.sel(latitude=slice(max(lo, hi), min(lo, hi)))

    if lon is not None:
        if np.isscalar(lon):
            da = da.sel(longitude=float(lon) % 360, method="nearest")
        elif isinstance(lon, slice):
            start = float(lon.start) % 360 if lon.start is not None else None
            stop = float(lon.stop) % 360 if lon.stop is not None else None
            lo, hi = sorted([start, stop])
            da = da.sel(longitude=slice(lo, hi))
        else:
            lo, hi = sorted(float(v) % 360 for v in lon)
            da = da.sel(longitude=slice(lo, hi))

    return da


if __name__ == "__main__":
#running core.py from main will list all the variables available in ERA5
    filter_str = sys.argv[1] if len(sys.argv) > 1 else None
    variables = list_variables(filter=filter_str)

    header = f"{'Variable':<60}  {'Units':<20}  Dims"
    print(header)
    print("-" * len(header))
    for v in variables:
        dims = ", ".join(v["dims"])
        print(f"{v['variable']:<60}  {v['units']:<20}  {dims}")

    print(f"\n{len(variables)} variable(s)")