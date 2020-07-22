#!/usr/bin/env python3

from lxml import etree

default_sim = \
    {
        #"FitnessFunction" : "UNDEFINED",
        #0.0 ~ 1.0, how safe do we want to have the time step 
        #1.0 if everything is fine, 0.5 if we want a safer run
        "DtFrac" : 0.9,
        #0.0 ~ 1.0, if we want voxels to jiggle a lot, we use 0.0, if we want to calm down, 1.0
        "BondDampingZ" : 0.1,
        #0.0 ~ 1.0, if we want voxels bouncing on the floor, we use 0.0, otherwise 1.0    
        "ColDampingZ" : 1.0,
        #0.0 ~ 1.0, if we want to dump everything in simulation, we use 1.0, otherwise 0.0
        "SlowDampingZ" : 1.0, 
        #number of seconds to run the experiment
        "StopConditionFormula" : 1,
        #number of steps per which we want to record voxels (e.g. 100 means every 100 steps)
        "RecordStepSize" : 100,
        #True or False, True if want to record voxels, else False
        "RecordVoxel" : True,
        #True or False, True if we want to record voxel links, else False
        "RecordLink" : False,
        #True or False, True if we want voxel collisions, else False
        "EnableCollision" : True,
        #"EnableAttach" : False,
        #"AttachCondition" : "UNDEFINED",
        #integer, number of steps in which there will be a special damping
        "SafetyGuard" : 500,
        #"ForceField" : "UNDEFINED",
        #True or False, True if we want to enable signals, else False
        "EnableSignals" : False,
        #True or False, True if we want to enable Cilia, else False
        "EnableCilia" : False,
        #True or False, True if we want to save position of all voxels
        "SavePositionOfAllVoxels" : False,
        #real number, sometimes we need to count how many pairs of Target voxels are close to each other
        "MaxDistInVoxelLengthsToCountAsPair" : 0
    }

class Sim(object):
    """Container for voxcraft-sim simulation parameters."""

    def __init__(self, parameters=default_sim):

        self.DtFrac = parameters["DtFrac"]
        self.BondDampingZ = parameters["BondDampingZ"]
        self.ColDampingZ = parameters["ColDampingZ"]
        self.SlowDampingZ = parameters["SlowDampingZ"]
        self.StopConditionFormula = parameters["StopConditionFormula"]
        self.RecordStepSize = parameters["RecordStepSize"]
        self.RecordVoxel = 1 if parameters["RecordVoxel"] else 0
        self.RecordLink = 1 if parameters["RecordLink"] else 0
        self.EnableCollision = 1 if parameters["EnableCollision"] else 0
        self.SafetyGuard = parameters["SafetyGuard"]
        self.EnableSignals = 1 if parameters["EnableSignals"] else 0
        self.EnableCilia = 1 if parameters["EnableCilia"] else 0
        self.SavePositionOfAllVoxels = 1 if parameters["SavePositionOfAllVoxels"] else 0
        self.MaxDistInVoxelLengthsToCountAsPair = parameters["MaxDistInVoxelLengthsToCountAsPair"]

    def write_to_xml(self, root, run_dir=None, individual=None, fitness_file_str=None, seed=0, **kwargs):
        sim_root = etree.SubElement(root, "Simulator")

        integration = etree.SubElement(sim_root, "Integration")
        etree.SubElement(integration, "DtFrac").text = str(self.DtFrac)

        #damping = etree.SubElement(sim_root, "Damping")
        #etree.SubElement(damping, "BondDampingZ").text = str(self.BondDampingZ)
        #etree.SubElement(damping, "ColDampingZ").text = str(self.ColDampingZ)
        #etree.SubElement(damping, "SlowDampingZ").text = str(self.SlowDampingZ)

        stop_condition = etree.SubElement(sim_root, "StopCondition")
        stop_condition_formula = etree.SubElement(stop_condition, "StopConditionFormula")
        mtsub = etree.SubElement(stop_condition_formula, "mtSUB")
        etree.SubElement(mtsub, "mtVAR").text = "t"
        etree.SubElement(mtsub, "mtCONST").text = str(self.StopConditionFormula)
       
        record_history = etree.SubElement(sim_root, "RecordHistory")
        etree.SubElement(record_history, "RecordStepSize").text = str(self.RecordStepSize)
        etree.SubElement(record_history, "RecordVoxel").text = str(self.RecordVoxel) 
        etree.SubElement(record_history, "RecordLink").text = str(self.RecordLink)

        #attachdetach = etree.SubElement(sim_root, "AttachDetach")
        #etree.SubElement(attachdetach, "EnableCollision").text = str(self.EnableCollision)
        #etree.SubElement(attachdetach, "SafetyGuard").text = str(self.SafetyGuard)

        #etree.SubElement(sim_root, "EnableSignals").text = str(self.EnableSignals)
        #etree.SubElement(sim_root, "EnableCilia").text = str(self.EnableCilia)
        #etree.SubElement(sim_root, "SavePositionOfAllVoxels").text = str(self.SavePositionOfAllVoxels)
        #etree.SubElement(sim_root, "MaxDistInVoxelLengthsToCountAsPair").text = str(self.MaxDistInVoxelLengthsToCountAsPair)
        
            

        return sim_root
