from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepGProp import brepgprop_VolumeProperties
from app.ShapeLogic.Modifications import get_oriented_bounding_box_bnd


def count_volume_from_shape(shape: TopoDS_Shape):
    props = GProp_GProps()
    brepgprop_VolumeProperties(shape, props)
    return props.Mass()


def get_dx_dy_dz(shape: TopoDS_Shape):
    theBox = get_oriented_bounding_box_bnd(shape)
    aBaryCenter = theBox.Center()
    aXDir = theBox.XDirection()
    aYDir = theBox.YDirection()
    aZDir = theBox.ZDirection()
    aHalfX = theBox.XHSize()
    aHalfY = theBox.YHSize()
    aHalfZ = theBox.ZHSize()

    return 2.0 * aHalfX, 2.0*aHalfY, 2.0 * aHalfZ