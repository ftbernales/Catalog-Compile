import os
import toml
# Import the Parser
from openquake.hmtk.parsers.faults.fault_yaml_parser import FaultYmltoSource
from openquake.hazardlib.scalerel.wc1994 import WC1994  
from openquake.hazardlib.scalerel.strasser2010 import (StrasserInterface, 
                                                       StrasserIntraslab)
from openquake.hmtk.plotting.faults.geology_mfd_plot import plot_recurrence_models

parent_dir = r'C:\Users\AMH-L198\Documents'
tec_reg = 'ASC' # ASC, Interface, Intraslab

# Fault mesh discretization step
mesh_spc = 3.0 #(km)

class FaultTomltoSource(FaultYmltoSource):
    def __init__(self, toml_s):
        self.data = toml.loads(toml_s)
        if "Fault_Model" not in self.data:
            raise ValueError("Fault Model not defined in input file!")

# Read fault model
input_s = """
Fault_Model_ID = 1
Fault_Model_Name = "Faults ASC"
[[Fault_Model]]
ID = 1
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "West Valley Fault"
Rake = 0.0
Slip_Type = "Strikeslip"
Slip_Completeness_Factor = 1.0
Aseismic = 0.02
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.2
b_value = [ 1.063, 0.136 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 7.2
Minimum_Magnitude = 4.0
b_value = [ 1.063, 0.136 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 121.05317, 14.17022, 121.04138, 14.19176, 121.04619, 14.21735, 121.0401, 14.25357, 121.04045, 14.32828, 121.04746, 14.42331, 121.05742, 14.52583, 121.08024, 14.63252, 121.13836, 14.76059, 121.14724, 14.79274, 121.16048, 14.85894, 121.18249, 14.91852, 121.19441, 14.96467, 121.2011, 14.99834, ]
Upper_Depth = 0.0
Lower_Depth = 30.0
Dip = 70.0
[Fault_Model.Slip]
Value = [ 3.0, 6.0, 10.0, 12.0, 20.0,]
Weight = [ 0.15, 0.25, 0.25, 0.25, 0.1,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 2
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "East Valley Fault"
Rake = 0.0
Slip_Type = "Strikeslip"
Slip_Completeness_Factor = 1.0
Aseismic = 0.02
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 6.3
b_value = [ 1.063, 0.136 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 6.3
Minimum_Magnitude = 4.0
b_value = [ 1.063, 0.136 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 121.20491, 14.79082, 121.17927, 14.75669, 121.16974, 14.73977, 121.15224, 14.71355, 121.14882, 14.71038, 121.14355, 14.69807, 121.14268, 14.69329, 121.14029, 14.688054, 121.13921, 14.68511, ]
Upper_Depth = 0.0
Lower_Depth = 30.0
Dip = 90.0
[Fault_Model.Slip]
Value = [ 3.0, 7.5, 10.0, 12.0, 20.0,]
Weight = [ 0.2, 0.25, 0.25, 0.25, 0.05,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 3
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "PFZ Infanta Segment"
Rake = 0.0
Slip_Type = "Strikeslip"
Slip_Completeness_Factor = 1.0
Aseismic = 0.42
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.6
b_value = [ 0.903, 0.027 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 7.6
Minimum_Magnitude = 4.0
b_value = [ 0.903, 0.027 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 121.39853, 15.36476, 121.48211, 15.1812, 121.52324, 15.0622, 121.57806, 14.94424, 121.60955, 14.61168, 121.63394, 14.50044, 121.67354, 14.37663, ]
Upper_Depth = 0.0
Lower_Depth = 30.0
Dip = 90.0
[Fault_Model.Slip]
Value = [ 18.0, 29.0, 35.0, 40.0, 49.0,]
Weight = [ 0.1, 0.25, 0.25, 0.3, 0.1,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 4
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "PFZ Ragay-Guinyangan Segment"
Rake = 0.0
Slip_Type = "Strikeslip"
Slip_Completeness_Factor = 1.0
Aseismic = 0.0
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.6
b_value = [ 0.903, 0.027 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 7.6
Minimum_Magnitude = 4.0
b_value = [ 0.903, 0.027 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 121.6756, 14.3751, 121.73456, 14.30566, 121.96547, 14.0803, 122.20898, 13.8861, 122.62805, 13.51448, 122.72493, 13.31817, ]
Upper_Depth = 0.0
Lower_Depth = 30.0
Dip = 90.0
[Fault_Model.Slip]
Value = [ 18.0, 29.0, 35.0, 40.0, 49.0,]
Weight = [ 0.1, 0.25, 0.25, 0.3, 0.1,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 5
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "PFZ Digdig Segment"
Rake = 0.0
Slip_Type = "Strikeslip"
Slip_Completeness_Factor = 1.0
Aseismic = 0.0
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.9
b_value = [ 0.903, 0.027 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 7.9
Minimum_Magnitude = 4.0
b_value = [ 0.903, 0.027 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 121.39245, 15.37601, 121.3584, 15.41865, 121.32292, 15.44778, 121.31535, 15.47553, 121.18324, 15.60631, 121.1408, 15.66646, 121.09973, 15.71486, 121.07034, 15.75953, 121.01583, 15.87386, 120.97029, 15.95648, 120.94799, 16.05412, 120.91479, 16.11715, 120.88156, 16.2461, 120.89618, 16.30194, ]
Upper_Depth = 0.0
Lower_Depth = 30.0
Dip = 90.0
[Fault_Model.Slip]
Value = [ 8.0, 17.0, 22.0, 27.0, 37.0,]
Weight = [ 0.3, 0.5, 0.1, 0.05, 0.05,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 6
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "Lubang Fault"
Rake = 0.0
Slip_Type = "Strikeslip"
Slip_Completeness_Factor = 1.0
Aseismic = 0.16
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.7
b_value = [ 0.819, 0.074 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 7.7
Minimum_Magnitude = 4.0
b_value = [ 0.819, 0.074 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 121.47893, 13.402810, 121.28563, 13.477450, 121.04801, 13.525000, 120.51579, 13.581080, 120.32761, 13.571380, ]
Upper_Depth = 0.0
Lower_Depth = 30.0
Dip = 90.0
[Fault_Model.Slip]
Value = [ 5.0, 15.0, 21.0, 40.0, 61.0,]
Weight = [ 0.1, 0.3, 0.3, 0.2, 0.1,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 7
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "Aglubang River Fault"
Rake = 0.0
Slip_Type = "Strikeslip"
Slip_Completeness_Factor = 1.0
Aseismic = 0.3
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.2
b_value = [ 0.961, 0.084 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 7.2
Minimum_Magnitude = 4.0
b_value = [ 0.961, 0.084 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 121.19118, 13.222320, 121.20660, 13.002800, ]
Upper_Depth = 0.0
Lower_Depth = 30.0
Dip = 90.0
[Fault_Model.Slip]
Value = [ 0.5, 1.0, 1.5,]
Weight = [ 0.2, 0.6, 0.2,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = "008"
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "Central Mindoro Fault"
Rake = 71
Slip_Type = "Reverse"
Slip_Completeness_Factor = 1.0
Aseismic = 0.4
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.5
b_value = [ 0.961, 0.084 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 7.5
Minimum_Magnitude = 4.0
b_value = [ 0.961, 0.084 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 121.45795, 12.519770, 121.40350, 12.664340, 121.34322, 12.690310, 121.25761, 12.821760, 121.24708, 12.874530, 121.21941, 12.927120, 121.20009, 13.002050, 121.11995, 13.155690, 121.09982, 13.221570, ]
Upper_Depth = 0.0
Lower_Depth = 30.0
Dip = 65.0
[Fault_Model.Slip]
Value = [ 4.0, 5.0, 6.0,]
Weight = [ 0.2, 0.6, 0.2,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = "009"
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "Southern Mindoro Fault"
Rake = 71
Slip_Type = "Reverse"
Slip_Completeness_Factor = 1.0
Aseismic = 0.2
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.0
b_value = [ 0.961, 0.084 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 7.0
Minimum_Magnitude = 4.0
b_value = [ 0.961, 0.084 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 121.20909, 12.237430, 121.20365, 12.406240, 121.32638, 12.483470, 121.40900, 12.584350, ]
Upper_Depth = 0.0
Lower_Depth = 30.0
Dip = 55.0
[Fault_Model.Slip]
Value = [ 0.5, 1.0, 1.5,]
Weight = [ 0.2, 0.6, 0.2,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 8
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "PFZ Sibuyan Sea"
Rake = 0.0
Slip_Type = "Strikeslip"
Slip_Completeness_Factor = 1.0
Aseismic = 0.4
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.6
b_value = [ 0.903, 0.027 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 7.6
Minimum_Magnitude = 4.0
b_value = [ 0.903, 0.027 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 121.97547, 13.61414, 122.2884, 13.30646, 122.51214, 13.13956, 122.75906, 12.94778, 123.11205, 12.68419, 123.23809, 12.61539, 123.28803, 12.5904, 123.32621, 12.58382, 123.3991, 12.54171, 123.44238, 12.52231, 123.46689, 12.50832, 123.48212, 12.49608, 123.50114, 12.48442, 123.51585, 12.47292, 123.53488, 12.46342, ]
Upper_Depth = 0.0
Lower_Depth = 30.0
Dip = 90.0
[Fault_Model.Slip]
Value = [ 5.0, 10.0, 15.0,]
Weight = [ 0.2, 0.6, 0.2,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 9
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "PFZ Burias"
Rake = 0.0
Slip_Type = "Strikeslip"
Slip_Completeness_Factor = 1.0
Aseismic = 0.3
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.4
b_value = [ 0.903, 0.027 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 7.4
Minimum_Magnitude = 4.0
b_value = [ 0.903, 0.027 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 123.40048, 12.707770, 123.26678, 12.876250, 123.22021, 12.910360, 123.15550, 12.963030, 123.10962, 13.035490, 123.06986, 13.117040, 122.95419, 13.248440, 122.66576, 13.636220, 122.30961, 13.970800, ]
Upper_Depth = 0.0
Lower_Depth = 30.0
Dip = 90.0
[Fault_Model.Slip]
Value = [ 3.5, 7.0, 10.5,]
Weight = [ 0.2, 0.6, 0.2,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 10
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "PFZ Masbate"
Rake = 0.0
Slip_Type = "Strikeslip"
Slip_Completeness_Factor = 1.0
Aseismic = 0.5
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.6
b_value = [ 0.903, 0.027 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 7.6
Minimum_Magnitude = 4.0
b_value = [ 0.903, 0.027 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 123.40911, 12.702390, 123.79823, 12.279500, 123.87545, 12.188710, 123.98945, 12.022920, 124.02105, 11.992230, 124.09332, 11.874110, 124.14966, 11.806730, ]
Upper_Depth = 0.0
Lower_Depth = 30.0
Dip = 90.0
[Fault_Model.Slip]
Value = [ 5.0, 7.5, 10.0, 15.0, 22.5,]
Weight = [ 0.1, 0.2, 0.3, 0.3, 0.1,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 11
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "Tablas Fault"
Rake = 80
Slip_Type = "Reverse"
Slip_Completeness_Factor = 1.0
Aseismic = 0.2
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.0
b_value = [ 0.796, 0.078 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 7.0
Minimum_Magnitude = 4.0
b_value = [ 0.796, 0.078 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 122.12371, 12.627770, 122.10566, 12.358880, 122.02302, 12.234820, ]
Upper_Depth = 0.0
Lower_Depth = 30.0
Dip = 35.0
[Fault_Model.Slip]
Value = [ 2.5, 5.0, 7.5,]
Weight = [ 0.2, 0.6, 0.2,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 12
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "Legazpi Lineament"
Rake = 0.0
Slip_Type = "Strikeslip"
Slip_Completeness_Factor = 1.0
Aseismic = 0.0
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.2
b_value = [ 0.903, 0.027 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 7.2
Minimum_Magnitude = 4.0
b_value = [ 0.903, 0.027 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 123.77217, 13.117650, 123.67447, 13.135480, 123.35893, 13.292440, 123.20650, 13.401250, 122.83100, 13.642700, ]
Upper_Depth = 0.0
Lower_Depth = 30.0
Dip = 90.0
[Fault_Model.Slip]
Value = [ 7.5, 15.0, 22.5,]
Weight = [ 0.2, 0.6, 0.2,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 13
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "Abra River Fault"
Rake = 90
Slip_Type = "Sinistral-Reverse,"
Slip_Completeness_Factor = "1,"
Aseismic = 0.3
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.5
b_value = [ 0.903, 0.027 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.5
b_value = [ 0.903, 0.027 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 120.70902, 16.959460, 120.68927, 16.982800, 120.67911, 17.005280, 120.67391, 17.156810, 120.68112, 17.226190, 120.72814, 17.570040, 120.73631, 17.788760, 120.74927, 17.840150, ]
Upper_Depth = 0
Lower_Depth = 30
Dip = 65.0
[Fault_Model.Slip]
Value = [ 2.0, 1.0, 3.0,]
Weight = [ 0.6, 0.2, 0.2,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 14
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "Ambuklao Fault"
Rake = 0
Slip_Type = "Sinistral-Reverse,"
Slip_Completeness_Factor = "1,"
Aseismic = 0.1
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.3
b_value = [ 0.903, 0.027 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.3
b_value = [ 0.903, 0.027 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 120.89861, 16.318940, 120.86618, 16.422170, 120.84832, 16.504020, 120.85033, 16.538210, 120.81387, 16.678280, 120.81365, 16.709320, 120.78948, 16.744910, 120.75867, 16.850280, 120.75591, 16.884480, 120.71668, 16.977260, ]
Upper_Depth = 0
Lower_Depth = 30
Dip = 60
[Fault_Model.Slip]
Value = [ 18.6, 9.0, 27.0,]
Weight = [ 0.6, 0.2, 0.2,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 15
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "Hapap Fault"
Rake = 135
Slip_Type = "Sinistral-Reverse,"
Slip_Completeness_Factor = "1,"
Aseismic = 0.1
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.6
b_value = [ 0.903, 0.027 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.6
b_value = [ 0.903, 0.027 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 121.25623, 17.427680, 121.26311, 17.388100, 121.21525, 17.167410, 121.10091, 17.031810, 121.05040, 16.999900, 120.94936, 16.508010, 120.91745, 16.425580, 120.95467, 16.276680, 120.94936, 16.210210, ]
Upper_Depth = 0
Lower_Depth = 30
Dip = 60
[Fault_Model.Slip]
Value = [ 8.8, 4.5, 13.5,]
Weight = [ 0.6, 0.2, 0.2,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = "018"
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "Casiguran-Dinalungan-Dipaculao-Palanan-Dinapigue Fault"
Rake = 45
Slip_Type = "Reverse,"
Slip_Completeness_Factor = "1,"
Aseismic = 0.6
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.8
b_value = [ 0.864, 0.064 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.8
b_value = [ 0.864, 0.064 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 122.56709, 17.22497, 122.53184, 17.11398, 122.51407, 17.02921, 122.42027, 16.795, 122.35276, 16.66631, 122.27884, 16.52889, 122.24539, 16.50847, 122.2445, 16.50794, 122.23782, 16.50273, 122.23497, 16.50018, 122.23337, 16.49898, 122.23123, 16.49773, 122.23043, 16.49722, 122.22934, 16.49629, 122.22827, 16.49516, 122.2199, 16.48483, 122.21485, 16.47563, 122.20921, 16.46671, 122.18805, 16.44185, 122.17535, 16.42227, 122.14058, 16.38058, 122.13707, 16.37685, 122.13219, 16.36584, 122.11972, 16.35061, 122.1171, 16.34593, 122.11117, 16.34018, 122.10811, 16.33644, 122.10346, 16.32695, 122.10192, 16.32429, 122.10035, 16.31763, 122.0971, 16.30661, 122.09626, 16.29142, 122.09415, 16.28329, 122.08974, 16.27273, 122.06984, 16.23228, 122.06507, 16.22774, 122.06367, 16.22572, 122.06078, 16.22295, 122.05128, 16.21598, 122.04653, 16.21282, 122.04151, 16.20914, 122.03597, 16.2058, 122.03152, 16.20206, 122.02872, 16.19831, 122.02434, 16.19324, 122.01823, 16.18711, 122.01309, 16.18081, 122.00885, 16.17713, 122.00586, 16.17355, 122.00214, 16.16974, 121.93262, 16.10504, 121.82513, 16.03337, 121.766, 15.9891, 121.71269, 15.94569, 121.65938, 15.90957, ]
Upper_Depth = 0
Lower_Depth = 30
Dip = 35.0
[Fault_Model.Slip]
Value = [ 2.0, 1.0, 4.0,]
Weight = [ 0.6, 0.2, 0.2,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = "019"
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "East Cordillera Fault"
Rake = 90
Slip_Type = "Reverse,"
Slip_Completeness_Factor = "1,"
Aseismic = 0.1
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.4
b_value = [ 0.903, 0.027 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.4
b_value = [ 0.903, 0.027 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 121.5398, 17.3471, 121.54085, 17.34125, 121.54115, 17.33413, 121.53978, 17.32646, 121.5399, 17.32338, 121.53919, 17.31748, 121.5388, 17.31332, 121.53843, 17.3081, 121.53876, 17.29888, 121.53966, 17.29547, 121.54019, 17.27047, 121.53847, 17.2692, 121.5393, 17.26328, 121.53965, 17.25888, 121.54435, 17.22028, 121.5434, 17.20535, 121.55118, 17.15992, 121.55538, 17.15117, 121.56189, 17.07033, 121.56344, 17.01522, 121.56492, 17.00993, 121.56241, 16.94213, 121.55677, 16.92338, 121.54983, 16.90761, 121.53345, 16.87568, 121.50695, 16.83453, 121.48826, 16.80829, 121.45973, 16.75968, 121.44274, 16.72736, 121.436, 16.71831, 121.4093, 16.67887, ]
Upper_Depth = 0
Lower_Depth = 30
Dip = 35.0
[Fault_Model.Slip]
Value = [ 4.0, 2.0, 6.0,]
Weight = [ 0.6, 0.2, 0.2,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 16
Tectonic_Region = "Active Shallow Crust"
Fault_Name = "East Zambales Fault"
Rake = 0
Slip_Type = "Reverse-Sinistral,"
Slip_Completeness_Factor = "1,"
Aseismic = 0.2
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.4
b_value = [ 0.746, 0.070 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.4
b_value = [ 0.746, 0.070 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 120.16073, 16.01774, 120.1805, 15.97077, 120.19776, 15.93585, 120.25069, 15.85277, 120.2988, 15.75283, 120.31484, 15.71791, 120.34691, 15.65171, 120.35808, 15.61314, 120.37659, 15.5734, 120.39382, 15.53656, 120.42552, 15.45303, 120.44972, 15.39855, 120.46272, 15.37676, ]
Upper_Depth = 0
Lower_Depth = 30
Dip = 65
[Fault_Model.Slip]
Value = [ 2.0, 1.0, 3.0,]
Weight = [ 0.6, 0.2, 0.2,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "WC1994",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]

"""

reader = FaultTomltoSource(input_s)
fault_model, tectonic_region = reader.read_file(mesh_spc)

# Construct fault source model
fault_model.build_fault_model()

# Write to an output NRML file
output_file_1 = os.path.join(parent_dir, 
                             'Simple_Faults_' + tec_reg + '_Full.xml')

fault_model.source_model.serialise_to_nrml(output_file_1, mesh_spacing=mesh_spc)

# COLLAPSED 
# Scaling relation for export
msr = {'ASC': WC1994(), 
       'Interface': StrasserInterface(), 
       'Intraslab': StrasserIntraslab()}
output_msr = msr[tec_reg]
# fault_model, tectonic_region = reader.read_file(mesh_spacing)
# Construct the fault source model - collapsing the branches
fault_model.build_fault_model(collapse=True, rendered_msr=output_msr)

# Write to an output NRML file
output_file_2 = os.path.join(parent_dir, 
                             'Simple_Faults_' + tec_reg + '_Collapsed.xml')

fault_model.source_model.serialise_to_nrml(output_file_2, mesh_spacing=mesh_spc)