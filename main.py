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
    shp = read_step_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'step_examples', '21_141_sponka.stp'))
    get_boundingbox(shp)

    print('box dx, dy, dz:', get_dx_dy_dz(shp))
    cones, holes, newshp = detect_through_holes(shp, True)

    cutFromParallelepiped = cut_from_parallelepiped(shp, 0.001)
    step_writer = STEPControl_Writer()
    Interface_Static_SetCVal("write.step.schema", "AP242")

    # transfer shapes and write file
    step_writer.Transfer(cutFromParallelepiped, STEPControl_StepModelType(STEPControl_AsIs))
    status = step_writer.Write(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result', 'objects.stp'))
    print('volume:', count_volume_from_shape(cutFromParallelepiped))
    print('box dx, dy, dz:', get_dx_dy_dz(cutFromParallelepiped))
    print('cones', cones)
    print('holes', holes)


    # display.DisplayShape(cutFromParallelepiped, transparency=0.5, color="blue")
    display.DisplayShape(shp, transparency=0.5, color="black")

    # shp1 = read_step_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result', 'objects.stp'))

    start_display()
