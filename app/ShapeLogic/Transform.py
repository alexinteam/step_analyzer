from Modifications import *

def invert_shape(shape: TopoDS_Shape):
    get_boundingbox(shape)

    offset = 0.001
    return cut_from_parallelepiped(shape, offset)

