from __future__ import print_function

import sys

from OCC.Core.GeomAbs import (GeomAbs_Plane, GeomAbs_Cylinder,GeomAbs_Cone,
                              GeomAbs_BSplineSurface, GeomAbs_Circle, GeomAbs_OtherCurve)
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_CompCurve
from OCC.Core.TopoDS import TopoDS_Face
from OCC.Display.SimpleGui import init_display
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer

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
        print("--> Radius", gp_cyl.Radius())
    if surf_type == GeomAbs_Cone:
        print("Identified Cone Geometry")
        # look for the properties of the cylinder
        # first get the related gp_Cyl
        gp_cone = surf.Cone()
        location = gp_cone.Location()  # a point of the axis
        axis = gp_cone.Axis().Direction()  # the cylinder axis
        # then export location and normal to the console output
        print("--> Location (global coordinates)", location.X(), location.Y(), location.Z())
        print("--> Axis (global coordinates)", axis.X(), axis.Y(), axis.Z())
        # print("--> Radius", gp_cone.RefRadius())
        for wire in TopologyExplorer(a_face).wires_from_face(a_face):
            curve = BRepAdaptor_CompCurve(wire, True)
            curve_type = curve.GetType()
            if curve_type == GeomAbs_Circle:
                circle = curve.Circle()
                circle.Radius()
                print("--> Radius", gp_cone.RefRadius())
            if curve_type == GeomAbs_OtherCurve:
                for edge in TopologyExplorer(wire).edges_from_wire(wire):
                    if TopologyExplorer(wire).number_of_edges_from_wire(wire) == 4:

                        a= 1
                circle = curve.Circle()
                circle.Radius()
                print("--> Radius", circle.Radius())

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


def recognize_batch(shp, event=None):
    """ Menu item : process all the faces of a single shape
    """
    # loop over faces only
    for face in TopologyExplorer(shp).faces():
        # call the recognition function
        recognize_face(face)


def exit(event=None):
    sys.exit()