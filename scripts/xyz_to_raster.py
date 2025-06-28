import os
import subprocess
import sys
from pathlib import Path

def run_gdal_grid(input_xyz, output_tif, output_resolution=5):
    print(f"🔄 Converting {input_xyz} to raster...")

    cmd = [
        "gdal_grid",
        "-zfield", "3",  # depth is 3rd column (0-based)
        "-a", f"invdist:power=2.0:smoothing=1.0",
        "-txe", "-180", "180",  # optional: set bounds or clip later
        "-tye", "-90", "90",
        "-outsize", "500", "500",  # or auto
        "-of", "GTiff",
        "-ot", "Float32",
        "-l", "input",
        "-a_srs", "EPSG:4326",
        "-a_ullr", "-180", "90", "180", "-90",
        "-a_srs", "EPSG:4326",
        "-a_nodata", "-9999",
        "-clipsrc", "data/aoi.geojson",  # optional
        input_xyz,
        output_tif
    ]

    subprocess.run(cmd, check=True)
    print(f"✅ Raster created: {output_tif}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python xyz_to_raster.py input.xyz output.tif")
        sys.exit(1)

    input_xyz = sys.argv[1]
    output_tif = sys.argv[2]

    run_gdal_grid(input_xyz, output_tif)