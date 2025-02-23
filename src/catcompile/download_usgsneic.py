import os, sys
from catcompile.USGS_save_catalogs import (serialize_usgs, 
                                           download_overall_seismicity,
                                           usgs_save_catalog)

if __name__ == '__main__':
    output_path = sys.argv[1]
    overall_seismicity_file = download_overall_seismicity()
    serialize_usgs(os.path.join(output_path, overall_seismicity_file))