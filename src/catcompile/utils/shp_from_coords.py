import geopandas as gpd
import os
from shapely.geometry import Polygon
from catcompile import USGS_save_catalogs as usgs


def shp_from_coords(coordinates=None, output_shapefile=None):
    """
    Create a polygon shapefile given a list of lon-lat pairs
    :param coordinates:
        List of tuples of longitude-latitude pairs
        (Default: coordinates defined in coords.json)
    :param output_shapefile
        String representing path of output shapefile 
        (Default: PH-extents.shp located in same directory)
    """
    if output_shapefile is None:
        DIRNAME = os.path.dirname(__file__)
        SHP_FILE = 'PH-extents'
        # Define the output shapefile path
        output_shapefile = os.path.join(DIRNAME, SHP_FILE + ".shp")

    if coordinates is None:
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

    # Save the GeoDataFrame to a shapefile
    gdf.to_file(output_shapefile)


if __name__ == '__main__':
    shp_from_coords()