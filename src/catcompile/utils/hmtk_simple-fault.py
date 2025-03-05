import os
import toml
# Import the Parser
from openquake.hmtk.parsers.faults.fault_yaml_parser import FaultYmltoSource
from openquake.hazardlib.scalerel.wc1994 import WC1994  
from openquake.hazardlib.scalerel.strasser2010 import (StrasserInterface, 
                                                       StrasserIntraslab)
from openquake.hmtk.plotting.faults.geology_mfd_plot import plot_recurrence_models

parent_dir = r'C:\Users\AMH-L198\OneDrive - AMH Philippines, Inc\PP24.224 HRI Southlinks Clubhouse DED\06 WORKFILES\05 SHA\02 Input Files\03 Simple Fault Sources (HMTK Input)'
tec_reg = 'Intraslab' # ASC, Interface, Intraslab

# Fault mesh discretization step
mesh_spacing = 1.0 #(km)

class FaultTomltoSource(FaultYmltoSource):
    def __init__(self, toml_s):
        self.data = toml.loads(toml_s)
        if "Fault_Model" not in self.data:
            raise ValueError("Fault Model not defined in input file!")

# Read fault model
input_s = """
Fault_Model_ID = 3
Fault_Model_Name = "Faults Intraslab"
[[Fault_Model]]
ID = 24
Tectonic_Region = "Subduction Intraslab"
Fault_Name = "Mid ELT"
Rake = 89.0
Slip_Type = "Reverse"
Slip_Completeness_Factor = 1.0
Aseismic = 0.0
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 7.5
b_value = [ 0.498, 0.217 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 7.5
Minimum_Magnitude = 4.0
b_value = [ 0.498, 0.217 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 122.9185205, 17.4986682, 122.6934636, 16.5749778, 122.6708207, 16.4795967, 122.5452554, 16.07453, 122.5068311, 15.9584555, 122.497225, 15.8838949, 122.533934, 15.6696275, 122.6409732, 15.5169609, 122.8191513, 15.3579025, 123.4399938, 15.0698818, ]
Upper_Depth = 50.0
Lower_Depth = 100.0
Dip = 58.52634515
[Fault_Model.Slip]
Value = [ 3.0, 9.0, 12.0, 15.0, 22.0,]
Weight = [ 0.15, 0.2, 0.4, 0.2, 0.05,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "StrasserIntraslab",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 25
Tectonic_Region = "Subduction Intraslab"
Fault_Name = "Mid MT1"
Rake = 95.0
Slip_Type = "Reverse"
Slip_Completeness_Factor = 1.0
Aseismic = 0.99
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 8.0
b_value = [ 0.538, 0.128 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 8.0
Minimum_Magnitude = 4.0
b_value = [ 0.538, 0.128 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 119.4391950, 16.1326835, 119.4534484, 16.2045251, 119.5775318, 16.6741547, 119.6840272, 17.2746754, 119.6917148, 17.3118294, 119.7792565, 17.6815796, ]
Upper_Depth = 50.0
Lower_Depth = 100.0
Dip = 50
[Fault_Model.Slip]
Value = [ 4.0, 20.0, 25.0, 100.0, 116.0,]
Weight = [ 0.2, 0.25, 0.35, 0.1, 0.1,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "StrasserIntraslab",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 26
Tectonic_Region = "Subduction Intraslab"
Fault_Name = "Mid MT2"
Rake = 98.0
Slip_Type = "Reverse"
Slip_Completeness_Factor = 1.0
Aseismic = 0.99
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 8.0
b_value = [ 0.826, 0.087 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 8.0
Minimum_Magnitude = 4.0
b_value = [ 0.826, 0.087 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 119.5574605, 13.8144997, 119.4142105, 14.3123147, 119.4118769, 14.3206087, 119.368106, 14.4799067, 119.3442198, 14.6295042, 119.3283031, 14.9598254, 119.3279649, 15.0178116, 119.3458711, 15.5071911, 119.3536429, 15.5878214, 119.439195, 16.1326835, ]
Upper_Depth = 50.0
Lower_Depth = 100.0
Dip = 47
[Fault_Model.Slip]
Value = [ 4.0, 20.0, 25.0, 100.0, 116.0,]
Weight = [ 0.2, 0.25, 0.35, 0.1, 0.1,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "StrasserIntraslab",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 27
Tectonic_Region = "Subduction Intraslab"
Fault_Name = "Deep MT2"
Rake = 98.0
Slip_Type = "Reverse"
Slip_Completeness_Factor = 1.0
Aseismic = 0.99
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 8.0
b_value = [ 0.569, 0.119 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 8.0
Minimum_Magnitude = 4.0
b_value = [ 0.569, 0.119 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 119.9267856, 13.852843, 119.8133793, 14.2789474, 119.7971624, 14.3581614, 119.727527, 14.8398567, 119.7207185, 14.9572364, 119.7286768, 15.2417213, 119.7351775, 15.3185257, 119.7749692, 15.5989277, 119.7913002, 15.6790733, 119.9464878, 16.2595252, ]
Upper_Depth = 100.0
Lower_Depth = 250.0
Dip = 63.19709449
[Fault_Model.Slip]
Value = [ 4.0, 20.0, 25.0, 100.0, 116.0,]
Weight = [ 0.2, 0.25, 0.35, 0.1, 0.1,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "StrasserIntraslab",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 28
Tectonic_Region = "Subduction Intraslab"
Fault_Name = "Mid MT3"
Rake = 90.0
Slip_Type = "Reverse"
Slip_Completeness_Factor = 1.0
Aseismic = 0.99
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 8.0
b_value = [ 0.608, 0.110 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 8.0
Minimum_Magnitude = 4.0
b_value = [ 0.608, 0.110 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 119.8623609, 13.0664723, 119.8578561, 13.0833794, 119.5960627, 13.7254269, 119.5574605, 13.8144997, ]
Upper_Depth = 50.0
Lower_Depth = 100.0
Dip = 50
[Fault_Model.Slip]
Value = [ 4.0, 20.0, 25.0, 100.0, 116.0,]
Weight = [ 0.2, 0.25, 0.35, 0.1, 0.1,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "StrasserIntraslab",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]
[[Fault_Model]]
ID = 29
Tectonic_Region = "Subduction Intraslab"
Fault_Name = "Deep MT3"
Rake = 95.0
Slip_Type = "Reverse"
Slip_Completeness_Factor = 1.0
Aseismic = 0.99
Aspect_Ratio = 1.5
[[Fault_Model.MFD_Model]]
Model_Name = "YoungsCoppersmithCharacteristic"
MFD_spacing = 0.1
Model_Weight = 0.5
Minimum_Magnitude = 4.0
Maximum_Magnitude = 8.0
b_value = [ 0.449, 0.089 ]

[[Fault_Model.MFD_Model]]
Model_Name = "AndersonLucoArbitrary"
Model_Type = "First"
MFD_spacing = 0.1
Model_Weight = 0.5
Maximum_Magnitude = 8.0
Minimum_Magnitude = 4.0
b_value = [ 0.449, 0.089 ]


[Fault_Model.Fault_Geometry]
Fault_Typology = "Simple"
Fault_Trace = [ 120.1653237, 13.0837413, 120.1390087, 13.2079956, 120.0647634, 13.4613081, 119.9424071, 13.8023508, ]
Upper_Depth = 100.0
Lower_Depth = 300.0
Dip = 81.44093882
[Fault_Model.Slip]
Value = [ 4.0, 20.0, 25.0, 100.0, 116.0,]
Weight = [ 0.2, 0.25, 0.35, 0.1, 0.1,]
[Fault_Model.Shear_Modulus]
Value = [ 30.0,]
Weight = [ 1.0,]
[Fault_Model.Magnitude_Scaling_Relation]
Value = [ "StrasserIntraslab",]
Weight = [ 1.0,]
[Fault_Model.Scaling_Relation_Sigma]
Value = [ 0.0,]
Weight = [ 1.0,]
[Fault_Model.Displacement_Length_Ratio]
Value = [ 1.25e-5,]
Weight = [ 1.0,]

"""

reader = FaultTomltoSource(input_s)
fault_model, tectonic_region = reader.read_file(mesh_spacing)

# Construct fault source model
fault_model.build_fault_model()

# Write to an output NRML file
output_file_1 = os.path.join(parent_dir, 
                             'Simple_Faults_' + tec_reg + '_Full.xml')

fault_model.source_model.serialise_to_nrml(output_file_1)

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

fault_model.source_model.serialise_to_nrml(output_file_2)