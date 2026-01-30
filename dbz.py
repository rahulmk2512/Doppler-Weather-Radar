# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 22:58:03 2026

@author: rahul
"""

import xarray as xr
import numpy as np
import pandas as pd

# ---------------------------------------
# File paths
# ---------------------------------------
input_file = r"C:\Users\rahul\Downloads\Data_MOSDAC\Data_MOSDAC\RCTLS_01JUN2021_061746_L2B_STD.nc"
output_csv = r"C:\Users\rahul\Desktop\DBZ_per_time_explicit.csv"

# ---------------------------------------
# Open dataset safely
# ---------------------------------------
ds = xr.open_dataset(input_file, decode_times=False)

print("Dataset opened successfully ✅")

# ---------------------------------------
# Extract DBZ array
# ---------------------------------------
DBZ = ds["DBZ"].values   # shape: (time, range)

n_time, n_range = DBZ.shape
print(f"DBZ shape: time={n_time}, range={n_range}")

# ---------------------------------------
# Create column names (range gate index)
# ---------------------------------------
range_columns = [f"gate_{i}" for i in range(n_range)]

# ---------------------------------------
# Create DataFrame
# ---------------------------------------
df = pd.DataFrame(DBZ, columns=range_columns)

# Optional: add time index column
if "time" in ds:
    df.insert(0, "time_seconds", ds["time"].values)

# ---------------------------------------
# Save to CSV
# ---------------------------------------
df.to_csv(output_csv, index=False)

print("CSV file saved successfully ✅")
print("Location:", output_csv)
