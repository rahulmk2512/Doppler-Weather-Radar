# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 22:23:21 2026

@author: rahul
"""

import numpy as np
import xarray as xr
import csv

# -------------------------------------------------
# 1. Radar location (given)
# -------------------------------------------------
lat0 = 8.5374        # degrees
lon0 = 76.8657       # degrees
alt0 = 27.0          # meters (not used in 2D lat calculation)

# Earth radius
R = 6371000.0        # meters

# IMD C-band DWR standard range resolution
range_resolution = 250.0  # meters

# -------------------------------------------------
# 2. Open dataset safely
# -------------------------------------------------
file_path = r"C:\Users\rahul\Downloads\Data_MOSDAC\Data_MOSDAC\RCTLS_01JUN2021_061746_L2B_STD.nc"
ds = xr.open_dataset(file_path, decode_times=False)

print("Dataset opened successfully ✅")

# -------------------------------------------------
# 3. Extract radar geometry
# -------------------------------------------------
az = np.deg2rad(ds["azimuth"].values)      # radians
el = np.deg2rad(ds["elevation"].values)    # radians

# Number of rays (time) and range gates
n_rays = az.shape[0]
n_gates = ds["DBZ"].shape[-1]

print("Number of rays :", n_rays)
print("Number of gates:", n_gates)

# Range array (meters)
r = np.arange(n_gates) * range_resolution

# -------------------------------------------------
# 4. Create 2D grids (time × range)
# -------------------------------------------------
az2d, r2d = np.meshgrid(az, r, indexing="ij")
el2d, _ = np.meshgrid(el, r, indexing="ij")

# Horizontal distance
d = r2d * np.cos(el2d)

# Northing offset
dy = d * np.cos(az2d)

# -------------------------------------------------
# 5. Latitude calculation
# -------------------------------------------------
lat = lat0 + (dy / R) * (180.0 / np.pi)

print("Latitude array shape:", lat.shape)

# -------------------------------------------------
# 6. Save latitude array to CSV
# -------------------------------------------------
output_csv = r"C:\Users\rahul\Desktop\latitude_per_time.csv"

with open(output_csv, mode="w", newline="") as f:
    writer = csv.writer(f)

    # Write header (range gate indices)
    header = ["time_index"] + [f"gate_{i}" for i in range(n_gates)]
    writer.writerow(header)

    # Write data row by row
    for i in range(n_rays):
        row = [i] + lat[i, :].tolist()
        writer.writerow(row)

print("Latitude CSV saved successfully ✅")
print("File location:", output_csv)
