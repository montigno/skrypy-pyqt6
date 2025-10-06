[diagram]
link=[N65] node=[U0:image#Node#U21:image_in]
link=[N63] node=[S1:roi_nameout#Node#U21:roi_name]
link=[N59] node=[A8:#Node#U13:out_path]
link=[N43] node=[U10:csv_out#Node#C6:asym_out]
link=[N40] node=[U16:csv_out#Node#C5:zspectras_out]
link=[N37] node=[U12:outFile#Node#U10:file_output]
link=[N35] node=[U14:outFile#Node#U16:file_output]
link=[N33] node=[C4:treatment_dir#Node#U12:path_in]
link=[N32] node=[U20:str_conc#Node#U12:path_name]
link=[N21] node=[U17:str_conc#Node#U14:path_name]
link=[N20] node=[C4:treatment_dir#Node#U14:path_in]
link=[N19] node=[C3:dir_root#Node#S1:dir_root]
link=[N18] node=[C2:data_list#Node#S1:file_list]
link=[N62] node=[U25:np_transpose#Node#U10:data]
link=[N22] node=[U9:array#Node#U25:a]
link=[N42] node=[A14:#Node#S0:correction_B0]
link=[N11] node=[U6:out_value#Node#S0:wassr_range]
link=[N10] node=[U5:out_value#Node#S0:cest_range]
link=[N15] node=[A3:#Node#U6:tag]
link=[N14] node=[A4:#Node#U6:tag_0]
link=[N12] node=[U3:newPath#Node#U7:json_file]
link=[N9] node=[A4:#Node#U5:tag_0]
link=[N5] node=[A2:#Node#U3:new_extension]
link=[N6] node=[U2:newPath#Node#U4:json_file]
link=[N7] node=[U4:dict_json#Node#U5:input_dict]
link=[N8] node=[A3:#Node#U5:tag]
link=[N13] node=[U7:dict_json#Node#U6:input_dict]
link=[N16] node=[U0:image#Node#S0:cest_img]
link=[N17] node=[U1:image#Node#S0:wassr_img]
link=[N0] node=[S1:cest_path#Node#U2:path_in]
link=[N3] node=[S1:wassr_path#Node#U3:path_in]
link=[N30] node=[S0:x_cest#Node#U22:list_float_in]
link=[N31] node=[S0:y_cest_mean#Node#U22:list_float_in_0]
link=[N23] node=[S0:x_asym#Node#U9:list_float_in]
link=[N24] node=[S0:y_asym_mean#Node#U9:list_float_in_0]
link=[N36] node=[A11:#Node#U20:stringIn_1]
link=[N28] node=[A10:#Node#U17:stringIn_1]
link=[N55] node=[U22:array#Node#U24:a]
link=[N61] node=[U24:np_transpose#Node#U16:data]
link=[N29] node=[C0:subject#Node#S1:subject]
link=[N47] node=[C1:roi_name#Node#S1:roi_name]
link=[N44] node=[A0:#Node#S0:ppm]
link=[N46] node=[A1:#Node#U8:end]
link=[N56] node=[A5:#Node#U8:start]
link=[N45] node=[C0:subject#Node#U8:in_string]
link=[N34] node=[S1:roi_nameout#Node#U17:stringIn]
link=[N41] node=[S1:roi_nameout#Node#U20:stringIn]
link=[N52] node=[A7:#Node#U17:stringIn_2]
link=[N57] node=[A7:#Node#U20:stringIn_2]
link=[N38] node=[U8:substring#Node#U17:stringIn_0]
link=[N39] node=[U8:substring#Node#U20:stringIn_0]
link=[N2] node=[S1:cest_path#Node#U13:in_file]
link=[N1] node=[A6:#Node#U2:new_extension]
link=[N4] node=[S1:wassr_path#Node#U15:in_file]
link=[N48] node=[U19:outPath#Node#U1:nifti_file]
link=[N49] node=[U18:outPath#Node#U0:nifti_file]
link=[N50] node=[U13:out_list#Node#U18:list_path_in]
link=[N53] node=[U15:out_list#Node#U19:list_path_in]
link=[N54] node=[C7:slice#Node#U19:index]
link=[N58] node=[C7:slice#Node#U18:index]
link=[N60] node=[A9:#Node#U15:out_path]
link=[N64] node=[S1:roi_path#Node#U21:roiIJ_file]
link=[N25] node=[U21:coord_roi#Node#S0:coord_roi]
constant=[A8] value=['/tmp/cest_spectr'] format=[path] label=[out_path] RectF=[(-1486.3500000000001, -1480.81, 120.0, 35.0)] 
constant=[A4] value=['value'] format=[str] label=[tag_0] RectF=[(-611.07, -1172.56, 56.0, 35.0)] 
constant=[A3] value=['SatTransFreqRanges'] format=[str] label=[tag] RectF=[(-710.26, -1228.1000000000001, 140.0, 35.0)] 
constant=[A2] value=['.json'] format=[str] label=[new_extension] RectF=[(-1164.3700000000001, -898.83, 52.0, 35.0)] 
constant=[A14] value=['cest_center'] format=[enumerate(('no', 'wassr', 'cest_center'))] label=[A9] RectF=[(-128.68, -636.37, 109.0, 31.0)] 
constant=[A0] value=[(-100000.0, 0.0, 100000.0)] format=[float] label=[ppm] RectF=[(-137.23, -775.74, 131.0, 31.0)] 
constant=[A1] value=[(-100000, -1, 100000)] format=[int] label=[end] RectF=[(-2278.31, -263.8, 87.0, 31.0)] 
constant=[A5] value=[(-100000, -6, 100000)] format=[int] label=[start] RectF=[(-2277.31, -347.8, 87.0, 31.0)] 
constant=[A11] value=['_asym'] format=[str] label=[new_str] RectF=[(-860.5, -97.14, 61.0, 35.0)] 
constant=[A10] value=['_zspectra'] format=[str] label=[new_str] RectF=[(-849.74, -287.59000000000003, 78.0, 35.0)] 
constant=[A7] value=['.csv'] format=[str] label=[stringIn_2] RectF=[(-763.59, -237.87, 47.0, 35.0)] 
constant=[A6] value=['.json'] format=[str] label=[new_extension] RectF=[(-1167.82, -1302.94, 52.0, 35.0)] 
constant=[A9] value=['/tmp/wassr_spectr'] format=[path] label=[out_path] RectF=[(-1423.78, -1159.74, 130.0, 35.0)] 
block=[U13] category=[Nipype.Interfaces_dcmstack] class=[dcmstack_SplitNifti] valInputs=[(['in_file', 'out_path'], ['Node(N2)', 'Node(N59)'], ['out_list'], ['list_path'])] RectF=[(-1273.89, -1567.07, 150.0, 80.0)] 
connt=[C6] name=[asym_out] type=[out] format=[path] RectF=[(2272.0, -615.67, 70, 24)] 
connt=[C5] name=[zspectras_out] type=[out] format=[path] RectF=[(2262.9900000000002, -1105.75, 70, 24)] 
block=[U17] category=[Tools.String] class=[string_concatenat_dyn] valInputs=[(['stringIn', 'stringIn_0', 'stringIn_1', 'stringIn_2'], ['Node(N34)', 'Node(N38)', 'Node(N28)', 'Node(N52)'], ['str_conc'], ['str'])] RectF=[(-603.92, -359.31, 166.77, 84.0)] 
connt=[C4] name=[treatment_dir] type=[in] format=[path] valOut=[path] RectF=[(-2501.64, 236.22, 70, 24)] 
connt=[C3] name=[dir_root] type=[in] format=[path] valOut=[path] RectF=[(-2627.3, -1253.5, 70, 24)] 
connt=[C2] name=[data_list] type=[in] format=[path] valOut=[path] RectF=[(-2621.58, -1348.49, 70, 24)] 
block=[U10] category=[FileIO.Csv] class=[csv_save_file] valInputs=[(['file_output', 'header', 'data'], ['Node(N37)', [''], 'Node(N62)'], ['csv_out'], ['path'])] RectF=[(2003.91, -657.67, 168.09, 84.0)] 
block=[U9] category=[Tools.Float_list] class=[float_list_to_array_dyn] valInputs=[(['list_float_in', 'list_float_in_0'], ['Node(N23)', 'Node(N24)'], ['array'], ['array_float'])] RectF=[(1423.6000000000001, -715.76, 174.98, 86.0)] 
block=[U22] category=[Tools.Float_list] class=[float_list_to_array_dyn] valInputs=[(['list_float_in', 'list_float_in_0'], ['Node(N30)', 'Node(N31)'], ['array'], ['array_float'])] RectF=[(1404.96, -1211.4, 170.98, 82.0)] 
block=[U14] category=[Tools.Path] class=[path_join_dyn] valInputs=[(['path_in', 'path_name'], ['Node(N20)', 'Node(N21)'], ['outFile'], ['path'])] RectF=[(435.07, -83.2, 185.11, 114.89)] 
block=[U5] category=[Tools.Dictionnary] class=[dict_get_value_dyn] valInputs=[(['input_dict', 'tag', 'tag_0'], ['Node(N7)', 'Node(N8)', 'Node(N9)'], ['out_value', 'out_value_dict'], ['str', 'dict'])] RectF=[(-257.57, -1278.13, 229.45000000000002, 134.54)] 
block=[U3] category=[Tools.Path] class=[path_change_extension] valInputs=[(['path_in', 'new_extension'], ['Node(N3)', 'Node(N5)'], ['newPath'], ['path'])] RectF=[(-974.0600000000001, -979.59, 198.97, 84.0)] 
block=[U2] category=[Tools.Path] class=[path_change_extension] valInputs=[(['path_in', 'new_extension'], ['Node(N0)', 'Node(N1)'], ['newPath'], ['path'])] RectF=[(-1061.32, -1348.77, 194.97, 80.0)] 
block=[U1] category=[Images.Nifti] class=[nifti_open_file] valInputs=[(['nifti_file'], ['Node(N48)'], ['image', 'dim', 'pixdim'], ['array_float', 'int', 'list_float'])] RectF=[(-226.05, -1092.31, 154.0, 84.0)] 
block=[U0] category=[Images.Nifti] class=[nifti_open_file] valInputs=[(['nifti_file'], ['Node(N49)'], ['image', 'dim', 'pixdim'], ['array_float', 'int', 'list_float'])] RectF=[(-684.9300000000001, -1548.78, 150.0, 80.0)] 
block=[U4] category=[FileIO.Json] class=[json_open_file] valInputs=[(['json_file'], ['Node(N6)'], ['dict_json'], ['dict'])] RectF=[(-716.47, -1348.63, 155.86, 80.0)] 
block=[U6] category=[Tools.Dictionnary] class=[dict_get_value_dyn] valInputs=[(['input_dict', 'tag', 'tag_0'], ['Node(N13)', 'Node(N15)', 'Node(N14)'], ['out_value', 'out_value_dict'], ['str', 'dict'])] RectF=[(-251.73000000000002, -963.1800000000001, 233.45000000000002, 138.54)] 
block=[U7] category=[FileIO.Json] class=[json_open_file] valInputs=[(['json_file'], ['Node(N12)'], ['dict_json'], ['dict'])] RectF=[(-691.1800000000001, -975.95, 159.86, 84.0)] 
script=[S0] title=[Script_editor] inputs=[['cest_img', 'in', 'array_float'], ['cest_range', 'in', 'array_float'], ['wassr_img', 'in', 'array_float'], ['wassr_range', 'in', 'array_float'], ['ppm', 'in', 'float'], ['correction_B0', 'in', 'str'], ['coord_roi', 'in', 'list_float']] outputs=[['y_cest', 'out', 'array_float'], ['y_cest_mean', 'out', 'list_float'], ['x_cest', 'out', 'list_float'], ['y_asym', 'out', 'array_float'], ['y_asym_mean', 'out', 'list_float'], ['x_asym', 'out', 'array_float'], ['map_asym', 'out', 'array_float']] code=[your code] RectF=[(156.86, -1550.93, 599.0, 1268.0)]
script=[S1] title=[Script_editor] inputs=[['file_list', 'in', 'path'], ['dir_root', 'in', 'path'], ['subject', 'in', 'str'], ['roi_name', 'in', 'str']] outputs=[['cest_path', 'out', 'path'], ['wassr_path', 'out', 'path'], ['roi_path', 'out', 'path'], ['roi_nameout', 'out', 'str']] code=[your code] RectF=[(-2362.81, -1407.02, 489.0, 389.0)]
block=[U16] category=[FileIO.Csv] class=[csv_save_file] valInputs=[(['file_output', 'header', 'data'], ['Node(N35)', [''], 'Node(N61)'], ['csv_out'], ['path'])] RectF=[(2001.92, -1115.3700000000001, 164.09, 80.0)] 
block=[U24] category=[Numpy.Nd_manipulation] class=[numpy_transpose] valInputs=[(['a'], ['Node(N55)'], ['np_transpose'], ['array_float'])] RectF=[(1647.28, -1209.69, 150.0, 80.0)] 
block=[U25] category=[Numpy.Nd_manipulation] class=[numpy_transpose] valInputs=[(['a'], ['Node(N22)'], ['np_transpose'], ['array_float'])] RectF=[(1674.65, -735.38, 154.0, 84.0)] 
connt=[C0] name=[subject] type=[in] format=[str] valOut=[] RectF=[(-2636.61, -978.98, 70, 24)] 
connt=[C1] name=[roi_name] type=[in] format=[str] valOut=[] RectF=[(-2640.57, -868.19, 70, 24)] 
block=[U8] category=[Tools.String] class=[string_substring] valInputs=[(['in_string', 'start', 'end'], ['Node(N45)', 'Node(N56)', 'Node(N46)'], ['substring'], ['str'])] RectF=[(-2079.81, -380.3, 163.23, 82.0)] 
block=[U20] category=[Tools.String] class=[string_concatenat_dyn] valInputs=[(['stringIn', 'stringIn_0', 'stringIn_1', 'stringIn_2'], ['Node(N41)', 'Node(N39)', 'Node(N36)', 'Node(N57)'], ['str_conc'], ['str'])] RectF=[(-617.96, -170.4, 166.77, 88.0)] 
block=[U12] category=[Tools.Path] class=[path_join_dyn] valInputs=[(['path_in', 'path_name'], ['Node(N33)', 'Node(N32)'], ['outFile'], ['path'])] RectF=[(430.87, 126.92, 187.11, 116.89)] 
block=[U18] category=[Tools.Path_list] class=[path_list_getElement] valInputs=[(['list_path_in', 'index'], ['Node(N50)', 'Node(N58)'], ['outPath'], ['path'])] RectF=[(-987.71, -1535.23, 171.0, 80.0)] 
block=[U19] category=[Tools.Path_list] class=[path_list_getElement] valInputs=[(['list_path_in', 'index'], ['Node(N53)', 'Node(N54)'], ['outPath'], ['path'])] RectF=[(-934.73, -1137.16, 171.0, 80.0)] 
connt=[C7] name=[slice] type=[in] format=[int] valOut=[0] RectF=[(-2628.33, -717.7, 70, 24)] 
block=[U15] category=[Nipype.Interfaces_dcmstack] class=[dcmstack_SplitNifti] valInputs=[(['in_file', 'out_path'], ['Node(N4)', 'Node(N60)'], ['out_list'], ['list_path'])] RectF=[(-1208.98, -1211.72, 150.0, 80.0)] 
block=[U21] category=[Images.ImageJ] class=[ImageJ_get_coord_roi] valInputs=[(['image_in', 'roiIJ_file', 'roi_name'], ['Node(N65)', 'Node(N64)', 'Node(N63)'], ['coord_roi'], ['list_float'])] RectF=[(-315.68, -530.29, 168.44, 128.96)] 
[source S0]
['coord_roi=U21:coord_roi', 'ppm=0.0', 'wassr_img=U1:image', 'cest_img=U0:image', 'cest_range=U5:out_value', 'wassr_range=U6:out_value', "correction_B0='cest_center'"]
from NodeEditor.modules.Tools.Float_array import float_array_add_row
from NodeEditor.modules.MRImaging.Irmage import CEST
from NodeEditor.modules.MRImaging.Irmage import WASSR
import numpy as np

xmin = cest_range[0][0]
xmax = cest_range[1][0]
delta_x = cest_range[2][0]
x_cest = np.linspace(xmin,  xmax, int(1 + (xmax - xmin) / delta_x))

#################################################

xmin = wassr_range[0][0]
xmax = wassr_range[1][0]
delta_x = wassr_range[2][0]
x_wassr= np.linspace(xmin,  xmax, int(1 + (xmax - xmin) / delta_x))

#################################################

sub_cest = np.squeeze(cest_img)
sub_wassr = np.squeeze(wassr_img)

if len(x_wassr) == len(sub_wassr[0, 0, :]):
    x_wassr = x_wassr[0:-1]

x_img, y_img, z_img = np.shape(sub_cest)
map_asym = sub_cest[:, :, 0]

y_cest, y_asym, x_asym, S0_cest = [], [], [], []

for i in range(x_img):
    for j in range(y_img):
        if sub_cest[i, j, 0] >10.0:
            try:
                cp = 0.0
                cest_cent = False
                if correction_B0 == 'wassr':
                    cp = WASSR(sub_wassr[i, j, :], x_wassr).estimated_center_freq()
                    cest_cent = False
                elif correction_B0 == 'cest_center':
                    cest_cent = True
                vr = CEST(sub_cest[i, j, :], x_cest, cp, ppm, 0.1, cest_cent)
                so = sub_cest[i, j, 0]
                map_asym[i, j] = vr.out_mapping()
                if [j, i] in coord_roi.tolist():
                    y_cest.append(vr.out_zspectra())
                    y_asym.append(vr.out_asym())
                    S0_cest.append(so)
                    #x_asym.append(vr.out_xasym())
            except Exception as err:
                print('error :', err)
                map_asym[ i, j] = 0.0
        else:
            map_asym[ i, j] = 0.0

#y_cest = np.array(y_cest)
y_cest_mean = np.mean( y_cest, axis=0 )
y_asym_mean = np.mean(y_asym, axis=0)
S0_cest_mean = np.mean(S0_cest)
x_cest = vr.out_xspectra()
x_asym = vr.out_xasym()

y_cest_mean = np.insert(y_cest_mean, 0, S0_cest_mean)
x_cest = np.insert(x_cest, 0, 0) 

['S0:y_cest', 'S0:y_cest_mean', 'S0:x_cest', 'S0:y_asym', 'S0:y_asym_mean', 'S0:x_asym', 'S0:map_asym']
[/source S0]
[source S1]
['roi_name=C1:roi_name', 'subject=C0:subject', 'file_list=C2:data_list', 'dir_root=C3:dir_root']
from NodeEditor.modules.FileIO.Yml import open_yaml_file
from NodeEditor.modules.Images.ImageJ import ImageJ_read_roi
import os

lst_f = open_yaml_file(file_list).dict_yaml()

cest_path = os.path.join(dir_root, lst_f[subject]['path_cest'])
wassr_path = os.path.join(dir_root, lst_f[subject]['path_wassr'])
roi_path = os.path.join(dir_root, lst_f[subject]['roi_zip_path'])

lst_roi = list(ImageJ_read_roi(roi_path).list_Rois().keys())
print('Roi list :', lst_roi)
roi_nameout = roi_name

if roi_name not in lst_roi:
    roi_nameout = lst_roi[0]

['S1:cest_path', 'S1:wassr_path', 'S1:roi_path', 'S1:roi_nameout']
[/source S1]

[execution]
['C2:data_list=', 'C3:dir_root=', 'C0:subject=', 'C1:roi_name=', 'C7:slice=', 'C4:treatment_dir=']
['S1', 'U8', 'ThreadOn', 'U2', 'U3', 'U17', 'U20', 'U13', 'U15', 'ThreadOff', 'ThreadOn', 'U12', 'U14', 'U7', 'U4', 'U18', 'U19', 'ThreadOff', 'ThreadOn', 'U5', 'U6', 'U1', 'U0', 'ThreadOff', 'U21', 'S0', 'ThreadOn', 'U22', 'U9', 'ThreadOff', 'ThreadOn', 'U25', 'U24', 'ThreadOff', 'U10', 'U16']
{'U8': ('Tools.String', 'string_substring', "(['in_string', 'start', 'end'], ['C0:subject', -6, -1], ['substring'], ['str'])"), 'U2': ('Tools.Path', 'path_change_extension', "(['path_in', 'new_extension'], ['S1:cest_path', '.json'], ['newPath'], ['path'])"), 'U3': ('Tools.Path', 'path_change_extension', "(['path_in', 'new_extension'], ['S1:wassr_path', '.json'], ['newPath'], ['path'])"), 'U17': ('Tools.String', 'string_concatenat_dyn', "(['stringIn', 'stringIn_0', 'stringIn_1', 'stringIn_2'], ['S1:roi_nameout', 'U8:substring', '_zspectra', '.csv'], ['str_conc'], ['str'])"), 'U20': ('Tools.String', 'string_concatenat_dyn', "(['stringIn', 'stringIn_0', 'stringIn_1', 'stringIn_2'], ['S1:roi_nameout', 'U8:substring', '_asym', '.csv'], ['str_conc'], ['str'])"), 'U13': ('Nipype.Interfaces_dcmstack', 'dcmstack_SplitNifti', "(['in_file', 'out_path'], ['S1:cest_path', '/tmp/cest_spectr'], ['out_list'], ['list_path'])"), 'U15': ('Nipype.Interfaces_dcmstack', 'dcmstack_SplitNifti', "(['in_file', 'out_path'], ['S1:wassr_path', '/tmp/wassr_spectr'], ['out_list'], ['list_path'])"), 'U12': ('Tools.Path', 'path_join_dyn', "(['path_in', 'path_name'], ['C4:treatment_dir', 'U20:str_conc'], ['outFile'], ['path'])"), 'U14': ('Tools.Path', 'path_join_dyn', "(['path_in', 'path_name'], ['C4:treatment_dir', 'U17:str_conc'], ['outFile'], ['path'])"), 'U7': ('FileIO.Json', 'json_open_file', "(['json_file'], ['U3:newPath'], ['dict_json'], ['dict'])"), 'U4': ('FileIO.Json', 'json_open_file', "(['json_file'], ['U2:newPath'], ['dict_json'], ['dict'])"), 'U18': ('Tools.Path_list', 'path_list_getElement', "(['list_path_in', 'index'], ['U13:out_list', 'C7:slice'], ['outPath'], ['path'])"), 'U19': ('Tools.Path_list', 'path_list_getElement', "(['list_path_in', 'index'], ['U15:out_list', 'C7:slice'], ['outPath'], ['path'])"), 'U5': ('Tools.Dictionnary', 'dict_get_value_dyn', "(['input_dict', 'tag', 'tag_0'], ['U4:dict_json', 'SatTransFreqRanges', 'value'], ['out_value', 'out_value_dict'], ['str', 'dict'])"), 'U6': ('Tools.Dictionnary', 'dict_get_value_dyn', "(['input_dict', 'tag', 'tag_0'], ['U7:dict_json', 'SatTransFreqRanges', 'value'], ['out_value', 'out_value_dict'], ['str', 'dict'])"), 'U1': ('Images.Nifti', 'nifti_open_file', "(['nifti_file'], ['U19:outPath'], ['image', 'dim', 'pixdim'], ['array_float', 'int', 'list_float'])"), 'U0': ('Images.Nifti', 'nifti_open_file', "(['nifti_file'], ['U18:outPath'], ['image', 'dim', 'pixdim'], ['array_float', 'int', 'list_float'])"), 'U21': ('Images.ImageJ', 'ImageJ_get_coord_roi', "(['image_in', 'roiIJ_file', 'roi_name'], ['U0:image', 'S1:roi_path', 'S1:roi_nameout'], ['coord_roi'], ['list_float'])"), 'U22': ('Tools.Float_list', 'float_list_to_array_dyn', "(['list_float_in', 'list_float_in_0'], ['S0:x_cest', 'S0:y_cest_mean'], ['array'], ['array_float'])"), 'U9': ('Tools.Float_list', 'float_list_to_array_dyn', "(['list_float_in', 'list_float_in_0'], ['S0:x_asym', 'S0:y_asym_mean'], ['array'], ['array_float'])"), 'U25': ('Numpy.Nd_manipulation', 'numpy_transpose', "(['a'], ['U9:array'], ['np_transpose'], ['array_float'])"), 'U24': ('Numpy.Nd_manipulation', 'numpy_transpose', "(['a'], ['U22:array'], ['np_transpose'], ['array_float'])"), 'U10': ('FileIO.Csv', 'csv_save_file', "(['file_output', 'header', 'data'], ['U12:outFile', [''], 'U25:np_transpose'], ['csv_out'], ['path'])"), 'U16': ('FileIO.Csv', 'csv_save_file', "(['file_output', 'header', 'data'], ['U14:outFile', [''], 'U24:np_transpose'], ['csv_out'], ['path'])")}
['U0:image', 'S1:roi_nameout', 'U10:csv_out', 'U16:csv_out', 'U12:outFile', 'U14:outFile', 'U20:str_conc', 'U17:str_conc', 'U25:np_transpose', 'U9:array', 'U6:out_value', 'U5:out_value', 'U3:newPath', 'U2:newPath', 'U4:dict_json', 'U7:dict_json', 'U0:image', 'U1:image', 'S1:cest_path', 'S1:wassr_path', 'S0:x_cest', 'S0:y_cest_mean', 'S0:x_asym', 'S0:y_asym_mean', 'U22:array', 'U24:np_transpose', 'S1:roi_nameout', 'S1:roi_nameout', 'U8:substring', 'U8:substring', 'S1:cest_path', 'S1:wassr_path', 'U19:outPath', 'U18:outPath', 'U13:out_list', 'U15:out_list', 'S1:roi_path', 'U21:coord_roi']
{}
['C5:zspectras_out=U16:csv_out', 'C6:asym_out=U10:csv_out']
[interlinks]
[]
