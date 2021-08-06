import requests
from datetime import datetime
import xml.etree.ElementTree as ET

print('\nProvide Latitude and Longitude in decimal degrees')
LAT = float(input('Latitude\t: '))
LON = float(input('Longitude\t: '))
# LAT = 14.36574
# LON = 121.400784

DATE = datetime.today().strftime('%Y.%m.%d')
print('\nProvide Geographic Region Boundary in decimal degrees')
print('Press "Enter" to use [Default]')
NORTH = float(input("North [21.1]\t: ") or 21.1)
SOUTH = float(input("South [4.00]\t: ") or 4.00)
EAST = float(input("East [128.5]\t: ") or 128.5)
WEST = float(input("West [116.1]\t: ") or 116.1)

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
