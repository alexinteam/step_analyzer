from __future__ import print_function

import sys
import os

from OCC.Core.GeomAbs import (GeomAbs_Plane, GeomAbs_Cylinder,
                              GeomAbs_BSplineSurface)
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.TopoDS import TopoDS_Face, TopoDS_Solid
from OCC.Display.SimpleGui import init_display
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.ShapeFactory import get_oriented_boundingbox
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.Bnd import Bnd_Box, Bnd_OBB
from OCC.Core.BRepBndLib import brepbndlib_Add, brepbndlib_AddOBB
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Ax2, gp_Dir, gp_XYZ
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakePolygon,
                                     BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid)
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common, BRepAlgoAPI_Cut
from OCC.Core.TopoDS import topods
from OCC.Display.SimpleGui import init_display

from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs, STEPControl_StepModelType
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform, BRepBuilderAPI_MakeVertex

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Extend.ShapeFactory import get_aligned_boundingbox
from OCC.Core.BRepGProp import brepgprop_VolumeProperties
from OCC.Core.GProp import GProp_GProps
import numpy as np
import random
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common, BRepAlgoAPI_Section, BRepAlgoAPI_Cut
from OCC.Core.BOPTools import BOPTools_AlgoTools_AreFacesSameDomain


from pprint import pprint

def recognize_face(a_face):
    """ Takes a TopoDS shape and tries to identify its nature
    whether it is a plane a cylinder a torus etc.
    if a plane, returns the normal
    if a cylinder, returns the radius
    """
    if not type(a_face) is TopoDS_Face:
        print("Please hit the 'G' key to switch to face selection mode")
        return False
    surf = BRepAdaptor_Surface(a_face, True)
    surf_type = surf.GetType()
    if surf_type == GeomAbs_Plane:
        print("Identified Plane Geometry")
        # look for the properties of the plane
        # first get the related gp_Pln
        gp_pln = surf.Plane()
        location = gp_pln.Location()  # a point of the plane
        normal = gp_pln.Axis().Direction()  # the plane normal
        # then export location and normal to the console output
        print("--> Location (global coordinates)", location.X(), location.Y(), location.Z())
        print("--> Normal (global coordinates)", normal.X(), normal.Y(), normal.Z())
    elif surf_type == GeomAbs_Cylinder:
        print("Identified Cylinder Geometry")
        # look for the properties of the cylinder
        # first get the related gp_Cyl
        gp_cyl = surf.Cylinder()
        location = gp_cyl.Location()  # a point of the axis
        axis = gp_cyl.Axis().Direction()  # the cylinder axis
        # then export location and normal to the console output
        print("--> Location (global coordinates)", location.X(), location.Y(), location.Z())
        print("--> Axis (global coordinates)", axis.X(), axis.Y(), axis.Z())
    elif surf_type == GeomAbs_BSplineSurface:
        print("Identified BSplineSurface Geometry")
        # gp_bsrf = surf.Surface()
        # degree = gp_bsrf.NbUKnots()
        # TODO use a model that provided BSplineSurfaces, as1_pe_203.stp only contains
        # planes and cylinders
    else:
        # TODO there are plenty other type that can be checked
        # see documentation for the BRepAdaptor class
        # https://www.opencascade.com/doc/occt-6.9.1/refman/html/class_b_rep_adaptor___surface.html
        print(surf_type, "recognition not implemented")


def recognize_clicked(shp, *kwargs):
    """ This is the function called every time
    a face is clicked in the 3d view
    """
    for shape in shp:  # this should be a TopoDS_Face TODO check it is
        print("Face selected: ", shape)
        recognize_face(shape)


def recognize_batch(event=None):
    """ Menu item : process all the faces of a single shape
    """
    # loop over faces only
    for face in TopologyExplorer(shp).faces():
        # call the recognition function
        recognize_face(face)


def exit(event=None):
    sys.exit()


def MakeSolidFromShell(shell):
    ms = BRepBuilderAPI_MakeSolid()
    ms.Add(topods.Shell(shell))
    solid = ms.Solid()
    return solid


if __name__ == '__main__':
    display, start_display, add_menu, add_function_to_menu = init_display()
    display.SetSelectionModeFace()  # switch to Face selection mode
    display.register_select_callback(recognize_clicked)
    # first loads the STEP file and display
    p = os.path.dirname(os.path.abspath(__file__))
    shpTmpl = read_step_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'step_examples', '21_141_0046_022_0.stp'))
    shp = read_step_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'step_examples', '21_141_0046_022_0_stock.stp'))

    sew = BRepBuilderAPI_Sewing()
    for face in TopologyExplorer(shpTmpl).faces():
        sew.Add(face)
    sew.Perform()
    solid = MakeSolidFromShell(sew.SewedShape())

    sew = BRepBuilderAPI_Sewing()
    for face in TopologyExplorer(shp).faces():
        sew.Add(face)
    sew.Perform()
    solid1 = MakeSolidFromShell(sew.SewedShape())

    myCut1 = BRepAlgoAPI_Cut(solid, solid1).Shape()


    step_writer = STEPControl_Writer()
    Interface_Static_SetCVal("write.step.schema", "AP242")

    # transfer shapes and write file
    step_writer.Transfer(myCut1, STEPControl_StepModelType(STEPControl_AsIs))
    status = step_writer.Write(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result', 'objects.stp'))

    display.DisplayShape([shp], color="yellow", transparency=0.5)
    display.DisplayShape([myCut1], color="blue")

    start_display()
