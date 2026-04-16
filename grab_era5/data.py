from grab_era5 import list_variables
from grab_era5 import open_era5

# All 200+ variables
for v in list_variables():
    print(v["variable"], f"({v['units']})", v["dims"])

# Filter by keyword
(list_variables("temperature"))
(list_variables("wind"))
(list_variables("precipitation"))