import sys
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

plt.rcParams["font.family"] = "Calibri"

def plot_disagg_M_R_eps(disagg_results, mag_bin_width, dist_bin_width):
    IM = 'PGA'
    RP = 10000
    df = pd.read_excel(disagg_results, sheet_name=None, skiprows=1)
    df_disagg = df.get(IM)
    df_data = df_disagg.loc[df_disagg['eps'] == 0] # this may be buggy if not 0

    eps = np.array(pd.unique(df_disagg['eps']))
    eps_list = np.unique(eps)
    num_eps = len(eps_list)

    mag = np.array(df_data['mag']) - mag_bin_width/2.
    dist = np.array(df_data['dist']) - dist_bin_width/2.
    aroe = np.array(df_data['ARoE'])

    # Get bin widths to get length and width of bars
    d_mag = 0.75*(mag_bin_width * np.ones(len(mag)))
    d_dist = 0.75*(dist_bin_width * np.ones(len(dist)))

    fig = plt.figure(figsize=(5.75,3.3))
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel('Distance R (km)', fontsize=10)
    ax.set_ylabel('Magnitude', fontsize=10)
    ax.set_zlabel('Contribution (%)', fontsize=10, rotation=90)
    ax.zaxis.set_rotate_label(False)
    ax.zaxis._axinfo['juggled'] = (1, 2, 0)

    ax.tick_params(axis='x', labelsize=9)
    ax.tick_params(axis='y', labelsize=9)
    ax.tick_params(axis='z', labelsize=9)

    # Loop over all coord values and then stack the bars for similar locations
    # colors = cm.tab20(np.linspace(0, 1, num_eps))
    colors = ['b', 'r', 'y'] # extend for arbitrary number of eps bins
    zpos = np.zeros_like(aroe)
    legend_elements = []
    for i, ep in enumerate(eps_list):
        d_aroe = np.array(df_disagg.loc[(df_disagg['eps'] == ep), 'ARoE'])
        ax.bar3d(dist, mag, zpos, d_dist, d_mag, d_aroe,
                color=colors[i], zsort='average', alpha=0.7, shade=True)
        legend_elements.append(mpatches.Patch(facecolor=colors[i],
                                label=f"\u03B5 = {ep:.2f}"))
        zpos += d_aroe 

    fig.legend(handles=legend_elements, loc="lower center", borderaxespad=0.,
                ncol=num_eps)
    plt.tight_layout(rect=[0, 0.05, 1.1, 1])
    fig.suptitle(f"Disaggregation Plot of {RP:,d}-year {IM}", 
                    fontsize=14, fontweight='bold')
    plt.savefig(f'disagg_M-R-eps_{RP:,d}-yr_{IM}.svg')


if __name__ == "__main__":
    disagg_results = '(SHA) Disaggregation Plots (M-R-Eps) R0 2022.12.07.xlsx'
    mag_bin_width = 0.3
    dist_bin_width = 20.
    
    plot_disagg_M_R_eps(disagg_results, mag_bin_width, dist_bin_width)