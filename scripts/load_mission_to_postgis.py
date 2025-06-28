import os
import sys
import django
import datetime
from osgeo import gdal
from django.contrib.gis.geos import Polygon, LineString

# Setup Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bathystack.settings')
django.setup()

from api.models import SurveyMission


def get_raster_footprint(raster_path):
    ds = gdal.Open(raster_path)
    gt = ds.GetGeoTransform()

    x_min = gt[0]
    y_max = gt[3]
    x_max = x_min + gt[1] * ds.RasterXSize
    y_min = y_max + gt[5] * ds.RasterYSize

    # Clockwise polygon
    coords = [
        (x_min, y_max),
        (x_max, y_max),
        (x_max, y_min),
        (x_min, y_min),
        (x_min, y_max),
    ]
    return Polygon(coords)


def simulate_trackline(bounds: Polygon) -> LineString:
    # Simple diagonal path inside bounds
    minx, miny, maxx, maxy = bounds.extent
    return LineString([
        (minx + 0.05 * (maxx - minx), miny + 0.05 * (maxy - miny)),
        (maxx - 0.05 * (maxx - minx), maxy - 0.05 * (maxy - miny))
    ])


def insert_survey(name, raster_path):
    print(f"📡 Inserting survey: {name}")
    footprint = get_raster_footprint(raster_path)
    track = simulate_trackline(footprint)

    SurveyMission.objects.create(
        name=name,
        description="Imported from raster",
        date=datetime.date.today(),
        raster_path=raster_path,
        footprint=footprint,
        track=track
    )
    print("✅ Survey mission inserted into database.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python load_mission_to_postgis.py <name> <path/to/raster.tif>")
        sys.exit(1)

    mission_name = sys.argv[1]
    raster_path = sys.argv[2]

    insert_survey(mission_name, raster_path)