import os
import openquake.cat.isc_downloader as isc
from catcompile import USGS_save_catalogs as usgs

"""
Downloads earthquake bulletin from ISC website:
http://www.isc.ac.uk/iscbulletin/search/bulletin/
"""
def download_isc(settings=None):
    if settings is None:
        ISF_SETTINGS_FILE = "PH_ISF_Settings.par"
    
    isc_cat = isc.ISCBulletinUrl()
    # Load settings saved in file
    isc_cat.LoadSettings(os.path.join(os.path.dirname(__file__), 
                                                    ISF_SETTINGS_FILE))

    # Geographic extents
    isc_cat.SetField('RectangleBottomLatitude', str(usgs.SOUTH))
    isc_cat.SetField('RectangleTopLatitude', str(usgs.NORTH))
    isc_cat.SetField('RectangleLeftLongitude', str(usgs.WEST))
    isc_cat.SetField('RectangleRightLongitude', str(usgs.EAST))

    # Download catalog in separate 10-year blocks to work around download limit
    isc_cat.GetCatalogue(SplitYears=10)

    # Save in ISF format
    isc_cat.WriteOutput("PH_ISF_Catalogue.isf", OverWrite=True)


if __name__ == '__main__':
    download_isc()