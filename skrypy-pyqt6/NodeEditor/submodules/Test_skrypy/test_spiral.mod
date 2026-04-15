[diagram]
link=[N10] node=[C0:in0#Node#F0:in0]
link=[N13] node=[F0:in0#Node#U1:set_title]
link=[N12] node=[F0:in0#Node#S0:k]
link=[N11] node=[A8:#Node#S0:angle_type]
link=[N9] node=[S0:x#Node#U1:x]
link=[N8] node=[A1:#Node#U0:xmin]
link=[N7] node=[A4:#Node#U0:xmax]
link=[N6] node=[A6:#Node#U0:delta_x]
link=[N5] node=[U0:outAbscissa#Node#S0:T]
link=[N4] node=[A0:#Node#U1:plot_linestyle]
link=[N3] node=[A3:#Node#U1:plot_color]
link=[N2] node=[A2:#Node#U1:plot_linewidth]
link=[N1] node=[A5:#Node#U1:style_use]
link=[N0] node=[S0:y#Node#U1:y_data]
block=[U1] category=[Matplotlib.Plots] class=[matplotlib_plot] valInputs=[(['y_data', 'x', 'style_use', 'plot_linewidth', 'plot_color', 'plot_linestyle', 'set_title'], ['Node(N0)', 'Node(N9)', 'Node(N1)', 'Node(N2)', 'Node(N3)', 'Node(N4)', 'Node(N13)'], [], [])] RectF=[(920.0, 80.0, 300.0, 500.0)] 
block=[U0] category=[Signals.Generator] class=[gen_abscissa] valInputs=[(['xmin', 'xmax', 'delta_x'], ['Node(N8)', 'Node(N7)', 'Node(N6)'], ['outAbscissa'], ['list_float'])] RectF=[(-380.0, -140.0, 160.0, 80.0)] 
script=[S0] title=[Script_editor] inputs=[['T', 'in', 'list_float'], ['k', 'in', 'float'], ['angle_type', 'in', 'str']] outputs=[['y', 'out', 'list_float'], ['x', 'out', 'list_float']] code=[your code] RectF=[(-60.0, -180.0, 656.0, 341.0)]
constant=[A8] value=['degree'] format=[enumerate(('radian', 'degree'))] label=[const] RectF=[(-260.0, 100.0, 85.0, 31.0)] 
constant=[A6] value=[(-100000.0, 2.0, 100000.0)] format=[float] label=[delta_x] RectF=[(-600.0, -60.0, 131.0, 31.0)] 
constant=[A5] value=['default'] format=[enumerate(('default', 'classic', 'bmh', 'fast', 'ggplot'))] label=[style_use] RectF=[(640.0, 260.0, 85.0, 31.0)] 
constant=[A4] value=[(-100000.0, 10000.0, 100000.0)] format=[float] label=[xmax] RectF=[(-600.0, -120.0, 131.0, 31.0)] 
constant=[A3] value=['blue'] format=[enumerate(('green', 'blue', 'red', 'black', 'yellow', 'cyan', 'magenta'))] label=[plot_color] RectF=[(640.0, 340.0, 93.0, 31.0)] 
constant=[A2] value=[(-100000.0, 1.0, 100000.0)] format=[float] label=[plot_linewidth] RectF=[(480.0, 320.0, 131.0, 31.0)] 
constant=[A1] value=[(-100000.0, 0.0, 100000.0)] format=[float] label=[xmin] RectF=[(-600.0, -180.0, 131.0, 31.0)] 
constant=[A0] value=['solid'] format=[enumerate(('solid', 'dotted', 'dashed', 'dashdot'))] label=[plot_linestyle] RectF=[(500.0, 400.0, 91.0, 31.0)] 
connt=[C0] name=[in0] type=[in] format=[list_float] valOut=[[0.0]] RectF=[(-1000.0, 220.0, 70, 24)] 
loopFor=[F0] inputs=[[[['in0', 'in', 'list_float'], ['in0', 'out', 'float']]]] outputs=[[]] listItems=[['S0', 'A3', 'A4', 'A0', 'A5', 'A2', 'U1', 'U0', 'A1', 'A6', 'A8']] RectF=[(-680.0, -360.0, 2020.0, 1200.0)] 
[source S0]
['T=U0:outAbscissa', "angle_type='degree'", 'k=F0:in0']
from NodeEditor.modules.Numpy.Functions_trigo import numpy_trigonometry
from NodeEditor.modules.Tools.Float import float_operations_dyn
import numpy as np

x, y = [], []

for t in T:
    xa = numpy_trigonometry(t, 'cos', angle_type).res()
    ya = numpy_trigonometry(t, 'sin', angle_type).res()
    xb = numpy_trigonometry(k*t+t, 'cos', angle_type).res()
    yb = numpy_trigonometry(k*t+t, 'sin', angle_type).res()
    xc = float_operations_dyn('mul', xa, list_float_in_0=k+1).out_result()
    yc = float_operations_dyn('mul', ya, list_float_in_0=k+1).out_result()
    xd = float_operations_dyn('sub', xc, list_float_in_0=xb).out_result()
    yd = float_operations_dyn('sub', yc, list_float_in_0=yb).out_result()
    x.append(xd)
    y.append(yd)


['S0:y', 'S0:x']
[/source S0]

[execution]
['C0:in0=']
['F0']
{}
[]
{}
[]
[loopfor F0]
['F0:in0=C0:in0']
['U0', 'S0', 'U1']
{'U0': ('Signals.Generator', 'gen_abscissa', "(['xmin', 'xmax', 'delta_x'], [0.0, 10000.0, 2.0], ['outAbscissa'], ['list_float'])"), 'U1': ('Matplotlib.Plots', 'matplotlib_plot', "(['y_data', 'x', 'style_use', 'plot_linewidth', 'plot_color', 'plot_linestyle', 'set_title'], ['S0:y', 'S0:x', 'default', 1.0, 'blue', 'solid', 'F0:in0'], [], [])")}
['F0:in0', 'F0:in0', 'S0:x', 'U0:outAbscissa', 'S0:y']
{}
[]
[interlinks]
[]
