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
        "isTarget" : False,
        #True if we want to measure voxels made by this mat. in all MathTree fcs(), else False
        "isMeasured" : True,
        #True if we don't want this material to move at all, else False
        "Fixed" : False,
        #True if we want attachment happen to this mat., else False
        "Sticky" : False,
        #real number, 0 if we don't want cilia to happen
        "Cilia" : 0,
        #True if this mat. can generate periodic signals, else False
        "isPaceMaker" : False,
        #real number, period between two signal
        "PaceMakerPeriod" : 0,
        #0.0 ~ 1.0, decay ratio of signal propagation in other parts of the body
        "signalValueDecay" : 0.9,
        #real number/sec delay of signal at every stop
        "signalTimeDelay" : 0.03,
        #real number how long does voxel stay inactive after sending signal
        "inactivePeriod" : 0.03,
        #False simple elastic model, True for perfectly elastic mat.
        "MatModel" : False,
        #real number in Pascal, Young's Modulus
        "Elastic_Mod" : 0,
        #real number in Pascal, if stress > threshold -> mat. will fail by fracture
        "Fail_Stress" : 0,
        #real number in kg/m^3, e.g. rubber's density 1.5e+3 kg/m^3
        "Density" : 0,
        #0.0 ~ 0.5
        "Poissons_Ratio" : 0,
        #small real number in 1/degree Celsius
        "CTE" : 0,
        #0.0 ~ 5.0, static frictional coefficient
        "uStatic" : 0,
        #0.0 ~ 1.0, kinetic frictional coefficient
        "uDynamic" : 0,
        #False if this material does not exerting cilia forces, else True
        "Cilia" : False
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
        self.isTarget = 1 if parameters["isTarget"] else 0
        self.isMeasured = 1 if parameters["isMeasured"] else 0
        self.Fixed = 1 if parameters["Fixed"] else 0
        self.Sticky = 1 if parameters["Sticky"] else 0
        self.Cilia = parameters["Cilia"]
        self.isPaceMaker = parameters["isPaceMaker"]
        self.PaceMakerPeriod = parameters["PaceMakerPeriod"]
        self.signalValueDecay = parameters["signalValueDecay"]
        self.signalTimeDelay = parameters["signalTimeDelay"]
        self.inactivePeriod = parameters["inactivePeriod"]
        self.MatModel = 1 if parameters["MatModel"] else 0
        self.Elastic_Mod = parameters["Elastic_Mod"]
        self.Fail_Stress = parameters["Fail_Stress"]
        self.Density = parameters["Density"]
        self.Poissons_Ratio = parameters["Poissons_Ratio"]
        self.CTE = parameters["CTE"]
        self.uStatic = parameters["uStatic"]
        self.uDynamic = parameters["uDynamic"]
        self.Cilia = 1 if parameters["Cilia"] else 0

    def write_to_xml( self, root ):
        
        material_root = etree.SubElement( root, "Material", ID=str( self.id ) )
        etree.SubElement( material_root, "Name" ).text = str( self.Name )  
        
        display = etree.SubElement( material_root, "Display" )
        etree.SubElement( display, "Red" ).text = str( self.color[0] )
        etree.SubElement( display, "Green" ).text = str( self.color[1] )
        etree.SubElement( display, "Blue" ).text = str( self.color[2] )
        etree.SubElement( display, "Alpha" ).text = str( self.color[3] )

        mechanical = etree.SubElement( material_root, "Mechanical" )
        etree.SubElement( mechanical, "isTarget" ).text = str( self.isTarget )
        etree.SubElement( mechanical, "isMeasured" ).text = str( self.isMeasured )
        etree.SubElement( mechanical, "Fixed" ).text = str( self.Fixed )
        etree.SubElement( mechanical, "Sticky" ).text = str( self.Sticky )
        etree.SubElement( mechanical, "Cilia" ).text = str( self.isPaceMaker )
        etree.SubElement( mechanical, "PaceMakerPeriod" ).text = str( self.PaceMakerPeriod )
        etree.SubElement( mechanical, "signalValueDecay" ).text = str( self.signalValueDecay )
        etree.SubElement( mechanical, "signalTimeDelay" ).text = str( self.signalTimeDelay )
        etree.SubElement( mechanical, "inactivePeriod" ).text = str( self.inactivePeriod )
        etree.SubElement( mechanical, "MatModel" ).text = str( self.MatModel )
        etree.SubElement( mechanical, "Elastic_Mod" ).text = str( self.Elastic_Mod )
        etree.SubElement( mechanical, "Fail_Stress" ).text = str( self.Fail_Stress )
        etree.SubElement( mechanical, "Density" ).text = str( self.Density )
        etree.SubElement( mechanical, "Poissons_Ratio" ).text = str( self.Poissons_Ratio )
        etree.SubElement( mechanical, "CTE" ).text = str( self.CTE )
        etree.SubElement( mechanical, "uStatic" ).text = str( self.uStatic )
        etree.SubElement( mechanical, "uDynamic" ).text = str( self.uDynamic )
        etree.SubElement( mechanical, "Cilia" ).text = str( self.Cilia )

        return material_root

if __name__ == "__main__":
  root = etree.Element( "Root" )
  mat = Material()
  x = mat.write_to_xml( root )
  print( etree.tostring( root, pretty_print=True ).decode( "utf-8" ) )
