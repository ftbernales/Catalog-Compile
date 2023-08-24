import datetime as dt
import os

import openquake.cat.catalogue_query_tools as cqt
from openquake.cat.hmg import info
from openquake.cat.isc_homogenisor import (DuplicateFinder, DynamicHomogenisor,
                                           HomogenisorPreprocessor,
                                           MagnitudeConversionRule)
from openquake.cat.parsers.converters import (GCMTtoISFParser,
                                              GenericCataloguetoISFParser)
from openquake.cat.parsers.isf_catalogue_reader import ISFReader

import catcompile.regressions as reg
from catcompile.usgs_catalog_reader import UsgsCsvReader
from itertools import pairwise

"""
Tools for creating homogenized catalog in terms of magnitude and origin
"""
REJECT_KEYS = ["mining", "geothermal", "explosion", "quarry", "reservoir", 
                "rockburst"]

DIRNAME = os.path.dirname(__file__)
ISF_FILE = 'cat-collections/PH_ISF_Catalogue'
ISCGEM_FILE = 'cat-collections/isc-gem-cat'
GCMT_FILE = 'cat-collections/gcmt-cat-1976-2020'
USGS_FILE = 'cat-collections/usgs_formatted'
PS_FILE = 'cat-collections/ps1992-ph-cat'
MAN_FILE = 'cat-collections/phivolcs-combined-minM4pt5'
MERGED_FILE = 'cat-collections/merged-catalog'

def homogenize():
    # STEP 1: READ AND IMPORT CATALOGS
    ## 1- Read ISC
    isc_parser = ISFReader(os.path.join(DIRNAME, ISF_FILE + '.isf'), 
                        rejection_keywords=REJECT_KEYS)
    isc_cat = isc_parser.read_file("ISC-RB", "ISC-PH")
    print(f"ISC-Reviewed Catalog contains: {isc_cat.get_number_events()} events.")

    _, mag_df = isc_cat.build_dataframe()
    x1, _ = info.get_table_mag_agency(mag_df)
    print(x1)

    ## 2- Read ISC-GEM
    iscgem_parser = GenericCataloguetoISFParser(
        os.path.join(DIRNAME, ISCGEM_FILE + ".csv"))
    iscgem_cat = iscgem_parser.parse("ISC-GEM", "ISC-GEM-PH")
    print(f"ISC-GEM Catalog contains: {iscgem_cat.get_number_events()} events.")

    _, mag_df = iscgem_cat.build_dataframe()
    x1, _ = info.get_table_mag_agency(mag_df)
    print(x1)

    ## 3- Read GCMT
    gcmt_parser = GCMTtoISFParser(os.path.join(DIRNAME, GCMT_FILE + ".txt"))
    gcmt_cat = gcmt_parser.parse()
    print(f"GCMT Catalog contains: {gcmt_cat.get_number_events()} events.")

    _, mag_df = gcmt_cat.build_dataframe()
    x1, _ = info.get_table_mag_agency(mag_df)
    print(x1)

    ## 4- Read USGS NEIC Comcat
    usgs_parser = UsgsCsvReader(os.path.join(DIRNAME, USGS_FILE + ".csv"))
    usgs_cat = usgs_parser.read_file("USGS-NEIC", "USGS-PH")
    print(f"USGS-NEIC Catalog contains: {usgs_cat.get_number_events()} events.")

    _, mag_df = usgs_cat.build_dataframe()
    x1, _ = info.get_table_mag_agency(mag_df)
    print(x1)

    ## 5- Read Pacheco & Sykes (1992) Catalog
    ps_parser = GenericCataloguetoISFParser(
        os.path.join(DIRNAME, PS_FILE + ".csv"))
    ps_cat = ps_parser.parse("PS", "PS-PH")
    print(f"USGS-NEIC Catalog contains: {ps_cat.get_number_events()} events.")

    _, mag_df = ps_cat.build_dataframe()
    x1, _ = info.get_table_mag_agency(mag_df)
    print(x1)

    ## 6- Read PHIVOLCS Catalog (note: datetimes already converted to UTC)
    man_parser = GenericCataloguetoISFParser(
        os.path.join(DIRNAME, MAN_FILE + ".csv"))
    man_cat = man_parser.parse("MAN", "MAN-CAT")
    print(f"PHIVOLCS Catalog contains: {man_cat.get_number_events()} events.")

    _, mag_df = man_cat.build_dataframe()
    x1, _ = info.get_table_mag_agency(mag_df)
    print(x1)

    # STEP 2: Merge catalogs and run duplicate finding tool
    cat_dicts = {'ISC-RB': isc_cat, 'ISC-GEM': iscgem_cat, 'GCMT': gcmt_cat,
                 'NEIC': usgs_cat, 'PS': ps_cat, 'MAN': man_cat}
    merged_cat = list(cat_dicts.values())[0] # start with ISC-RB
    print(f"Base catalog: {list(cat_dicts.keys())[0]}")
    time_window = 60. # seconds
    dist_window = 110. # km
    # then merge the rest in given sequence in cat_dicts
    for code, cat in list(cat_dicts.items())[1:]:
        dupfinder = DuplicateFinder(merged_cat, time_window, dist_window, 
                    logging=True)
        print(f"Merging {code} catalog...")
        merged_cat = dupfinder.merge_catalogue(cat)
        
    # Build the HDF5 Database for merged catalog
    database_file = os.path.join(DIRNAME, MERGED_FILE + ".hdf5")
    if os.path.exists(database_file):
        os.remove(database_file)
    _ = merged_cat.build_dataframe(hdf5_file=database_file)
    
    merged_db = cqt.CatalogueDB(database_file)
    agency_count = cqt.get_agency_magtype_statistics(merged_db)

    ### Clear whitespace before? ###
    origin_rules = [
        ("1900/01/01 - 2023/12/31", 
        ["ISC-GEM", "ISC-EHB", "EHB", "ISC", "IDC", "NEIC", "NEIS", "USCGS", 
        "NIED", "GCMT", "GUTE", "PAS", "PS", "MAN"])
    ]

if __name__ == '__main__':
    homogenize()