import os
import tempfile
import pandas as pd # type: ignore
import shutil
import openquake.cat.catalogue_query_tools as cqt # type: ignore
from openquake.cat.hmg import merge # type: ignore
from catcompile.usgs_catalog_reader import UsgsCsvReader
from openquake.cat.parsers.isf_catalogue_reader import ISFReader # type: ignore
from openquake.cat.parsers.converters import (GenericCataloguetoISFParser, GenericCataloguetoGCMT, GCMTtoISFParser,) # type: ignore
from openquake.cat.isc_homogenisor import (HomogenisorPreprocessor, DynamicHomogenisor, MagnitudeConversionRule, DuplicateFinder,) # type: ignore
import warnings

END_DATE = '2025/01/31'

# Suppress warnings
warnings.filterwarnings("ignore")
# Set the base path
BASE_PATH = os.getcwd()
temp_dir = tempfile.mkdtemp()

def homogenize(isf_file,gcmt_file,phivolcs_file,isc_gem_file,usgs_file,pas_file,database_file_iscgem,
               database_file_iscrb,database_file_usgs,database_file_gcmt,database_file_PAS,
               database_file_Phivolcs,database_file_final,output_catalogue_file,output_file_path,
               output_file_path1,output_csv_path):
    """
    Homegenise the Catalogues.
    Args:
        isf_file (str): Path to the ISF file.
        gcmt_file (str): Path to the GCMT file.
        phivolcs_file (str): Path to the Phivolcs file.
        isc_gem_file (str): Path to the ISC-GEM file.
        usgs_file (str): Path to the USGS file.
        pas_file (str): Path to the Pacheco & Sykes 1992 file.
    """
    #ISCGEM
    iscgem_parser = GenericCataloguetoISFParser(isc_gem_file)
    iscgem_catalogue = iscgem_parser.parse("ISC-GEM", "ISC-GEM-CAT")

    #ISC
    isc_parser_1900_2021 = ISFReader(isf_file, 
                                     selected_origin_agencies=["ISC-GEM", "ISC-EHB", "EHB", "ISC", "IDC", "NEIC", "NEIS", "USCGS", "NIED", "GCMT", "GUTE", "CENT", "P&S","MAN"], 
                                     selected_magnitude_agencies=["ISC-GEM", "ISC-EHB", "EHB", "ISC", "IDC", "NEIC", "NEIS", "USCGS", "NIED", "GCMT", "GUTE", "CENT", "P&S","MAN"])
    isc_catalogue_1900_2021 = isc_parser_1900_2021.read_file("ISC-RB", "ISC-1900-2021")

    #USGS-COMCAT
    usgsComcat_parser = UsgsCsvReader(usgs_file)
    usgsComcat_catalogue = usgsComcat_parser.read_file("usgsComcat", "usgsComcat-CAT")

    #GCMT
    GCMT_catalogue = GCMTtoISFParser(gcmt_file).parse()

    #Pacheco & Sykes 1992
    PAS_parser = GenericCataloguetoISFParser(pas_file)
    PAS_catalogue = PAS_parser.parse("ps1992-ph", "ps1992-ph-CAT")

    #PHIVOLCS
    phivolcs_parser = GenericCataloguetoISFParser(phivolcs_file)
    phivolcs_catalogue = phivolcs_parser.parse("phivolcs", "phivolcs-CAT")

    print("ISC-GEM Catalogue 1900-2020 contains: %d events" % iscgem_catalogue.get_number_events())
    print("ISC Reviewed Bulletin Catalogue 1900-2021 contains: %d events" % isc_catalogue_1900_2021.get_number_events())
    print("USGS-NEIC Catalogue contains: %d events" % usgsComcat_catalogue.get_number_events())
    print("GCMT Catalogue contains: %d events" % GCMT_catalogue.get_number_events())
    print("Pacheco&Sykes1992 in PH Catalogue 1900-1989 contains: %d events" % PAS_catalogue.get_number_events())
    print("PHIVOLCS Catalogue 2015-2024 contains: %d events" % phivolcs_catalogue.get_number_events())

    # Build the HDF5 Database
    if os.path.exists(database_file_iscgem):
        os.remove(database_file_iscgem)
    _ = iscgem_catalogue.build_dataframe(hdf5_file=database_file_iscgem)
    db = cqt.CatalogueDB(database_file_iscgem)
    agency_count = cqt.get_agency_magtype_statistics(db)

    # Build the HDF5 Database
    if os.path.exists(database_file_iscrb):
     os.remove(database_file_iscrb)
    _ = isc_catalogue_1900_2021.build_dataframe(hdf5_file=database_file_iscrb)
    db1 = cqt.CatalogueDB(database_file_iscrb)
    agency_count = cqt.get_agency_magtype_statistics(db1)

    # Build the HDF5 Database
    if os.path.exists(database_file_usgs):
     os.remove(database_file_usgs)
    _ = usgsComcat_catalogue.build_dataframe(hdf5_file=database_file_usgs)
    db2 = cqt.CatalogueDB(database_file_usgs)
    agency_count = cqt.get_agency_magtype_statistics(db2)

    # Build the HDF5 Database
    if os.path.exists(database_file_gcmt):
     os.remove(database_file_gcmt)
    _ = GCMT_catalogue.build_dataframe(database_file_gcmt)
    db3 = cqt.CatalogueDB(database_file_gcmt)
    agency_count = cqt.get_agency_magtype_statistics(db3)

    # Build the HDF5 Database
    if os.path.exists(database_file_PAS):
     os.remove(database_file_PAS)
    _ = PAS_catalogue.build_dataframe(database_file_PAS)
    db4 = cqt.CatalogueDB(database_file_PAS)
    agency_count = cqt.get_agency_magtype_statistics(db4)

    # Build the HDF5 Database
    if os.path.exists(database_file_Phivolcs):
     os.remove(database_file_Phivolcs)
    _ = phivolcs_catalogue.build_dataframe(database_file_Phivolcs)
    db5 = cqt.CatalogueDB(database_file_Phivolcs)
    agency_count = cqt.get_agency_magtype_statistics(db5)

    # Merging Catalogue
    print('merge ISC-GEM and ISC-RB')
    merge1 = DuplicateFinder(iscgem_catalogue, 60, 110, logging=True)
    merged1Catalogue = merge1.merge_catalogue(isc_catalogue_1900_2021)

    print('merging with usgs-comcat')
    merge2 = DuplicateFinder(merged1Catalogue, 60, 110, logging=True)
    merged2Catalogue = merge2.merge_catalogue(usgsComcat_catalogue)

    print('merging with gcmt')
    merge3 = DuplicateFinder(merged2Catalogue, 60, 110, logging=True)
    merged3Catalogue = merge3.merge_catalogue(GCMT_catalogue)

    print('merging with Pacheco&Sykes')
    merge4 = DuplicateFinder(merged3Catalogue, 60, 110, logging=True)
    merged4Catalogue = merge4.merge_catalogue(PAS_catalogue)

    print('merging with Phivolcs')
    merge5 = DuplicateFinder(merged4Catalogue, 60, 110, logging=True)
    merged5Catalogue = merge5.merge_catalogue(phivolcs_catalogue)

    # Build the HDF5 Database
    if os.path.exists(database_file_final):
     os.remove(database_file_final)
    _ = merged5Catalogue.build_dataframe(database_file_final)
    db7 = cqt.CatalogueDB(database_file_final)
    agency_count = cqt.get_agency_magtype_statistics(db7)

    origin_rules = [
        ("1900/01/01 - " + END_DATE, ["ISC-GEM", "ISC-EHB", "EHB", "ISC", "IDC", "NEIC", "NEIS", "USCGS", 
                                     "NIED", "GCMT", "GUTE", "CENT", "P&S", "MAN", "ps1992-ph", "usgsComcat", 
                                     "phivolcs"])]

    """
    Weatherill (2015) Table 1. Mw conversions
    """
    def iscgem_mw(magnitude):
        """
        For Mw recorded by ISCGEM take the value with no uncertainty
        """
        return magnitude

    def iscgem_mw_sigma(magnitude):
        """
        No additional uncertainty   
        """
        return 0.0

    def gcmt_mw(magnitude):
        """
        For Mw recorded by GCMT take the value with no uncertainty
        """
        return magnitude

    def gcmt_mw_sigma(magnitude):
        """
        No additional uncertainty   
        """
        return 0.0

    def neic_mw(magnitude):
        """
        If Mw reported by NEIC,
        """
        return 1.021 * magnitude - 0.091

    def neic_mw_sigma(magnitude):
        """
        Uncertainty of 0.101 units
        """
        return 0.105

    def nied_mw(magnitude):
        """
        If Mw reported by NIED,
        """
        return 0.964 * magnitude + 0.248

    def nied_mw_sigma(magnitude):
        """
        Uncertainty of 0.11 units
        """
        return 0.11

    def isc_ms(magnitude):
        """
        If Ms reported by ISC, convert to Mw from Weatherill (2015),
        """
        if magnitude > 6.0:
            return 0.994 * magnitude + 0.1        
        else:
            return 0.616 * magnitude + 2.369

    def isc_ms_sigma(magnitude):
        """
        With Magnitude dependent uncertainty
        """
        if magnitude > 6.0:
            return 0.174
        else:
            return 0.147

    def neic_ms(magnitude):
        """
        If Ms reported by NEIC, convert to Mw from Weatherill (2015),
        """
        if magnitude > 6.47:
            return 1.005 * magnitude - 0.026       
        else:
            return 0.723 * magnitude + 1.798

    def neic_ms_sigma(magnitude):
        """
        With Magnitude dependent uncertainty
        """
        if magnitude > 6.47:
            return 0.187
        else:
            return 0.159
        
    def neic_msz(magnitude):
        """
        If Msz reported by NEIC, convert to Mw from Weatherill (2015),
        """
        if magnitude > 6.47:
            return 0.950 * magnitude + 0.359     
        else:
            return 0.707 * magnitude + 1.933

    def neic_msz_sigma(magnitude):
        """
        With Magnitude dependent uncertainty
        """
        if magnitude > 6.47:
            return 0.204
        else:
            return 0.179

    def neic_mb(magnitude):
        """
        If Mb reported by NEIC,
        """
        return 1.159 * magnitude - 0.659

    def neic_mb_sigma(magnitude):
        """
        Uncertainty of 0.283 units
        """
        return 0.283

    def isc_mb(magnitude):
        """
        If Mw reported by isc,
        """
        return 1.084 * magnitude - 0.142

    def isc_mb_sigma(magnitude):
        """
        Uncertainty of 0.317 units
        """
        return 0.317

    def pas_ms(magnitude):
        """
        For Ms recorded by p&S take the value with no uncertainty. 
        In their database Pacheco & Sykes (1992) use
        the 20-s period Ms value, which, for our purposes, we treat as
        equivalent to MW in the magnitude range 7.0 ≤ MW ≤ 8.0. (Weatherill, 2015)
        """
        return magnitude

    def pas_ms_sigma(magnitude):
        """
        0.2 additional uncertainty   
        """
        return 0.2

    def phivolcs_ms(magnitude):
        """
        own regression
        """
        if magnitude < 5.8:
            return 0.407 * magnitude + 3.225  
        else:
            return 1.470 * magnitude - 2.937

    def phivolcs_ms_sigma(magnitude):
        """
        own regression
        """
        if magnitude < 5.8:
            return 0.223
        else:
            return 0.255

    def phivolcs_mw(magnitude):
        """
        own regression
        """
        return 0.944 * magnitude + 0.362   

    def phivolcs_mw_sigma(magnitude):
        """
        own regression
        """
        return 0.104

    def phivolcs_mb(magnitude):
        """
        own regression
        """
        return 0.998 * magnitude - 0.305   


    def phivolcs_mb_sigma(magnitude):
        """
        own regression
        """
        return 0.350

    def phivolcs_mL(magnitude):
        """
        own regression
        """
        return 0.979 * magnitude + 0.711


    def phivolcs_mL_sigma(magnitude):
        """
        own regression
        """
        return 0.300
    
    rule_set_1900 = [
        MagnitudeConversionRule("ISC-GEM", "Mw", iscgem_mw, iscgem_mw_sigma),

        MagnitudeConversionRule("GCMT", "Mw", gcmt_mw, gcmt_mw_sigma),

        MagnitudeConversionRule("NEIC", "Mw", neic_mw, neic_mw_sigma),
        MagnitudeConversionRule("NEIS", "Mw", neic_mw, neic_mw_sigma),

        MagnitudeConversionRule("NIED", "Mw", nied_mw, nied_mw_sigma),

        MagnitudeConversionRule("ISC", "Ms", isc_ms, isc_ms_sigma),
        MagnitudeConversionRule("IDC", "Ms", isc_ms, isc_ms_sigma),

        MagnitudeConversionRule("NEIC", "Ms", neic_ms, neic_ms_sigma),
        MagnitudeConversionRule("NEIS", "MS", neic_ms, neic_ms_sigma),
        MagnitudeConversionRule("USCGS", "ms", neic_ms, neic_ms_sigma),
        

        MagnitudeConversionRule("NEIC", "Msz", neic_msz, neic_msz_sigma),
        MagnitudeConversionRule("NEIS", "Msz", neic_msz, neic_msz_sigma),

        MagnitudeConversionRule("NEIC", "Mb", neic_mb, neic_mb_sigma),
        MagnitudeConversionRule("NEIS", "Mb", neic_mb, neic_mb_sigma),
        MagnitudeConversionRule("USCGS", "mb", neic_mb, neic_mb_sigma),


        MagnitudeConversionRule("ISC", "Mb", isc_mb, isc_mb_sigma),
        
        MagnitudeConversionRule("P&S", "Mw", pas_ms, pas_ms_sigma),
        MagnitudeConversionRule("P&S", "Ms", pas_ms, pas_ms_sigma),
        MagnitudeConversionRule("ps1992-ph", "Ms", pas_ms, pas_ms_sigma),

        MagnitudeConversionRule("usgsComcat", "mwc", neic_mw, neic_mw_sigma),
        MagnitudeConversionRule("usgsComcat", "mww", neic_mw, neic_mw_sigma),
        MagnitudeConversionRule("usgsComcat", "mw", neic_mw, neic_mw_sigma),
        MagnitudeConversionRule("usgsComcat", "mwr", neic_mw, neic_mw_sigma),
        MagnitudeConversionRule("usgsComcat", "mwb", neic_mw, neic_mw_sigma),
        MagnitudeConversionRule("usgsComcat", "ms", neic_ms, neic_ms_sigma),
        MagnitudeConversionRule("usgsComcat", "mb", neic_mb, neic_mb_sigma),

        MagnitudeConversionRule("MAN", "Mw", phivolcs_mw, phivolcs_mw_sigma),
        MagnitudeConversionRule("MAN", "Ms", phivolcs_ms, phivolcs_ms_sigma),
        MagnitudeConversionRule("MAN", "mb", phivolcs_mb, phivolcs_mb_sigma),

        MagnitudeConversionRule("phivolcs", "Mw", phivolcs_mw, phivolcs_mw_sigma),
        MagnitudeConversionRule("phivolcs", "Ms", phivolcs_ms, phivolcs_ms_sigma),
        MagnitudeConversionRule("phivolcs", "mb", phivolcs_mb, phivolcs_mb_sigma),
        MagnitudeConversionRule("phivolcs", "mL", phivolcs_mL, phivolcs_mL_sigma),
    ]

    magnitude_rules = [("1900/01/01 - " + END_DATE, rule_set_1900)]

    preprocessor = HomogenisorPreprocessor("time")
    pp_catalogue = preprocessor.execute(merged5Catalogue, origin_rules, magnitude_rules)
    harmonisor_1900_2024 = DynamicHomogenisor(pp_catalogue, logging=True)
    homogenised_catalogue_1900_2024 = harmonisor_1900_2024.homogenise(magnitude_rules, origin_rules)
    print("Merged Catalogue 1900-2024 contains: %d events" % homogenised_catalogue_1900_2024.get_number_events())

    harmonisor_1900_2024.export_homogenised_to_csv(output_catalogue_file)
    #if os.path.exists(output_catalogue_file):
        #os.remove(output_catalogue_file)
    print("catalogue saved in cwd:", output_catalogue_file)

    with open(output_catalogue_file, "r") as input_file, open(output_file_path, "w") as output_file:
        for line in input_file:
            # Split the line into parts using commas
            parts = line.split(",")
            
            # Keep only the first 20 parts (up to the 20th comma)
            truncated_line = ",".join(parts[:20]) + "\n"
            
            # Write the modified line to the output file
            output_file.write(truncated_line)

    print("CSV file manipulation completed.")

    # Open the input and output files
    delimiter = ","  # Replace with your CSV delimiter

    with open(output_catalogue_file, "r") as input_file, open(output_file_path1, "w") as output_file:
        for line in input_file:
            # Split the line into parts using commas
            parts = line.strip().split(delimiter)
            
            # Join the first 20 parts (up to the 20th comma) and everything after it
            truncated_parts = parts[:20] + [" || ".join(parts[20:])]
            
            # Create the modified line by joining the truncated parts
            modified_line = delimiter.join(truncated_parts) + "\n"
            
            # Write the modified line to the output file
            output_file.write(modified_line)

    print("CSV file manipulation completed.")

    cleaned_file_path = output_file_path1

    df = pd.read_csv(cleaned_file_path)

    # Assuming your DataFrame is named df
    # Filter the DataFrame based on latitude and longitude conditions
    filtered_df = df[
        (df['latitude'] >= -1) & (df['latitude'] <= 22) &
        (df['longitude'] >= 116) & (df['longitude'] <= 130)]

    # Save the filtered DataFrame to a CSV file
    filtered_df.to_csv(output_csv_path, index=False)

    print("Filtered DataFrame saved to CSV:", output_csv_path)

    #remove the contents of the tempdir when you are done
    shutil.rmtree(temp_dir)
    print("Temporary directory and its contents removed.")

