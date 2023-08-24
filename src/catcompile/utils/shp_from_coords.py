import geopandas as gpd
import os
from shapely.geometry import Polygon
from catcompile import USGS_save_catalogs as usgs


DIRNAME = os.path.dirname(__file__)
SHP_FILE = 'PH-extents'

# Define the coordinates of the polygon's vertices
coordinates = [
    (usgs.WEST, usgs.NORTH),
    (usgs.EAST, usgs.NORTH),
    (usgs.EAST, usgs.SOUTH),
    (usgs.WEST, usgs.SOUTH),
]

# Create a Polygon geometry
polygon = Polygon(coordinates)

# Create a GeoDataFrame with the polygon geometry
geometry = [polygon]
gdf = gpd.GeoDataFrame(geometry=geometry)

# Define the output shapefile path
output_shapefile = os.path.join(DIRNAME, SHP_FILE + ".shp")

# Save the GeoDataFrame to a shapefile
gdf.to_file(output_shapefile)