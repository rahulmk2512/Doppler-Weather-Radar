# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 22:49:58 2026

@author: rahul
"""

import numpy as np
import xarray as xr
import pandas as pd

# -------------------------------------------------
# 1. FILE PATH
# -------------------------------------------------
file_path = r"C:\Users\rahul\Downloads\Data_MOSDAC\Data_MOSDAC\RCTLS_01JUN2021_061746_L2B_STD.nc"

# -------------------------------------------------
# 2. RADAR LOCATION (given)
# -------------------------------------------------
lat0 = 8.5374        # degrees
lon0 = 76.8657       # degrees
alt0 = 27.0          # meters (not used in 2D)

# -------------------------------------------------
# 3. CONSTANTS
# -------------------------------------------------
R = 6371000.0            # Earth radius (m)
range_resolution = 250.0  # IMD C-band DWR (meters)

# -------------------------------------------------
# 4. OPEN DATASET (SAFE)
# -------------------------------------------------
ds = xr.open_dataset(file_path, decode_times=False)

# -------------------------------------------------
# 5. EXTRACT GEOMETRY
# -------------------------------------------------
azimuth = np.deg2rad(ds["azimuth"].values)      # radians
elevation = np.deg2rad(ds["elevation"].values)  # radians
time_array = ds["time"].values                  # raw time values

# Number of range gates from DBZ
n_gates = ds["DBZ"].shape[-1]

# Range array (meters)
range_array = np.arange(n_gates) * range_resolution

# -------------------------------------------------
# 6. CREATE 2D GRIDS (time × range)
# -------------------------------------------------
az2d, r2d = np.meshgrid(azimuth, range_array, indexing="ij")
el2d, _ = np.meshgrid(elevation, range_array, indexing="ij")

# -------------------------------------------------
# 7. POLAR → CARTESIAN (local)
# -------------------------------------------------
horizontal_distance = r2d * np.cos(el2d)

dx = horizontal_distance * np.sin(az2d)   # Easting (m)

# -------------------------------------------------
# 8. CARTESIAN → LONGITUDE
# -------------------------------------------------
longitude = lon0 + (dx / (R * np.cos(np.deg2rad(lat0)))) * (180 / np.pi)

print("Longitude array shape:", longitude.shape)

# -------------------------------------------------
# 9. SAVE TO CSV (EXPLICIT PER TIME)
# -------------------------------------------------
# Create DataFrame
lon_df = pd.DataFrame(longitude)

# Optional: label rows with time values
lon_df.insert(0, "time_seconds", time_array)

# Save CSV
output_csv = r"C:\Users\rahul\Desktop\longitude_per_time_explicit.csv"
lon_df.to_csv(output_csv, index=False)

print("Longitude CSV saved successfully ✅")
print("File location:", output_csv)
