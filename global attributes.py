# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 21:20:09 2026

@author: rahul
"""

import xarray as xr

file_path = r"C:\Users\rahul\Downloads\Data_MOSDAC\Data_MOSDAC\RCTLS_01JUN2021_061746_L2B_STD.nc"

ds = xr.open_dataset(file_path, decode_times=False)

print("Dataset opened successfully ✅")

# Print DBZ attributes safely
for k, v in ds["DBZ"].attrs.items():
    print(k, ":", v)

print("\nGlobal attributes:")
for k, v in ds.attrs.items():
    print(k, ":", v)
z