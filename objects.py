from __future__ import print_function

import os

from OCC.Extend.DataExchange import read_step_file
from OCC.Display.SimpleGui import init_display

from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs, STEPControl_StepModelType
from OCC.Core.Interface import Interface_Static_SetCVal

from app.ShapeLogic.Modifications import get_boundingbox, cut_from_parallelepiped
from app.ShapeLogic.Info import count_volume_from_shape, get_dx_dy_dz
from app.ShapeLogic.Objects import detect_through_holes

from app.Display.Display import recognize_clicked

if __name__ == '__main__':
    display, start_display, add_menu, add_function_to_menu = init_display()
    display.SetSelectionModeFace()
    display.register_select_callback(recognize_clicked)
    p = os.path.dirname(os.path.abspath(__file__))
    shp = read_step_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result', 'objects.stp'))
    display.DisplayShape(shp, transparency=0.0, color="black")
    start_display()
