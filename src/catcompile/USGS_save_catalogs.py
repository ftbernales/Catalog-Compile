import os
import json
import requests
from datetime import datetime
import xml.etree.ElementTree as ET
import pandas as pd


with open(os.path.join(os.path.dirname(__file__), 'coords.json')) as f:
    coords = json.load(f)
    LAT = coords['center']['latitude']
    LON = coords['center']['longitude']

    DATE = datetime.today().strftime('%Y.%m.%d')
    NORTH = coords['boundary']['north']
    SOUTH = coords['boundary']['south']
    EAST = coords['boundary']['east']
    WEST = coords['boundary']['west']

def usgs_save_catalog(file, extension, lat, lon, mindepth, maxdepth, radius):
    filename = file + DATE + '.' + extension
    print('\nSaving ' + filename, end='')
    url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?' + \
            'starttime=1900-01-01' + \
            '&orderby=magnitude' + \
            '&minmagnitude=4.5' + \
            '&format=' + str(extension) + \
            '&maxlatitude=' + str(NORTH) + \
            '&minlatitude=' + str(SOUTH) + \
            '&maxlongitude=' + str(EAST) + \
            '&minlongitude=' + str(WEST) + \
            '&latitude=' + str(lat) + \
            '&longitude=' + str(lon) + \
            '&maxradiuskm=' + str(radius) + \
            '&mindepth=' + str(mindepth) + \
            '&maxdepth=' + str(maxdepth)
    if extension == 'kml':
        url += '&kmlcolorby=depth'

    r = requests.get(url)
    open(filename, 'w', encoding='utf-8').write(r.content.decode('utf-8'))

    if extension == 'kml':
        tree = ET.parse(filename)

        elem = tree.find(".//{http://www.opengis.net/kml/2.2}name")
        lat = tree.find(".//{http://www.opengis.net/kml/2.2}latitude")
        lon = tree.find(".//{http://www.opengis.net/kml/2.2}longitude")
        range = tree.find(".//{http://www.opengis.net/kml/2.2}range")

        elem.text = file.replace('_', ' ').strip()
        lat.text = str(LAT)
        lon.text = str(LON)
        range.text = "3000000"

        ET.register_namespace('', "http://www.opengis.net/kml/2.2")
        tree.write(filename)

def download_overall_seismicity(output_dir=None):
    if output_dir is None:
        # Use current dir
        output_dir = os.path.join(os.path.dirname(__file__), 'cat-collections/')
    
    file_parent = os.path.join(output_dir, 'Overall_Seismicity_')
    usgs_save_catalog(file_parent, 'csv', '', '', 0, 800, '')
    usgs_save_catalog(file_parent, 'kml', '', '', 0, 800, '')


def serialize_usgs(filename):
    """
    Serialize into new csv format downloaded from USGS Comcat for reading in 
    HMTK/MBTK
    """
    NEW_FILENAME = 'usgs_formatted.csv'
    df_usgs = pd.read_csv(filename, encoding='windows-1252')
    
    # Split datetime into new separate columns
    df_usgs['time'] = pd.to_datetime(df_usgs['time'])
    df_usgs.insert(0, "year", df_usgs['time'].dt.year)
    df_usgs.insert(1, "month", df_usgs['time'].dt.month)
    df_usgs.insert(2, "day", df_usgs['time'].dt.day)
    df_usgs.insert(3, "hour", df_usgs['time'].dt.hour)
    df_usgs.insert(4, "minute", df_usgs['time'].dt.minute)
    df_usgs.insert(5, "second", df_usgs['time'].dt.second.astype(float) + \
                            df_usgs['time'].dt.microsecond.astype(float)/1.E6)
    df_usgs.drop(columns='time', inplace=True)

    # Move ID column
    id = df_usgs.pop('id')
    df_usgs.insert(0, 'id', id)

    # Rename fields to be consistent with parsers
    df_usgs.rename(columns={'mag': 'magnitude', 'magType': 'magnitudeType',
                            'id': 'eventID'}, 
                   inplace=True)
    
    # Filter events not from USGS National Earthquake Information Center, PDE
    df_usgs = df_usgs[df_usgs['net'] == 'us']

    # Save to csv
    df_usgs.to_csv(os.path.join(os.path.dirname(filename), NEW_FILENAME), 
                   index=False)


if __name__ == '__main__':
    usgs_save_catalog('Vicinity_100km_', 'csv', LAT, LON, 0, 800, 100)
    usgs_save_catalog('Vicinity_100km_', 'kml', LAT, LON, 0, 800, 100)

    usgs_save_catalog('Shallow_500km_', 'csv', LAT, LON, 0, 50, 500)
    usgs_save_catalog('Shallow_500km_', 'kml', LAT, LON, 0, 50, 500)

    usgs_save_catalog('Mid_Crust_500km_', 'csv', LAT, LON, 50, 100, 500)
    usgs_save_catalog('Mid_Crust_500km_', 'kml', LAT, LON, 50, 100, 500)

    usgs_save_catalog('Deep_500km_', 'csv', LAT, LON, 100, 800, 500)
    usgs_save_catalog('Deep_500km_', 'kml', LAT, LON, 100, 800, 500)

    usgs_save_catalog('All_Depths_500km_', 'csv', LAT, LON, 0, 800, 500)
    usgs_save_catalog('All_Depths_500km_', 'kml', LAT, LON, 0, 800, 500)

    usgs_save_catalog('Overall_Seismicity_', 'csv', '', '', 0, 800, '')
    usgs_save_catalog('Overall_Seismicity_', 'kml', '', '', 0, 800, '')
