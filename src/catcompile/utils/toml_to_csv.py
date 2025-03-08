import sys
import warnings
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
        max_mag = _check_list_same_elem(max_mags, raise_warning=True)
        bval = _check_list_same_elem(bsigvals, raise_warning=True)
        
        z1 = fault['Fault_Geometry']['Upper_Depth']
        z2 = fault['Fault_Geometry']['Lower_Depth']
        rake = fault['Rake'] # For future checks
        dip = fault['Fault_Geometry']['Dip'] # For future checks
        slip_rate = fault['Slip']['Value']
        slip_wt = fault['Slip']['Weight']
        df0 = DataFrame(
            [[fault['Fault_Name'], fault['Slip_Type'], 
            max_mag,
            "\n".join(f"{s}" for s in slip_rate), 
            "\n".join(f"{s:.2f}" for s in slip_wt),
            f"{z1:.0f}-{z2:.0f}",
            bval[0], bval[1], fault['Aseismic']
            ]],
            columns=col_labels)
        df_line_src = concat([df_line_src, df0], ignore_index=True)

    if output_filename is not None:
        df_line_src.to_csv(output_filename)
        print(f"Data exported successfully to {output_filename}")

    return df_line_src.to_dict()


def _slip_type_from_rake(rake_angle, tec_reg):
    """
    [For future implementation]

    Classifies given rake angle and tectonic region to rake classes according to
    Aki and Richards convention.
    
    Returns:
    `fault_type`
    """
    if abs(rake_angle) >= 180:
        raise ValueError('Invalid rake angle! Absolute value should be < 180.')

    # Fault rake classification according to rake angle (Aki & Richards)
    rake_classes = {
        # 'Dextral': (-157.5, 157.5), 'OR' inequality range
        'Sinistral': (22.5, -22.5),
        'Reverse': (112.5, 67.5),
        'Normal': (-67.5, -112.5),
        'Reverse-Sinistral': (67.5, 22.5),
        'Normal-Sinistral': (-22.5, -67.5),
        'Reverse-Dextral': (157.5, 112.5),
        'Normal-Dextral': (-112.5, -157.5)
    }

    # Map `fault_type` given in rake classification but due to 'OR' inequality 
    # in "Dextral", return it when `next()` defaults
    fault_type = next((cls for cls, (rake1, rake2) in rake_classes.items() 
                       if rake1 >= rake_angle >= rake2), "Dextral")

    return fault_type


def _check_list_same_elem(lst, raise_warning=True):
    if len(lst) == 0:
        return None  
    
    if all(element == lst[0] for element in lst):
        return lst[0]
    else:
        warnings.warn(f'Elements do not match!')
        return None


if __name__ == '__main__':
    input_f = sys.argv[1]
    output_f = sys.argv[2]

    df = toml_to_csv(input_f, output_filename=output_f)