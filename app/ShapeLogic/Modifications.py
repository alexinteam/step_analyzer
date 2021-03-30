from OCC.Core.BRepBndLib import brepbndlib_Add, brepbndlib_AddOBB
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.Bnd import Bnd_Box, Bnd_OBB
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.TopoDS import topods
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir, gp_XYZ


def get_boundingbox(shape: TopoDS_Shape, tol=1e-6, use_mesh=True):
    bbox = Bnd_Box()
    bbox.SetGap(tol)
    if use_mesh:
        mesh = BRepMesh_IncrementalMesh()
        mesh.SetParallelDefault(True)
        mesh.SetShape(shape)
        mesh.Perform()
        if not mesh.IsDone():
            raise AssertionError("Mesh not done.")
    brepbndlib_Add(shape, bbox, use_mesh)

    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    return xmin, ymin, zmin, xmax, ymax, zmax, xmax - xmin, ymax - ymin, zmax - zmin


def get_oriented_bounding_box(
        shape, offset=0.0,
        xWidht=None, yWidht=None, zWidht=None,
        xxWidht=None, yyWidht=None, zzWidht=None,
):
    bbox = Bnd_OBB()
    brepbndlib_AddOBB(shape, bbox, True, True, True)
    # bbox.Enlarge(0.5)
    obb_shape1 = ConvertBndToShape(
        bbox, offset, xWidht, yWidht, zWidht, zzWidht, xxWidht, yyWidht
    )
    return obb_shape1


def get_oriented_bounding_box_bnd(shape):
    bbox = Bnd_OBB()
    brepbndlib_AddOBB(shape, bbox, True, True, True)

    return bbox


def cut_from_parallelepiped(shape, offset=0.001):
    myBox1 = get_oriented_bounding_box(shape, offset=offset)
    myBox2 = get_oriented_bounding_box(shape, xWidht=offset)
    myBox3 = get_oriented_bounding_box(shape, yWidht=offset)
    myBox4 = get_oriented_bounding_box(shape, zWidht=offset)
    myBox5 = get_oriented_bounding_box(shape, xxWidht=offset)
    myBox6 = get_oriented_bounding_box(shape, yyWidht=offset)
    myBox7 = get_oriented_bounding_box(shape, zzWidht=offset)

    sew = BRepBuilderAPI_Sewing()
    for face in TopologyExplorer(shape).faces():
        sew.Add(face)
    sew.Perform()
    solid = MakeSolidFromShell(sew.SewedShape())

    myCut1 = BRepAlgoAPI_Cut(myBox1, solid).Shape()
    myCut2 = BRepAlgoAPI_Cut(myCut1, myBox2).Shape()
    myCut3 = BRepAlgoAPI_Cut(myCut2, myBox3).Shape()
    myCut4 = BRepAlgoAPI_Cut(myCut3, myBox4).Shape()
    myCut5 = BRepAlgoAPI_Cut(myCut4, myBox5).Shape()
    myCut6 = BRepAlgoAPI_Cut(myCut5, myBox6).Shape()
    myCut7 = BRepAlgoAPI_Cut(myCut6, myBox7).Shape()
    return myCut7


def ConvertBndToShape(
        theBox, offset=0.0,
        xWidht=None, yWidht=None, zWidht=None, xxWidht=None, yyWidht=None, zzWidht=None,
):
    aBaryCenter = theBox.Center()
    aXDir = theBox.XDirection()
    aYDir = theBox.YDirection()
    aZDir = theBox.ZDirection()
    aHalfX = theBox.XHSize()
    aHalfY = theBox.YHSize()
    aHalfZ = theBox.ZHSize()

    ax = gp_XYZ(aXDir.X(), aXDir.Y(), aXDir.Z())
    ay = gp_XYZ(aYDir.X(), aYDir.Y(), aYDir.Z())
    az = gp_XYZ(aZDir.X(), aZDir.Y(), aZDir.Z())

    p = gp_Pnt(aBaryCenter.X() - offset, aBaryCenter.Y() - offset, aBaryCenter.Z() - offset)
    anAxes = gp_Ax2(p, gp_Dir(aZDir), gp_Dir(aXDir))
    anAxes.SetLocation(gp_Pnt(p.XYZ() - ax * aHalfX - ay * aHalfY - az * aHalfZ))
    if xWidht is not None:
        anAxes.SetLocation(gp_Pnt(p.XYZ() + (ax * (aHalfX - xWidht)) - ay * aHalfY - az * aHalfZ))
        aBox = BRepPrimAPI_MakeBox(anAxes, 2.0 * aHalfX, 2.0 * aHalfY + 0.01, 2.0 * aHalfZ + 0.01).Shape()
    elif xxWidht is not None:
        anAxes.SetLocation(gp_Pnt(p.XYZ() - ax * (3.0 * aHalfX - xxWidht) - ay * aHalfY - az * aHalfZ))
        aBox = BRepPrimAPI_MakeBox(anAxes, 2.0 * aHalfX, 2.0 * aHalfY + 0.01, 2.0 * aHalfZ + 0.01).Shape()
    elif yWidht is not None:
        anAxes.SetLocation(gp_Pnt(p.XYZ() - ax * aHalfX + ay * (aHalfY - yWidht) - az * aHalfZ))
        aBox = BRepPrimAPI_MakeBox(anAxes, 2.0 * aHalfX + 0.01, 2.0 * aHalfY, 2.0 * aHalfZ + 0.01).Shape()
    elif yyWidht is not None:
        anAxes.SetLocation(gp_Pnt(p.XYZ() - ax * aHalfX - ay * (3.0 * aHalfY - yyWidht) - az * aHalfZ))
        aBox = BRepPrimAPI_MakeBox(anAxes, 2.0 * aHalfX + 0.01, 2.0 * aHalfY, 2.0 * aHalfZ + 0.01).Shape()
    elif zWidht is not None:
        anAxes.SetLocation(gp_Pnt(p.XYZ() - ax * aHalfX - ay * aHalfY + az * (aHalfZ - zWidht)))
        aBox = BRepPrimAPI_MakeBox(anAxes, 2.0 * aHalfX + 0.01, 2.0 * aHalfY + 0.01, 2.0 * aHalfZ).Shape()
    elif zzWidht is not None:
        anAxes.SetLocation(gp_Pnt(p.XYZ() - ax * aHalfX - ay * aHalfY - az * (3.0 * aHalfZ - zzWidht)))
        aBox = BRepPrimAPI_MakeBox(anAxes, 2.0 * aHalfX + 0.01, 2.0 * aHalfY + 0.01, 2.0 * aHalfZ).Shape()
    else:
        aBox = BRepPrimAPI_MakeBox(anAxes, 2.0 * aHalfX, 2.0 * aHalfY, 2.0 * aHalfZ).Shape()

    return aBox

def MakeSolidFromShell(shell):
    ms = BRepBuilderAPI_MakeSolid()
    ms.Add(topods.Shell(shell))
    solid = ms.Solid()
    return solid

def remove_face(shape, faceToRemove):
    for face in TopologyExplorer(shape).faces():
        if face.IsSame(faceToRemove):
            face.Nullify()

    return shape