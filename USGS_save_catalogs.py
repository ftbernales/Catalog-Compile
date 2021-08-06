import json
import requests
from datetime import datetime
import xml.etree.ElementTree as ET

f = open('coords.json')
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
