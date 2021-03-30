## Step file reader viewer and analyzer

###Requirements:
conda

python 3.9

pyqt5	5.15.4	

pyqt5-qt	5.15.2	

pyqt5-qt5	5.15.2	

pythonocc-core	7.4.1	

setuptools	52.0.0	

steputils	0.1a2	

### Brief:
This is a tiny project to open *.step file, invert model and save result to step file

## Used materials:

https://dev.opencascade.org/doc/occt-7.0.0/overview/html/occt_user_guides__test_harness.html

https://github.com/tpaviot/pythonocc-demos

https://github.com/tpaviot/pythonocc-demos/tree/master/examples

### RUN cut from parallelepiped

1. add step files to step_examples
   
2. change in main.py

```shp = read_step_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'step_examples', 'YOUR_FILE_NAME'))```

3. python main.py

### RUN cut from form

1. add step files to step_examples
   
2. change in main_from_zag.py

```
shpTmpl = read_step_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'step_examples', 'YOUR_TEMPLATE'))
shp = read_step_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'step_examples', 'YOUR_FILE_NAME'))
```

3. python main_from_zag.py