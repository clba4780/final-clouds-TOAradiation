from grab_era5 import list_variables

# All 200+ variables
for v in list_variables():
    print(v["variable"], f"({v['units']})", v["dims"])

# Filter by keyword
(list_variables("temperature"))
