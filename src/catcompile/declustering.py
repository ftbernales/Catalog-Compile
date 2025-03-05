import os, sys
import numpy as np
from copy import deepcopy
from openquake.hazardlib.mfd import TruncatedGRMFD
from openquake.hmtk.parsers.catalogue.csv_catalogue_parser \
    import CsvCatalogueWriter 
from openquake.hmtk.parsers.catalogue import CsvCatalogueParser
from openquake.hmtk.plotting.seismicity.catalogue_plots \
    import plot_magnitude_time_density
from openquake.hmtk.plotting.seismicity.occurrence.recurrence_plot \
    import plot_recurrence_model
from openquake.hmtk.seismicity.declusterer.dec_gardner_knopoff \
    import GardnerKnopoffType1
from openquake.hmtk.seismicity.declusterer.distance_time_windows import \
    (GardnerKnopoffWindow, GruenthalWindow, UhrhammerWindow)


def decluster_cat(catalogue_filename, output_cat_dec):
    """
    Purge aftershocks using a seismicity declustering algorithm

    :param catalogue_filename:
        Name of the .csv file of earthquake catalog
    :param output_cat_dec:
        Name of the output .csv file of declustered earthquake catalog
    """
    # Importing catalogue
    parser = CsvCatalogueParser(catalogue_filename) # From .csv to hmtk

    # Read and process the catalogue content in a variable called "catalogue"
    catalogue = parser.read_file(start_year=1900, end_year=2024)

    # How many events in the catalogue?
    print("The catalogue contains %g events" % catalogue.get_number_events())

    # What is the geographical extent of the catalogue?
    bbox = catalogue.get_bounding_box()
    print("Catalogue ranges from %.4f E to %.4f E Longitude and %.4f N to %.4f N Latitude\n" % bbox)

    catalogue.sort_catalogue_chronologically()
    print("Catalogue Sorting OK!")

    # Visualing the Catalogue
    magnitude_bin_width = 0.1  # In magnitude units
    time_bin_width = 1.0 # In years
    plot_magnitude_time_density(catalogue, magnitude_bin_width, time_bin_width)

    # Shows depth histogram every 5 km  
    # plot_depth_histogram(catalogue, 5, normalisation=True)
    """
    # Map configuration
    llon, ulon, llat, ulat = catalogue.get_bounding_box()
    map_config = {'min_lon': np.floor(llon), 'max_lon': np.ceil(ulon),
                'min_lat': np.floor(llat), 'max_lat': np.ceil(ulat), 'resolution':'i'}
    # Creating a basemap - input a cconfiguration and (if desired) a title
    basemap1 = HMTKBaseMap(map_config, 'Earthquake Catalogue') # type: ignore


    # Adding the catalogue to the basemap
    # In this case we will 'close' the figure after rendering, we do this by setting 'overlay=False'
    # This is also the default option
    # If we wanted to add another layer on top, we would set the overlay to True
    basemap1.add_catalogue(catalogue, overlay=False)
    """
    """
    The HMTK supports several methods for declustering the earthquake catalogue:

    1. Gardner & Knopoff (1974)

    2. AFTERAN (Musson, 1999)

    Others will (eventually) be added in the future

    We illustrate the use of the Gardner & Knopoff Algorithm
    """

    # Create an `instance' of the tool
    declust_method = GardnerKnopoffType1()

    # Create a configuration file
    declust_config = {"time_distance_window": GardnerKnopoffWindow(), "fs_time_prop": 1.0}

    """
    All declustering algorithms produce two outputs:

    * cluster_index = Vector indicating the number of the cluster to which the earthquake belongs (including mainshock)
    * cluster_flag = Vector indicating if the event is a foreshock (-1), mainshock (0) or aftershock (1)
    """
    cluster_index, cluster_flag = declust_method.decluster(catalogue, declust_config)

    data = np.column_stack([catalogue.get_decimal_time(),
                            catalogue.data['magnitude'],
                            catalogue.data['longitude'],
                            catalogue.data['latitude'], cluster_index, cluster_flag])
    print('\t Time\t\t  Magnitude\t Long.\t\t  Lat.\t\t     Cluster No.     Index (-1 = foreshock, 0 = mainshock, 1 = afterschock)')
    for row in data:
        print('\t%14.8f\t%6.2f\t\t%8.3f\t%8.3f\t%6.0f\t\t%6.0f' %(row[0], row[1], row[2], row[3], row[4], row[5]))

    """
    Having run the declustering algorithm you may want to remove all of the 'non-Poissonian' events (i.e. foreshocks and aftershocks) from the catalogue    
    """        
    # Copying the catalogue and saving it under a new name "catalogue_dec"(declustered catalogue) 
    catalogue_dec = deepcopy(catalogue)

    # Logical indexing: Chossing the outputs for the main events: Cluster_flag = 0 
    mainshock_flag = cluster_flag == 0 

    # Filtering the foreshocks and aftershocks in the copy of the catalogue 
    catalogue_dec.purge_catalogue(mainshock_flag)


    # Printing the number of events considered main shocks
    print('Declustering: ok')
    print("Number of events in original catalogue: %g" % catalogue.get_number_events())
    print('Number of mainshocks: %g' % catalogue_dec.get_number_events())

    # Saving the Catalogue

    if os.path.exists(output_cat_dec):
        os.remove(output_cat_dec)

    # Call the method and save the output file under the name "cat_csv"
    cat_csv = CsvCatalogueWriter(output_cat_dec) 

    # Write the purged catalogue
    cat_csv.write_file(catalogue_dec)
    print("Catalogue successfully written to %s" % output_cat_dec)

    # Analysis of Completeness
    """
    # Set up the configuration parameters
    comp_config = {'magnitude_bin': 0.5, 'time_bin': 5.0, 'increment_lock': False}

    # Calling the method
    completeness_algorithm = Stepp1971()

    # Use the catalogue and completeness configuration
    completeness_table = completeness_algorithm.completeness(catalogue_dec, comp_config)
    print('Completeness: ok')

    # Print the completeness table
    print('\n')
    print('Completeness table using Stepp method (1971)')
    print(completeness_table)
    print('\n')

    # Setting configuration for the completeness plot
    completeness_parameters = completeness_algorithm
    output_file = "outputs/Project_Completeness_Overall_Plot.png"
    if os.path.exists(output_file):
        os.remove(output_file)
    plot_stepp_1972.create_stepp_plot(completeness_parameters, output_file)
    plot_stepp_1972.create_stepp_plot(completeness_parameters, figure_size=(8, 6), 
                                    filename=output_file, filetype='png', dpi=300, ax=None)
    """
   
    # Manual setup of the completeness table
    # The hmtk allows to use a completeness table proposed by the modeller. 

    # truncate cataLogue to years 1900 and above for plotting

    cat_dec_plot = deepcopy(catalogue_dec) 
    cat_years = cat_dec_plot.data['year']
    cat_mon = cat_dec_plot.data['month'] 
    cat_day = cat_dec_plot.data['day'] 
    cat_hr = cat_dec_plot.data['hour']
    cat_min = cat_dec_plot.data['minute'] 
    cat_sec = cat_dec_plot.data['second'] 
    cat_mags = cat_dec_plot.data['magnitude']

    # cat_recent_years = cat_years >= 1619 
    cat_recent_years = cat_years >= 1900 
    cat_dec_plot.data['year'] = cat_years[cat_recent_years] 
    cat_dec_plot.data['month'] = cat_mon[cat_recent_years] 
    cat_dec_plot.data['day'] = cat_day[cat_recent_years] 
    cat_dec_plot.data['hour'] = cat_hr[cat_recent_years] 
    cat_dec_plot.data['minute'] = cat_min[cat_recent_years] 
    cat_dec_plot.data['second'] = cat_sec[cat_recent_years] 
    cat_dec_plot.data['magnitude'] = cat_mags[cat_recent_years] 

    # Table format
    completeness_table_a = np.array([[1995, 4.5],
                                    [1978, 4.9],
                                    [1971, 5.0],
                                    [1963, 5.6],
                                    [1950, 5.9],
                                    [1935, 6.0],
                                    [1924, 6.2],
                                    [1915, 6.8],
                                    [1871, 7.0],
                                    [1863, 7.5],                                 
                                    [1619, 8.2]])

    # completeness_table_a = np.array([[2017.,     2.5],
    #                                     [1998.,     3. ],
    #                                     [1995.,     3.5],
    #                                     [1997.,     4. ],
    #                                     [1989.,     4.5],
    #                                     [1965.,     5. ],
    #                                     [1937.,     5.5],
    #                                     [1915.,     6. ],
    #                                     [1892.,     6.5],
    #                                     [1884.,     7. ],
    #                                     [1884.,     7.5],
    #                                     [1817.,    8. ],
    #                                     [1619.,     8.5]])

    # completeness_table_a = np.array([[2017, 4.5],
    #                                     [2010, 4.5],
    #                                     [2003, 4.5],
    #                                     [1989, 4.5],
    #                                     [1970, 5.0],
    #                                     [1937, 6.0],
    #                                     [1915, 6.8],
    #                                     [1890, 7.0],
    #                                     [1863, 7.2],                                 
    #                                     [1619, 7.5]])

    plot_magnitude_time_density(cat_dec_plot, 0.2, 1.0,
                                completeness=completeness_table_a, figure_size=(8, 6), 
                                    filename="global_Stepp_plot", filetype='png', dpi=300, ax=None)    

    """
    ESTIMATING RECURRENCE
    Several methods are available for estimating recurrence taking into account time-dependent completeness

    1. 'Weighted' Maximum Likelihood
    2. Kijko & Smit (2012)
    3. Weichert (1980)
    4. Penalized Maximum Likelihood (Johnston et al., 1994)
    """

    recurrence_estimator = Weichert()

    # recurrence_config = {"magnitude_interval": 0.1}
    recurrence_config = {"magnitude_interval": 0.1, "referebce_magnitude": None}

    bval, sigma_b, aval, sigma_a = recurrence_estimator.calculate(catalogue_dec,
                                                                recurrence_config,
                                                                completeness_table_a)

    print("a = %.3f (+/- %.3f),  b = %.3f (+/-%.3f)" % (aval, sigma_a, bval, sigma_b))

    mfd0 = TruncatedGRMFD(4.8, 9.0, 0.1, aval, bval)
    plot_recurrence_model(mfd0, catalogue_dec, completeness_table_a, 0.1, figure_size=(8, 6), 
                                    filename="plot overall recurrence", filetype='png', dpi=300, ax=None)
    
if __name__ == "__main__":
    cat_filename = sys.argv[1]
    output_dec = sys.argv[2]
    decluster_cat(cat_filename, output_dec)