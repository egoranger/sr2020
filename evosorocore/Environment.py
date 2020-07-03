#!/usr/bin/env python3
import numpy as np
from lxml import etree

default_env = \
    {
        #True or False, use Simulator Force Field as an alternative
        "GravEnabled" : True,
        #a real number in m/s^2, negative means downwards
        "GravAcc" : -9.81,
        #True or False (False will let things fall for ever)
        "FloorEnabled" : True,
        #True or False (this way we can move the voxels)
        "VaryTempEnabled" : True,
        #a real number in degree Celsius (amplitude of temp oscillation)
        "TempAmplitude" : 0,
        #a real number in second (period of temp oscillation)
        "TempPeriod" : 0.1
    }

class Env(object):
    """Container for voxcraft-sim environment parameters."""

    def __init__(self, parameters=default_env ):

        self.GravEnabled = 1 if default_env["GravEnabled"] else 0
        self.GravAcc = default_env["GravAcc"]
        self.FloorEnabled = 1 if default_env["FloorEnabled"] else 0
        self.VaryTempEnabled = 1 if default_env["VaryTempEnabled"] else 0
        self.TempAmplitude = default_env["TempAmplitude"]
        self.TempPeriod = default_env["TempPeriod"]

    def write_to_xml( self, root ):

        env_root = etree.SubElement(root, "Environment")
        
        gravity = etree.SubElement(env_root, "Gravity")
        etree.SubElement(gravity, "GravEnabled").text = str(self.GravEnabled)
        etree.SubElement(gravity, "GravAcc").text = str(self.GravAcc)
        etree.SubElement(gravity, "FloorEnabled").text = str(self.FloorEnabled)
        
        thermal = etree.SubElement(env_root, "Thermal")
        etree.SubElement(thermal, "VaryTempEnabled").text = str(self.VaryTempEnabled)
        etree.SubElement(thermal, "TempAmplitude").text = str(self.TempAmplitude)
        etree.SubElement(thermal, "TempPeriod").text = str(self.TempPeriod)

        return env_root

default_vxc = \
    {
    "Lattice_Dim" : 0.01,
    
    }

class VXC_Wrapper(object):
    def __init__(self, lattice_dimension=0.01):
        self.lattice_dimension = lattice_dimension

    def write_to_xml(self, root, material_pallette, robot=None, **kwargs):
        VXC_root = etree.SubElement(root, "VXC", Version="0.94")

        lattice = etree.SubElement(VXC_root, "Lattice")
        etree.SubElement(lattice, "Lattice_Dim").text = str(self.lattice_dimension)
        #etree.SubElement(lattice, "X_Dim_Adj").text = "1"
        #etree.SubElement(lattice, "Y_Dim_Adj").text = "1"
        #etree.SubElement(lattice, "Z_Dim_Adj").text = "1"
        #etree.SubElement(lattice, "X_Line_Offset").text = "0"
        #etree.SubElement(lattice, "Y_Line_Offset").text = "0"
        #etree.SubElement(lattice, "X_Layer_Offset").text = "0"
        #etree.SubElement(lattice, "Y_Layer_Offset").text = "0"

        #voxel = etree.SubElement(VXC_root, "Voxel")
        #etree.SubElement(voxel, "Vox_Name").text = "BOX"
        #etree.SubElement(voxel, "X_Squeeze").text = "1"
        #etree.SubElement(voxel, "Y_Squeeze").text = "1"
        #etree.SubElement(voxel, "Z_Squeeze").text = "1"

        if material_pallette != []:
            palette = etree.SubElement(VXC_root, "Palette")
            for material in material_pallette:
                material.write_to_xml(palette)

        if robot:
            robot.write_to_xml(VXC_root)

        return VXC_root
