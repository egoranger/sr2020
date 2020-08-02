from lxml import etree

default_mat = \
    {
        #material id
        "id" : 0,
        #material name
        "Name" : "Default name",
        #material color, rgba
        "color" : (1,0,1,1),
        #True if we want voxels of this mat. to be target, else False
        "isTarget" : None, #False
        #True if we want to measure voxels made by this mat. in all MathTree fcs(), else False
        "isMeasured" : None, #True
        #True if we don't want this material to move at all, else False
        "Fixed" : None, #False
        #True if we want attachment happen to this mat., else False
        "Sticky" : None, #False
        #real number, 0 if we don't want cilia to happen
        "Cilia" : None, #0
        #True if this mat. can generate periodic signals, else False
        "isPaceMaker" : None, #False
        #real number, period between two signal
        "PaceMakerPeriod" : None, #0
        #0.0 ~ 1.0, decay ratio of signal propagation in other parts of the body
        "signalValueDecay" : None, #0.9
        #real number/sec delay of signal at every stop
        "signalTimeDelay" : None, #0.03
        #real number how long does voxel stay inactive after sending signal
        "inactivePeriod" : None, #0.03
        #False simple elastic model, True for perfectly elastic mat.
        "MatModel" : None, #False
        #real number in Pascal, Young's Modulus
        "Elastic_Mod" : None, #0
        #real number in Pascal, if stress > threshold -> mat. will fail by fracture
        "Fail_Stress" : None, #0
        #real number in kg/m^3, e.g. rubber's density 1.5e+3 kg/m^3
        "Density" : None, #0
        #0.0 ~ 0.5
        "Poissons_Ratio" : None, #0
        #small real number in 1/degree Celsius
        "CTE" : None, #0
        #0.0 ~ 5.0, static frictional coefficient
        "uStatic" : None, #0
        #0.0 ~ 1.0, kinetic frictional coefficient
        "uDynamic" : None #0
    }

class Material(object):
    """
    base class for materials.
    Please override if you need special attributes such as actuation or cilia
    """

    def __init__( self, parameters=default_mat ):
        self.id = parameters["id"]
        self.Name = parameters["Name"]
        self.color = parameters["color"]
        self.isTarget = parameters["isTarget"]
        self.isMeasured = parameters["isMeasured"]
        self.Fixed = parameters["Fixed"]
        self.Sticky = parameters["Sticky"]
        self.Cilia = parameters["Cilia"]
        self.isPaceMaker = parameters["isPaceMaker"]
        self.PaceMakerPeriod = parameters["PaceMakerPeriod"]
        self.signalValueDecay = parameters["signalValueDecay"]
        self.signalTimeDelay = parameters["signalTimeDelay"]
        self.inactivePeriod = parameters["inactivePeriod"]
        self.MatModel = parameters["MatModel"]
        self.Elastic_Mod = parameters["Elastic_Mod"]
        self.Fail_Stress = parameters["Fail_Stress"]
        self.Density = parameters["Density"]
        self.Poissons_Ratio = parameters["Poissons_Ratio"]
        self.CTE = parameters["CTE"]
        self.uStatic = parameters["uStatic"]
        self.uDynamic = parameters["uDynamic"]

    def write_to_xml( self, root ):
        
        material_root = etree.SubElement( root, "Material", ID=str( self.id ) )
        etree.SubElement( material_root, "Name" ).text = str( self.Name )  
        
        display = etree.SubElement( material_root, "Display" )
        etree.SubElement( display, "Red" ).text = str( self.color[0] )
        etree.SubElement( display, "Green" ).text = str( self.color[1] )
        etree.SubElement( display, "Blue" ).text = str( self.color[2] )
        etree.SubElement( display, "Alpha" ).text = str( self.color[3] )

        mechanical = etree.SubElement( material_root, "Mechanical" )
        #TODO too many ifs... can we reduce this somehow? (perhaps some loop?)
        if self.isTarget is not None:
          etree.SubElement( mechanical, "isTarget" ).text = str( self.isTarget )
        if self.isMeasured is not None:
          etree.SubElement( mechanical, "isMeasured" ).text = str( self.isMeasured )
        if self.Fixed is not None:
          etree.SubElement( mechanical, "Fixed" ).text = str( self.Fixed )
        if self.Sticky is not None:
          etree.SubElement( mechanical, "Sticky" ).text = str( self.Sticky )
        if self.isPaceMaker is not None:
          etree.SubElement( mechanical, "Cilia" ).text = str( self.isPaceMaker )
        if self.PaceMakerPeriod is not None:
          etree.SubElement( mechanical, "PaceMakerPeriod" ).text = str( self.PaceMakerPeriod )
        if self.signalValueDecay is not None:
          etree.SubElement( mechanical, "signalValueDecay" ).text = str( self.signalValueDecay )
        if self.signalTimeDelay is not None:
          etree.SubElement( mechanical, "signalTimeDelay" ).text = str( self.signalTimeDelay )
        if self.inactivePeriod is not None:
          etree.SubElement( mechanical, "inactivePeriod" ).text = str( self.inactivePeriod )
        if self.MatModel is not None:
          etree.SubElement( mechanical, "MatModel" ).text = str( self.MatModel )
        if self.Elastic_Mod is not None:
          etree.SubElement( mechanical, "Elastic_Mod" ).text = str( self.Elastic_Mod )
        if self.Fail_Stress is not None:
          etree.SubElement( mechanical, "Fail_Stress" ).text = str( self.Fail_Stress )
        if self.Density is not None:
          etree.SubElement( mechanical, "Density" ).text = str( self.Density )
        if self.Poissons_Ratio is not None:
          etree.SubElement( mechanical, "Poissons_Ratio" ).text = str( self.Poissons_Ratio )
        if self.CTE is not None:
          etree.SubElement( mechanical, "CTE" ).text = str( self.CTE )
        if self.uStatic is not None:
          etree.SubElement( mechanical, "uStatic" ).text = str( self.uStatic )
        if self.uDynamic is not None:
          etree.SubElement( mechanical, "uDynamic" ).text = str( self.uDynamic )

        return material_root

if __name__ == "__main__":
  root = etree.Element( "Root" )
  mat = Material()
  x = mat.write_to_xml( root )
  print( etree.tostring( root, pretty_print=True ).decode( "utf-8" ) )
