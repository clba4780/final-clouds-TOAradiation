# TOA, 2-meter temperature, cloud cover comparison

A lightweight python package that compares TOA incident solar radiation, 2-meter temperature and cloud cover using observations from ERA-5 reanalysis. 

# background
2-meter temperature, cloud cover, and top-of-atmosphere (TOA) incident solar radition are key variables important for undstanding how incoming shortwave (SW) radiation from the Sun influence the surface of the Earth. 

TOA incident solar radiation represents the amount of energy reaching the top of the atmosphere, which is then modulated by the  cloud cover over a region. By comparing these variables, this packages analyzes how cloud cover and incoming solar radiation impact surface temperature. 

# installation

```
pip install -e .
```
for plotting support
```
pip install -e ".[plot]"
```

# quickstart