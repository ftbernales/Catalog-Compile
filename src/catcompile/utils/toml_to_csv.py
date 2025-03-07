import os, sys
import toml
from pandas import DataFrame, concat
from openquake.hmtk.parsers.faults.fault_yaml_parser import FaultYmltoSource


def toml_to_csv(toml_file, output_filename=None):
    """
    Converts line source toml to csv file 

    Returns a dictionary of Line Source attributes
    """
    reader = FaultYmltoSource(toml_file)
    fault = reader.data
    col_labels = ['Source', 'Type', 'Mw', 'Slip Rate (mm/yr)', 'Weight',
                  'Depth (km)', 'b', 'sig_b', 'Aseismic Ratio']
    df_line_src = DataFrame(columns=col_labels)

    for fault in reader.data["Fault_Model"]:
        max_mags = []
        bsigvals = []
        for mfd_model in fault['MFD_Model']:
            max_mags.append(mfd_model['Maximum_Magnitude'])
            bsigvals.append(mfd_model['b_value'])
        max_mag = _check_list_same_elem(max_mags)
        bval = _check_list_same_elem(bsigvals)
        
        z1 = fault['Fault_Geometry']['Upper_Depth']
        z2 = fault['Fault_Geometry']['Lower_Depth']
        df0 = DataFrame([[fault['Fault_Name'], fault['Slip_Type'], 
                        max_mag,
                        fault['Slip']['Value'], fault['Slip']['Weight'],
                        f"{z1:.0f}-{z2:.0f}",
                        bval[0], bval[1], fault['Aseismic']
                        ]],
                        columns=col_labels)
        df_line_src = concat([df_line_src, df0], ignore_index=True)

    if output_filename is not None:
        df_line_src.to_csv(output_filename)
        print(f"Data exported successfully to {output_filename}")

    return df_line_src.to_dict()


def _slip_type_from_rake(rake_angle):
    pass

def _check_list_same_elem(lst):
    if len(lst) == 0:
        return None  
    
    if all(element == lst[0] for element in lst):
        return lst[0]
    else:
        return None

# def 
# raise warning if Maximum Magnitude and b-value/sig_b is not same in MFD_Model


if __name__ == '__main__':
    input_f = sys.argv[1]
    output_f = sys.argv[2]

    df = toml_to_csv(input_f, output_filename=output_f)