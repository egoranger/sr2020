import random

import numpy as np
from lxml import etree


class Robot(object):
    """
    An example robot object. Please override me!
    """

    def __init__(self, morphology=None):
        if morphology is not None:
            self.morphology = morphology
        else:
            self.morphology = np.ones(shape=(2, 2, 5), dtype=np.int8)

    def write_to_xml(self, root, **kwargs):
        structure = etree.SubElement(root, "Structure")
        structure.set('replace', 'VXA.VXC.Structure')
        structure.set('Compression', 'ASCII_READABLE')

        etree.SubElement(structure, "X_Voxels").text = str(self.morphology.shape[2])
        etree.SubElement(structure, "Y_Voxels").text = str(self.morphology.shape[1])
        etree.SubElement(structure, "Z_Voxels").text = str(self.morphology.shape[0])

        data = etree.SubElement(structure, "Data")
        for layer in range(self.morphology.shape[0]):
            etree.SubElement(data, "Layer").text = etree.CDATA(''.join([str(d) for d in self.morphology[layer, :, :].flatten()]))

        return structure