def main():
    # Database locations, Temporary locations for homogenising
    database_file_iscgem = os.path.join(temp_dir,"iscgem-catalogue_db.hdf5")
    database_file_iscrb = os.path.join(temp_dir,"iscrb-catalogue_db1.hdf5")
    database_file_usgs = os.path.join(temp_dir,"usgs-catalogue_db2.hdf5")
    database_file_gcmt = os.path.join(temp_dir,"gcmt-catalogue_db3.hdf5")
    database_file_PAS = os.path.join(temp_dir,"PAS-catalogue_db4.hdf5")
    database_file_Phivolcs = os.path.join(temp_dir,"Phivolcs-catalogue_db5.hdf5")
    database_file_final = os.path.join(temp_dir,"merged-catalogue_db1.hdf5")

    output_catalogue_file = f"outputs/1900-2024-merged-homogeneous_catalogue.csv"
    output_file_path1 = os.path.join(temp_dir, "1900-2024-merged-homogeneous_catalogue-cleaned.csv")

    # Database locations, input and output files
    isf_output_file = f"catalog/PH_ISF_Catalogue.isf"
    gcmt_input_file = f"catalog/gcmt-cat-1976-2024.txt"
    phivolcs_input_file = f"catalog/combined_hmtk_minM4pt5_UTF8.csv"
    isc_gem_input_file = f"catalog/isc-gem-cat-cleaned.csv"
    usgs_input_file = f"catalog/usgs_formatted.csv"
    pas_input_file = f"catalog/ps1992-ph-cat.csv"
    
    output_file_path = f"outputs/1900-2024-merged-homogeneous_catalogue-cleaned.csv"
    output_csv_path = f"outputs/1900-2024-merged-homogeneous_catalogue.csv"

    # Homogenising Catalogue
    homogenize(isf_output_file,gcmt_input_file,phivolcs_input_file, isc_gem_input_file,usgs_input_file,pas_input_file,
               database_file_iscgem,database_file_iscrb,database_file_usgs,database_file_gcmt,database_file_PAS,
                database_file_Phivolcs,database_file_final,output_catalogue_file,output_file_path,
                output_file_path1,output_csv_path)

if __name__ == "__main__":
    main()