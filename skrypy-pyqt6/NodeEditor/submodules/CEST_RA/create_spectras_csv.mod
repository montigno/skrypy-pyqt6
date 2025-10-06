[diagram]
link=[N53] node=[U0:image#Node#U8:image_in]
link=[N50] node=[S1:roi_nameout#Node#U8:roi_name]
link=[N49] node=[S1:roi_nameout#Node#U17:stringIn_1]
link=[N48] node=[S1:roi_nameout#Node#U20:stringIn_1]
link=[N46] node=[A1:#Node#U20:stringIn_0]
link=[N45] node=[A1:#Node#U17:stringIn_0]
link=[N36] node=[A11:#Node#U20:stringIn_2]
link=[N28] node=[A10:#Node#U17:stringIn_2]
link=[N41] node=[A7:#Node#U20:stringIn_3]
link=[N39] node=[A7:#Node#U17:stringIn_3]
link=[N38] node=[C0:subject#Node#U20:stringIn]
link=[N34] node=[C0:subject#Node#U17:stringIn]
link=[N44] node=[A0:#Node#S0:ppm]
link=[N47] node=[C1:roi_name#Node#S1:roi_name]
link=[N29] node=[C0:subject#Node#S1:subject]
link=[N61] node=[U24:np_transpose#Node#U16:data]
link=[N55] node=[U22:array#Node#U24:a]
link=[N24] node=[S0:y_asym_mean#Node#U9:list_float_in_0]
link=[N23] node=[S0:x_asym#Node#U9:list_float_in]
link=[N31] node=[S0:y_cest_mean#Node#U22:list_float_in_0]
link=[N30] node=[S0:x_cest#Node#U22:list_float_in]
link=[N3] node=[S1:wassr_path#Node#U3:path_in]
link=[N1] node=[S1:wassr_path#Node#U1:nifti_file]
link=[N2] node=[S1:cest_path#Node#U0:nifti_file]
link=[N0] node=[S1:cest_path#Node#U2:path_in]
link=[N17] node=[U1:image#Node#S0:wassr_img]
link=[N16] node=[U0:image#Node#S0:cest_img]
link=[N13] node=[U7:dict_json#Node#U6:input_dict]
link=[N8] node=[A3:#Node#U5:tag]
link=[N7] node=[U4:dict_json#Node#U5:input_dict]
link=[N6] node=[U2:newPath#Node#U4:json_file]
link=[N5] node=[A2:#Node#U3:new_extension]
link=[N4] node=[A2:#Node#U2:new_extension]
link=[N9] node=[A4:#Node#U5:tag_0]
link=[N12] node=[U3:newPath#Node#U7:json_file]
link=[N14] node=[A4:#Node#U6:tag_0]
link=[N15] node=[A3:#Node#U6:tag]
link=[N10] node=[U5:out_value#Node#S0:cest_range]
link=[N11] node=[U6:out_value#Node#S0:wassr_range]
link=[N42] node=[A14:#Node#S0:correction_B0]
link=[N22] node=[U9:array#Node#U25:a]
link=[N62] node=[U25:np_transpose#Node#U10:data]
link=[N18] node=[C2:data_list#Node#S1:file_list]
link=[N19] node=[C3:dir_root#Node#S1:dir_root]
link=[N20] node=[C4:treatment_dir#Node#U14:path_in]
link=[N21] node=[U17:str_conc#Node#U14:path_name]
link=[N32] node=[U20:str_conc#Node#U12:path_name]
link=[N33] node=[C4:treatment_dir#Node#U12:path_in]
link=[N35] node=[U14:outFile#Node#U16:file_output]
link=[N37] node=[U12:outFile#Node#U10:file_output]
link=[N40] node=[U16:csv_out#Node#C5:zspectras_out]
link=[N43] node=[U10:csv_out#Node#C6:asym_out]
link=[N52] node=[S1:roi_path#Node#U8:roiIJ_file]
link=[N25] node=[U8:coord_roi#Node#S0:coord_roi]
constant=[A1] value=['_'] format=[str] label=[stringIn_1] RectF=[(-910.21, -205.07, 32.0, 35.0)] 
constant=[A7] value=['.csv'] format=[str] label=[stringIn_2] RectF=[(-768.5, -203.48000000000002, 47.0, 35.0)] 
constant=[A10] value=['_zspectra'] format=[str] label=[new_str] RectF=[(-930.8000000000001, -276.94, 78.0, 35.0)] 
constant=[A11] value=['_asym'] format=[str] label=[new_str] RectF=[(-776.98, -96.32000000000001, 61.0, 35.0)] 
constant=[A0] value=[(-100000.0, 4.3, 100000.0)] format=[float] label=[ppm] RectF=[(-107.65, -772.57, 131.0, 31.0)] 
constant=[A14] value=['cest_center'] format=[enumerate(('no', 'wassr', 'cest_center'))] label=[A9] RectF=[(-128.68, -636.37, 109.0, 31.0)] 
constant=[A2] value=['.json'] format=[str] label=[new_extension] RectF=[(-1402.95, -1262.88, 52.0, 35.0)] 
constant=[A3] value=['SatTransFreqRanges'] format=[str] label=[tag] RectF=[(-674.5, -1172.73, 140.0, 35.0)] 
constant=[A4] value=['value'] format=[str] label=[tag_0] RectF=[(-594.32, -1084.58, 56.0, 35.0)] 
block=[U8] category=[Images.ImageJ] class=[ImageJ_get_coord_roi] valInputs=[(['image_in', 'roiIJ_file', 'roi_name'], ['Node(N53)', 'Node(N52)', 'Node(N50)'], ['coord_roi'], ['list_float'])] RectF=[(-339.42, -562.58, 181.82, 150.27)] 
block=[U20] category=[Tools.String] class=[string_concatenat_dyn] valInputs=[(['stringIn', 'stringIn_0', 'stringIn_1', 'stringIn_2', 'stringIn_3'], ['Node(N38)', 'Node(N46)', 'Node(N48)', 'Node(N36)', 'Node(N41)'], ['str_conc'], ['str'])] RectF=[(-600.57, -165.05, 189.5, 128.13)] 
block=[U12] category=[Tools.Path] class=[path_join_dyn] valInputs=[(['path_in', 'path_name'], ['Node(N33)', 'Node(N32)'], ['outFile'], ['path'])] RectF=[(430.87, 126.92, 187.11, 116.89)] 
connt=[C1] name=[roi_name] type=[in] format=[str] valOut=[] RectF=[(-2601.73, -676.65, 70, 24)] 
connt=[C0] name=[subject] type=[in] format=[str] valOut=[] RectF=[(-2597.77, -787.44, 70, 24)] 
block=[U25] category=[Numpy.Nd_manipulation] class=[numpy_transpose] valInputs=[(['a'], ['Node(N22)'], ['np_transpose'], ['array_float'])] RectF=[(1674.65, -735.38, 154.0, 84.0)] 
block=[U24] category=[Numpy.Nd_manipulation] class=[numpy_transpose] valInputs=[(['a'], ['Node(N55)'], ['np_transpose'], ['array_float'])] RectF=[(1647.28, -1209.69, 150.0, 80.0)] 
block=[U16] category=[FileIO.Csv] class=[csv_save_file] valInputs=[(['file_output', 'header', 'data'], ['Node(N35)', [''], 'Node(N61)'], ['csv_out'], ['path'])] RectF=[(2001.92, -1115.3700000000001, 164.09, 80.0)] 
script=[S1] title=[Script_editor] inputs=[['file_list', 'in', 'path'], ['dir_root', 'in', 'path'], ['subject', 'in', 'str'], ['roi_name', 'in', 'str']] outputs=[['cest_path', 'out', 'path'], ['wassr_path', 'out', 'path'], ['roi_path', 'out', 'path'], ['roi_nameout', 'out', 'str']] code=[your code] RectF=[(-2075.94, -1326.69, 523.0, 489.0)]
script=[S0] title=[Script_editor] inputs=[['cest_img', 'in', 'array_float'], ['cest_range', 'in', 'array_float'], ['wassr_img', 'in', 'array_float'], ['wassr_range', 'in', 'array_float'], ['ppm', 'in', 'float'], ['correction_B0', 'in', 'str'], ['coord_roi', 'in', 'list_float']] outputs=[['y_cest', 'out', 'array_float'], ['y_cest_mean', 'out', 'list_float'], ['x_cest', 'out', 'list_float'], ['y_asym', 'out', 'array_float'], ['y_asym_mean', 'out', 'list_float'], ['x_asym', 'out', 'array_float'], ['map_asym', 'out', 'array_float']] code=[your code] RectF=[(156.86, -1550.93, 599.0, 1268.0)]
block=[U7] category=[FileIO.Json] class=[json_open_file] valInputs=[(['json_file'], ['Node(N12)'], ['dict_json'], ['dict'])] RectF=[(-642.28, -967.0600000000001, 159.86, 84.0)] 
block=[U6] category=[Tools.Dictionnary] class=[dict_get_value_dyn] valInputs=[(['input_dict', 'tag', 'tag_0'], ['Node(N13)', 'Node(N15)', 'Node(N14)'], ['out_value', 'out_value_dict'], ['str', 'dict'])] RectF=[(-230.54, -960.61, 233.45000000000002, 138.54)] 
block=[U4] category=[FileIO.Json] class=[json_open_file] valInputs=[(['json_file'], ['Node(N6)'], ['dict_json'], ['dict'])] RectF=[(-671.19, -1342.16, 155.86, 80.0)] 
block=[U0] category=[Images.Nifti] class=[nifti_open_file] valInputs=[(['nifti_file'], ['Node(N2)'], ['image', 'dim', 'pixdim'], ['array_float', 'int', 'list_float'])] RectF=[(-1180.78, -1615.6100000000001, 150.0, 80.0)] 
block=[U1] category=[Images.Nifti] class=[nifti_open_file] valInputs=[(['nifti_file'], ['Node(N1)'], ['image', 'dim', 'pixdim'], ['array_float', 'int', 'list_float'])] RectF=[(-1180.3600000000001, -1258.43, 154.0, 84.0)] 
block=[U2] category=[Tools.Path] class=[path_change_extension] valInputs=[(['path_in', 'new_extension'], ['Node(N0)', 'Node(N4)'], ['newPath'], ['path'])] RectF=[(-1202.28, -1451.16, 194.97, 80.0)] 
block=[U3] category=[Tools.Path] class=[path_change_extension] valInputs=[(['path_in', 'new_extension'], ['Node(N3)', 'Node(N5)'], ['newPath'], ['path'])] RectF=[(-1205.14, -1096.26, 198.97, 84.0)] 
block=[U5] category=[Tools.Dictionnary] class=[dict_get_value_dyn] valInputs=[(['input_dict', 'tag', 'tag_0'], ['Node(N7)', 'Node(N8)', 'Node(N9)'], ['out_value', 'out_value_dict'], ['str', 'dict'])] RectF=[(-344.17, -1313.47, 229.45000000000002, 134.54)] 
block=[U14] category=[Tools.Path] class=[path_join_dyn] valInputs=[(['path_in', 'path_name'], ['Node(N20)', 'Node(N21)'], ['outFile'], ['path'])] RectF=[(435.07, -83.2, 185.11, 114.89)] 
block=[U22] category=[Tools.Float_list] class=[float_list_to_array_dyn] valInputs=[(['list_float_in', 'list_float_in_0'], ['Node(N30)', 'Node(N31)'], ['array'], ['array_float'])] RectF=[(1404.96, -1211.4, 170.98, 82.0)] 
block=[U9] category=[Tools.Float_list] class=[float_list_to_array_dyn] valInputs=[(['list_float_in', 'list_float_in_0'], ['Node(N23)', 'Node(N24)'], ['array'], ['array_float'])] RectF=[(1427.15, -735.27, 174.98, 86.0)] 
block=[U10] category=[FileIO.Csv] class=[csv_save_file] valInputs=[(['file_output', 'header', 'data'], ['Node(N37)', [''], 'Node(N62)'], ['csv_out'], ['path'])] RectF=[(2003.91, -657.67, 168.09, 84.0)] 
connt=[C2] name=[data_list] type=[in] format=[path] valOut=[path] RectF=[(-2584.28, -1245.22, 70, 24)] 
connt=[C3] name=[dir_root] type=[in] format=[path] valOut=[path] RectF=[(-2590.01, -1150.22, 70, 24)] 
connt=[C4] name=[treatment_dir] type=[in] format=[path] valOut=[path] RectF=[(-2580.15, 225.51, 70, 24)] 
connt=[C5] name=[zspectras_out] type=[out] format=[path] RectF=[(2262.9900000000002, -1105.75, 70, 24)] 
connt=[C6] name=[asym_out] type=[out] format=[path] RectF=[(2272.0, -615.67, 70, 24)] 
block=[U17] category=[Tools.String] class=[string_concatenat_dyn] valInputs=[(['stringIn', 'stringIn_0', 'stringIn_1', 'stringIn_2', 'stringIn_3'], ['Node(N34)', 'Node(N45)', 'Node(N49)', 'Node(N28)', 'Node(N39)'], ['str_conc'], ['str'])] RectF=[(-603.92, -359.31, 185.49, 118.78)] 
[source S0]
['coord_roi=U8:coord_roi', "correction_B0='cest_center'", 'wassr_range=U6:out_value', 'cest_range=U5:out_value', 'cest_img=U0:image', 'wassr_img=U1:image', 'ppm=4.3']
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

print("CEST, WASSR", len(x_wassr), len(sub_wassr[0, 0, :]))

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
                print('script error :', err)
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
['dir_root=C3:dir_root', 'file_list=C2:data_list', 'subject=C0:subject', 'roi_name=C1:roi_name']
from NodeEditor.modules.FileIO.Yml import yaml_open_file
from NodeEditor.modules.Images.ImageJ import ImageJ_read_roi
import os

lst_f = yaml_open_file(file_list).dict_yaml()

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
['C2:data_list=', 'C3:dir_root=', 'C0:subject=', 'C1:roi_name=', 'C4:treatment_dir=']
['S1', 'ThreadOn', 'U17', 'U20', 'U3', 'U1', 'U0', 'U2', 'ThreadOff', 'ThreadOn', 'U8', 'U4', 'U7', 'U14', 'U12', 'ThreadOff', 'ThreadOn', 'U6', 'U5', 'ThreadOff', 'S0', 'ThreadOn', 'U9', 'U22', 'ThreadOff', 'ThreadOn', 'U24', 'U25', 'ThreadOff', 'U10', 'U16']
{'U17': ('Tools.String', 'string_concatenat_dyn', "(['stringIn', 'stringIn_0', 'stringIn_1', 'stringIn_2', 'stringIn_3'], ['C0:subject', '_', 'S1:roi_nameout', '_zspectra', '.csv'], ['str_conc'], ['str'])"), 'U20': ('Tools.String', 'string_concatenat_dyn', "(['stringIn', 'stringIn_0', 'stringIn_1', 'stringIn_2', 'stringIn_3'], ['C0:subject', '_', 'S1:roi_nameout', '_asym', '.csv'], ['str_conc'], ['str'])"), 'U3': ('Tools.Path', 'path_change_extension', "(['path_in', 'new_extension'], ['S1:wassr_path', '.json'], ['newPath'], ['path'])"), 'U1': ('Images.Nifti', 'nifti_open_file', "(['nifti_file'], ['S1:wassr_path'], ['image', 'dim', 'pixdim'], ['array_float', 'int', 'list_float'])"), 'U0': ('Images.Nifti', 'nifti_open_file', "(['nifti_file'], ['S1:cest_path'], ['image', 'dim', 'pixdim'], ['array_float', 'int', 'list_float'])"), 'U2': ('Tools.Path', 'path_change_extension', "(['path_in', 'new_extension'], ['S1:cest_path', '.json'], ['newPath'], ['path'])"), 'U8': ('Images.ImageJ', 'ImageJ_get_coord_roi', "(['image_in', 'roiIJ_file', 'roi_name'], ['U0:image', 'S1:roi_path', 'S1:roi_nameout'], ['coord_roi'], ['list_float'])"), 'U4': ('FileIO.Json', 'json_open_file', "(['json_file'], ['U2:newPath'], ['dict_json'], ['dict'])"), 'U7': ('FileIO.Json', 'json_open_file', "(['json_file'], ['U3:newPath'], ['dict_json'], ['dict'])"), 'U14': ('Tools.Path', 'path_join_dyn', "(['path_in', 'path_name'], ['C4:treatment_dir', 'U17:str_conc'], ['outFile'], ['path'])"), 'U12': ('Tools.Path', 'path_join_dyn', "(['path_in', 'path_name'], ['C4:treatment_dir', 'U20:str_conc'], ['outFile'], ['path'])"), 'U6': ('Tools.Dictionnary', 'dict_get_value_dyn', "(['input_dict', 'tag', 'tag_0'], ['U7:dict_json', 'SatTransFreqRanges', 'value'], ['out_value', 'out_value_dict'], ['str', 'dict'])"), 'U5': ('Tools.Dictionnary', 'dict_get_value_dyn', "(['input_dict', 'tag', 'tag_0'], ['U4:dict_json', 'SatTransFreqRanges', 'value'], ['out_value', 'out_value_dict'], ['str', 'dict'])"), 'U9': ('Tools.Float_list', 'float_list_to_array_dyn', "(['list_float_in', 'list_float_in_0'], ['S0:x_asym', 'S0:y_asym_mean'], ['array'], ['array_float'])"), 'U22': ('Tools.Float_list', 'float_list_to_array_dyn', "(['list_float_in', 'list_float_in_0'], ['S0:x_cest', 'S0:y_cest_mean'], ['array'], ['array_float'])"), 'U24': ('Numpy.Nd_manipulation', 'numpy_transpose', "(['a'], ['U22:array'], ['np_transpose'], ['array_float'])"), 'U25': ('Numpy.Nd_manipulation', 'numpy_transpose', "(['a'], ['U9:array'], ['np_transpose'], ['array_float'])"), 'U10': ('FileIO.Csv', 'csv_save_file', "(['file_output', 'header', 'data'], ['U12:outFile', [''], 'U25:np_transpose'], ['csv_out'], ['path'])"), 'U16': ('FileIO.Csv', 'csv_save_file', "(['file_output', 'header', 'data'], ['U14:outFile', [''], 'U24:np_transpose'], ['csv_out'], ['path'])")}
['U0:image', 'S1:roi_nameout', 'S1:roi_nameout', 'S1:roi_nameout', 'U24:np_transpose', 'U22:array', 'S0:y_asym_mean', 'S0:x_asym', 'S0:y_cest_mean', 'S0:x_cest', 'S1:wassr_path', 'S1:wassr_path', 'S1:cest_path', 'S1:cest_path', 'U1:image', 'U0:image', 'U7:dict_json', 'U4:dict_json', 'U2:newPath', 'U3:newPath', 'U5:out_value', 'U6:out_value', 'U9:array', 'U25:np_transpose', 'U17:str_conc', 'U20:str_conc', 'U14:outFile', 'U12:outFile', 'U16:csv_out', 'U10:csv_out', 'S1:roi_path', 'U8:coord_roi']
{}
['C5:zspectras_out=U16:csv_out', 'C6:asym_out=U10:csv_out']
[interlinks]
[]
