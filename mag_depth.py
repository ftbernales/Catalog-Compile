import matplotlib.pyplot as plt
import numpy as np
import sys
from matplotlib import rcParams
from openquake.hmtk.parsers.catalogue import CsvCatalogueParser
from copy import deepcopy

rcParams['font.family'] = 'Calibri'

def mag_depth_hist(fname) -> None:
  # Importing catalogue
  catalogue_filename = fname
  parser = CsvCatalogueParser(catalogue_filename) # From .csv to hmtk

  # Read and process the catalogue content in a variable called "catalogue"
  catalogue = parser.read_file(start_year=1619, end_year=2023)
  catalogue_shallow = deepcopy(catalogue)
  catalogue_shallow.purge_catalogue(catalogue.data['depth'] <= 50.)
  catalogue_mid = deepcopy(catalogue)
  catalogue_mid.purge_catalogue(np.all([catalogue.data['depth'] > 50., 
                                        catalogue.data['depth'] <= 100.], 
                                        axis=0))
  catalogue_deep = deepcopy(catalogue)
  catalogue_deep.purge_catalogue(catalogue.data['depth'] > 100.)

  m_min = 3.5 # add autodetection of max from catalogue
  m_max = 8.0 # add autodetection of max from catalogue
  m_step = 0.5
  bin_pts = np.arange(m_min, m_max + m_step, m_step)
  hist_shallow, bins_shallow = np.histogram(catalogue_shallow['magnitude'], 
                                            bins = bin_pts)
  hist_mid, bins_mid = np.histogram(catalogue_mid['magnitude'], bins = bin_pts)
  hist_deep, bins_deep = np.histogram(catalogue_deep['magnitude'], 
                                      bins = bin_pts)

  # Plotting
  fig, ax = plt.subplots(figsize=(5.75,4.0))

  ax.bar(bin_pts[:-1], hist_shallow, bottom = hist_mid + hist_deep, 
         edgecolor='black', 
         width=m_step, align='edge')
  ax.bar(bin_pts[:-1], hist_mid, bottom = hist_deep, edgecolor='black', 
         width=m_step, align='edge')
  ax.bar(bin_pts[:-1], hist_deep, edgecolor='black', 
         width=m_step, align='edge')

  # Sum of values
  total_values = hist_shallow + hist_mid + hist_deep

  # Total values labels
  for i, total in enumerate(total_values):
    ax.text(bin_pts[i] + m_step/2, total + 100, total,
            ha = 'center', weight = 'bold', color = 'black')
  
  ax.legend(['0-50 km', '50-100 km', '>100 km'], title="Depth class:")
  ax.set_xlabel('Magnitude')
  ax.set_ylabel('Number of events')
  plt.title('Magnitude-Depth Distribution', size=12, fontweight='bold')
  fig.tight_layout()
  plt.show()

if __name__ == '__main__':
  fname = sys.argv[1]
  mag_depth_hist(fname)