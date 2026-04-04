"""
Print all available ERA5 variables with units and dimensions.
Pass an optional filter string to narrow results.

Run:
    python examples/list_all_variables.py
    python examples/list_all_variables.py temperature
    python examples/list_all_variables.py wind
"""

import sys
from grab_era5 import list_variables

filter_str = sys.argv[1] if len(sys.argv) > 1 else None
variables = list_variables(filter=filter_str)

header = f"{'Variable':<60}  {'Units':<20}  Dims"
print(header)
print("-" * len(header))
for v in variables:
    dims = ", ".join(v["dims"])
    print(f"{v['variable']:<60}  {v['units']:<20}  {dims}")

print(f"\n{len(variables)} variable(s)")
