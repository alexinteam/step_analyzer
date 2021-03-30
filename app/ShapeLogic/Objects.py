from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone
from OCC.Core.BRepTools import BRepTools_ReShape

from app.ShapeLogic.Info import get_dx_dy_dz
from OCC.Core.TopoDS import topods, TopoDS_Compound, TopoDS_Face
from OCC.Core.gp import (gp_Pnt, gp_OX, gp_Vec, gp_Trsf, gp_DZ, gp_Ax2, gp_Ax3,
                         gp_Pnt2d, gp_Dir2d, gp_Ax2d, gp_Pln)


def analyze(shape: TopoDS_Shape):
    holes = detect_through_holes(shape)
    return holes

# сквозные отверстия
def detect_through_holes(shape: TopoDS_Shape, removeHoles: bool=False):
    holes = 0
    cones = 0
    re = BRepTools_ReShape()
    faces = TopologyExplorer(shape).number_of_faces()
    shells = TopologyExplorer(shape).number_of_shells()
    dxShape, dyShape, dzShape = get_dx_dy_dz(shape)
    for shell in TopologyExplorer(shape).shells():
        for face in TopologyExplorer(shell).faces():
            dxFace, dyFace, dzFace = get_dx_dy_dz(face)
            surf = BRepAdaptor_Surface(face, True)
            surf_type = surf.GetType()
            # if surf_type == GeomAbs_Plane:
            #     # print("Identified Plane Geometry")
            #     gp_pln = surf.Plane()
            #     location = gp_pln.Location()  # a point of the plane
            #     normal = gp_pln.Axis().Direction()  # the plane normal
            #     # print("--> Location (global coordinates)", location.X(), location.Y(), location.Z())
            #     # print("--> Normal (global coordinates)", normal.X(), normal.Y(), normal.Z())
            if surf_type == GeomAbs_Cylinder:
                print("Identified Cylinder Geometry")
                # look for the properties of the cylinder
                # first get the related gp_Cyl
                gp_cyl = surf.Cylinder()
                location = gp_cyl.Location()  # a point of the axis
                axis = gp_cyl.Axis().Direction()  # the cylinder axis
                # then export location and normal to the console output
                print("--> Location (global coordinates)", location.X(), location.Y(), location.Z())
                print("--> Axis (global coordinates)", axis.X(), axis.Y(), axis.Z())

                holes = holes + 1

                # for edge in TopologyExplorer(shape).edges_from_face(face):
                #     re.Remove(edge)
                # re.Remove(face)
                # re.Replace(shell, re.Apply(shell))
                # shape = re.Apply(shell)

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

                cones = cones + 1

                # for edge in TopologyExplorer(shape).edges_from_face(face):
                #     re.Remove(edge)
                # re.Remove(face)
                # re.Replace(shell, re.Apply(shell))
                # shape = re.Apply(shell)
            else:
                # TODO there are plenty other type that can be checked
                # see documentation for the BRepAdaptor class
                # https://www.opencascade.com/doc/occt-6.9.1/refman/html/class_b_rep_adaptor___surface.html
                print(surf_type, "recognition not implemented")


    return cones,holes, shape


def face_is_plane(face: TopoDS_Face) -> bool:
    """
    Returns True if the TopoDS_Face is a plane, False otherwise
    """
    surf = BRepAdaptor_Surface(face, True)
    surf_type = surf.GetType()
    return surf_type == GeomAbs_Plane

def geom_plane_from_face(aFace: TopoDS_Face) -> gp_Pln:
    """
    Returns the geometric plane entity from a planar surface
    """
    return BRepAdaptor_Surface(aFace, True).Plane()
