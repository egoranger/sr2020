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
        #Is temperature enabled?
        "TempEnabled" : False,
        #True or False (this way we can move the voxels)
        "VaryTempEnabled" : False,
        #degrees of Celsius
        "TempBase" : 25,
        #a real number in degree Celsius (amplitude of temp oscillation)
        "TempAmplitude" : 0,
        #a real number in second (period of temp oscillation)
        "TempPeriod" : 0.1
    }

class Env(object):
    """Container for voxcraft-sim environment parameters."""

    def __init__(self, parameters=default_env ):

        self.GravEnabled = 1 if parameters["GravEnabled"] else 0
        self.GravAcc = parameters["GravAcc"]
        self.FloorEnabled = 1 if parameters["FloorEnabled"] else 0
        self.TempEnabled = 1 if parameters["TempEnabled"] else 0
        self.VaryTempEnabled = 1 if parameters["VaryTempEnabled"] else 0
        self.TempBase = parameters["TempBase"]
        self.TempAmplitude = parameters["TempAmplitude"]
        self.TempPeriod = parameters["TempPeriod"]

    def write_to_xml( self, root ):

        env_root = etree.SubElement(root, "Environment")
        
        gravity = etree.SubElement(env_root, "Gravity")
        etree.SubElement(gravity, "GravEnabled").text = str(self.GravEnabled)
        etree.SubElement(gravity, "GravAcc").text = str(self.GravAcc)
        etree.SubElement(gravity, "FloorEnabled").text = str(self.FloorEnabled)
        
        thermal = etree.SubElement(env_root, "Thermal")
        etree.SubElement(thermal, "TempEnabled").text = str(self.TempEnabled)
        etree.SubElement(thermal, "VaryTempEnabled").text = str(self.VaryTempEnabled)
        etree.SubElement(thermal, "TempBase").text = str(self.TempBase)
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

        if material_pallette != []:
            palette = etree.SubElement(VXC_root, "Palette")
            for material in material_pallette:
                material.write_to_xml(palette)

        if robot:
            robot.write_to_xml(VXC_root)

        return VXC_root
