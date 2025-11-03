[diagram]
link=[N41] node=[U17:temp_folder#Node#U20:path_in]
link=[N40] node=[A1:#Node#U20:path_name]
link=[N38] node=[U13:temp_folder#Node#U16:path_in]
link=[N37] node=[A8:#Node#U10:split_dim]
link=[N35] node=[C6:slice#Node#U11:index]
link=[N34] node=[C6:slice#Node#U12:index]
link=[N33] node=[U10:out_list#Node#U12:list_path_in]
link=[N32] node=[U12:outPath#Node#U1:nifti_file]
link=[N31] node=[U11:outPath#Node#U0:nifti_file]
link=[N28] node=[U9:out_list#Node#U11:list_path_in]
link=[N2] node=[S1:cest_path#Node#U9:in_file]
link=[N1] node=[S1:wassr_path#Node#U10:in_file]
link=[N26] node=[C4:treatment_dir#Node#U14:path_in]
link=[N25] node=[C3:ppm#Node#U19:stringIn_0]
link=[N18] node=[C3:ppm#Node#S0:ppm]
link=[N24] node=[C2:subject#Node#U15:stringIn]
link=[N23] node=[C2:subject#Node#S1:subject]
link=[N22] node=[C1:dir_root#Node#S1:dir_root]
link=[N21] node=[C0:data_list#Node#S1:file_list]
link=[N49] node=[U15:str_conc#Node#U14:path_name]
link=[N48] node=[A6:#Node#U15:stringIn_0]
link=[N19] node=[S0:map_asym#Node#U8:image]
link=[N3] node=[S1:wassr_path#Node#U3:path_in]
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
link=[N56] node=[A7:#Node#U19:stringIn]
link=[N58] node=[A17:#Node#U19:stringIn_1]
link=[N59] node=[U19:str_conc#Node#U18:new_str]
link=[N20] node=[U14:outFile#Node#U18:path_in]
link=[N60] node=[U18:newPath#Node#U8:nifti_path]
link=[N27] node=[U8:pathFile#Node#C5:out_map]
link=[N36] node=[A5:#Node#U9:split_dim]
link=[N30] node=[A9:#Node#U16:path_name]
link=[N39] node=[U16:outFile#Node#U9:out_path]
link=[N29] node=[U20:outFile#Node#U10:out_path]
constant=[A1] value=['wasse_tmp.nii'] format=[str] label=[path_name] RectF=[(-1659.98, -754.36, 105.0, 35.0)] 
constant=[A8] value=[(-100000, 2, 100000)] format=[int] label=[split_dim] RectF=[(-1306.8700000000001, -983.65, 87.0, 31.0)] 
constant=[A14] value=['cest_center'] format=[enumerate(('no', 'wassr', 'cest_center'))] label=[A9] RectF=[(-120.12, -474.85, 109.0, 31.0)] 
constant=[A2] value=['.json'] format=[str] label=[new_extension] RectF=[(-1263.3700000000001, -1048.41, 52.0, 35.0)] 
constant=[A6] value=['.nii'] format=[str] label=[stringIn_0] RectF=[(-2000.3700000000001, -637.62, 42.0, 35.0)] 
constant=[A3] value=['SatTransFreqRanges'] format=[str] label=[tag] RectF=[(-674.5, -1172.73, 140.0, 35.0)] 
constant=[A4] value=['value'] format=[str] label=[tag_0] RectF=[(-594.32, -1084.58, 56.0, 35.0)] 
constant=[A17] value=['ppm'] format=[str] label=[stringIn_1] RectF=[(-985.6800000000001, 276.74, 51.0, 35.0)] 
constant=[A7] value=['_'] format=[str] label=[stringIn] RectF=[(-962.54, 156.81, 32.0, 35.0)] 
constant=[A5] value=[(-100000, 2, 100000)] format=[int] label=[split_dim] RectF=[(-1355.99, -1529.7, 87.0, 31.0)] 
constant=[A9] value=['cest_tmp.nii'] format=[str] label=[path_name] RectF=[(-1712.92, -1579.3, 93.0, 35.0)] 
block=[U20] category=[Tools.Path] class=[path_join_dyn] valInputs=[(['path_in', 'path_name'], ['Node(N41)', 'Node(N40)'], ['outFile'], ['path'])] RectF=[(-1519.05, -828.85, 162.33, 82.0)] 
block=[U17] category=[FileIO.Tools] class=[get_temporary_folder] valInputs=[([], [], ['temp_folder'], ['path'])] RectF=[(-1726.54, -874.5600000000001, 152.0, 82.0)] 
block=[U16] category=[Tools.Path] class=[path_join_dyn] valInputs=[(['path_in', 'path_name'], ['Node(N38)', 'Node(N30)'], ['outFile'], ['path'])] RectF=[(-1543.57, -1664.18, 160.33, 80.0)] 
block=[U13] category=[FileIO.Tools] class=[get_temporary_folder] valInputs=[([], [], ['temp_folder'], ['path'])] RectF=[(-1771.14, -1714.81, 150.0, 80.0)] 
block=[U10] category=[Nipype.Interfaces_dcmstack] class=[dcmstack_SplitNifti] valInputs=[(['in_file', 'out_path', 'split_dim'], ['Node(N1)', 'Node(N29)', 'Node(N37)'], ['out_list'], ['list_path'])] RectF=[(-1055.49, -1087.04, 152.55, 114.9)] 
block=[U12] category=[Tools.Path_list] class=[path_list_getElement] valInputs=[(['list_path_in', 'index'], ['Node(N33)', 'Node(N34)'], ['outPath'], ['path'])] RectF=[(-793.22, -999.28, 171.0, 80.0)] 
block=[U11] category=[Tools.Path_list] class=[path_list_getElement] valInputs=[(['list_path_in', 'index'], ['Node(N28)', 'Node(N35)'], ['outPath'], ['path'])] RectF=[(-753.63, -1545.57, 171.0, 80.0)] 
connt=[C4] name=[treatment_dir] type=[in] format=[path] valOut=[path] RectF=[(-2480.65, 68.27, 70, 24)] 
connt=[C3] name=[ppm] type=[in] format=[float] valOut=[0.0] RectF=[(-2483.5, -384.05, 70, 24)] 
connt=[C2] name=[subject] type=[in] format=[str] valOut=[] RectF=[(-2498.58, -1161.77, 70, 24)] 
connt=[C1] name=[dir_root] type=[in] format=[path] valOut=[path] RectF=[(-2493.83, -1273.8600000000001, 70, 24)] 
connt=[C0] name=[data_list] type=[in] format=[path] valOut=[path] RectF=[(-2498.91, -1370.44, 70, 24)] 
block=[U15] category=[Tools.String] class=[string_concatenat_dyn] valInputs=[(['stringIn', 'stringIn_0'], ['Node(N24)', 'Node(N48)'], ['str_conc'], ['str'])] RectF=[(-1873.15, -675.03, 164.77, 82.0)] 
script=[S1] title=[Script_editor] inputs=[['file_list', 'in', 'path'], ['dir_root', 'in', 'path'], ['subject', 'in', 'str']] outputs=[['cest_path', 'out', 'path'], ['wassr_path', 'out', 'path']] code=[your code] RectF=[(-2178.5, -1423.44, 442.0, 277.0)]
script=[S0] title=[Script_editor] inputs=[['cest_img', 'in', 'array_float'], ['cest_range', 'in', 'array_float'], ['wassr_img', 'in', 'array_float'], ['wassr_range', 'in', 'array_float'], ['ppm', 'in', 'float'], ['correction_B0', 'in', 'str']] outputs=[['map_asym', 'out', 'array_float']] code=[your code] RectF=[(156.86, -1550.93, 599.0, 1268.0)]
block=[U7] category=[FileIO.Json] class=[json_open_file] valInputs=[(['json_file'], ['Node(N12)'], ['dict_json'], ['dict'])] RectF=[(-700.63, -794.75, 159.86, 84.0)] 
block=[U6] category=[Tools.Dictionnary] class=[dict_get_value_dyn] valInputs=[(['input_dict', 'tag', 'tag_0'], ['Node(N13)', 'Node(N15)', 'Node(N14)'], ['out_value', 'out_value_dict'], ['str', 'dict'])] RectF=[(-317.25, -869.6, 233.45000000000002, 138.54)] 
block=[U4] category=[FileIO.Json] class=[json_open_file] valInputs=[(['json_file'], ['Node(N6)'], ['dict_json'], ['dict'])] RectF=[(-634.44, -1322.22, 155.86, 80.0)] 
block=[U0] category=[Images.Nifti] class=[nifti_open_file] valInputs=[(['nifti_file'], ['Node(N31)'], ['image', 'dim', 'pixdim'], ['array_float', 'int', 'list_float'])] RectF=[(-369.38, -1555.17, 150.0, 80.0)] 
block=[U1] category=[Images.Nifti] class=[nifti_open_file] valInputs=[(['nifti_file'], ['Node(N32)'], ['image', 'dim', 'pixdim'], ['array_float', 'int', 'list_float'])] RectF=[(-342.47, -1015.01, 154.0, 84.0)] 
block=[U2] category=[Tools.Path] class=[path_change_extension] valInputs=[(['path_in', 'new_extension'], ['Node(N0)', 'Node(N4)'], ['newPath'], ['path'])] RectF=[(-1028.66, -1318.39, 194.97, 80.0)] 
block=[U3] category=[Tools.Path] class=[path_change_extension] valInputs=[(['path_in', 'new_extension'], ['Node(N3)', 'Node(N5)'], ['newPath'], ['path'])] RectF=[(-1010.7, -791.2, 198.97, 84.0)] 
block=[U5] category=[Tools.Dictionnary] class=[dict_get_value_dyn] valInputs=[(['input_dict', 'tag', 'tag_0'], ['Node(N7)', 'Node(N8)', 'Node(N9)'], ['out_value', 'out_value_dict'], ['str', 'dict'])] RectF=[(-344.17, -1313.47, 229.45000000000002, 134.54)] 
block=[U8] category=[Images.Nifti] class=[nifti_save_file] valInputs=[(['image', 'nifti_path'], ['Node(N19)', 'Node(N60)'], ['pathFile'], ['path'])] RectF=[(1347.21, -1.1, 160.31, 80.0)] 
block=[U14] category=[Tools.Path] class=[path_join_dyn] valInputs=[(['path_in', 'path_name'], ['Node(N26)', 'Node(N49)'], ['outFile'], ['path'])] RectF=[(-1286.3, -31.3, 185.11, 114.89)] 
block=[U18] category=[Tools.Path] class=[path_add_suffixprefix] valInputs=[(['path_in', 'new_str', 'place'], ['Node(N20)', 'Node(N59)', 'suffix'], ['newPath'], ['path'])] RectF=[(144.94, 14.86, 150.0, 80.0)] 
block=[U19] category=[Tools.String] class=[string_concatenat_dyn] valInputs=[(['stringIn', 'stringIn_0', 'stringIn_1'], ['Node(N56)', 'Node(N25)', 'Node(N58)'], ['str_conc'], ['str'])] RectF=[(-839.24, 192.77, 166.77, 84.0)] 
connt=[C5] name=[out_map] type=[out] format=[path] RectF=[(1602.98, 25.25, 70, 24)] 
connt=[C6] name=[slice] type=[in] format=[int] valOut=[0] RectF=[(-2467.31, -897.99, 70, 24)] 
block=[U9] category=[Nipype.Interfaces_dcmstack] class=[dcmstack_SplitNifti] valInputs=[(['in_file', 'out_path', 'split_dim'], ['Node(N2)', 'Node(N39)', 'Node(N36)'], ['out_list'], ['list_path'])] RectF=[(-1184.3, -1602.6000000000001, 170.1, 101.93)] 
[source S0]
["correction_B0='cest_center'", 'wassr_range=U6:out_value', 'cest_range=U5:out_value', 'cest_img=U0:image', 'wassr_img=U1:image', 'ppm=C3:ppm']
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
                map_asym[i, j] = vr.out_mapping()
            except Exception as err:
                print('error :', err)
                map_asym[ i, j] = 0.0
        else:
            map_asym[ i, j] = 0.0
['S0:map_asym']
[/source S0]
[source S1]
['file_list=C0:data_list', 'dir_root=C1:dir_root', 'subject=C2:subject']
from NodeEditor.modules.FileIO.Yml import open_yaml_file
import os

lst_f = open_yaml_file(file_list).dict_yaml()

cest_path = os.path.join(dir_root, lst_f[subject]['path_cest'])
wassr_path = os.path.join(dir_root, lst_f[subject]['path_wassr'])
roi_path = os.path.join(dir_root, lst_f[subject]['roi_zip_path'])




['S1:cest_path', 'S1:wassr_path']
[/source S1]

[execution]
['C0:data_list=', 'C1:dir_root=', 'C2:subject=', 'C6:slice=', 'C3:ppm=', 'C4:treatment_dir=']
['S1', 'U13', 'U15', 'U17', 'U19', 'ThreadOn', 'U20', 'U16', 'U14', 'U3', 'U2', 'ThreadOff', 'ThreadOn', 'U9', 'U10', 'U4', 'U7', 'U18', 'ThreadOff', 'ThreadOn', 'U12', 'U11', 'U6', 'U5', 'ThreadOff', 'ThreadOn', 'U1', 'U0', 'ThreadOff', 'S0', 'U8']
{'U13': ('FileIO.Tools', 'get_temporary_folder', "([], [], ['temp_folder'], ['path'])"), 'U15': ('Tools.String', 'string_concatenat_dyn', "(['stringIn', 'stringIn_0'], ['C2:subject', '.nii'], ['str_conc'], ['str'])"), 'U17': ('FileIO.Tools', 'get_temporary_folder', "([], [], ['temp_folder'], ['path'])"), 'U19': ('Tools.String', 'string_concatenat_dyn', "(['stringIn', 'stringIn_0', 'stringIn_1'], ['_', 'C3:ppm', 'ppm'], ['str_conc'], ['str'])"), 'U20': ('Tools.Path', 'path_join_dyn', "(['path_in', 'path_name'], ['U17:temp_folder', 'wasse_tmp.nii'], ['outFile'], ['path'])"), 'U16': ('Tools.Path', 'path_join_dyn', "(['path_in', 'path_name'], ['U13:temp_folder', 'cest_tmp.nii'], ['outFile'], ['path'])"), 'U14': ('Tools.Path', 'path_join_dyn', "(['path_in', 'path_name'], ['C4:treatment_dir', 'U15:str_conc'], ['outFile'], ['path'])"), 'U3': ('Tools.Path', 'path_change_extension', "(['path_in', 'new_extension'], ['S1:wassr_path', '.json'], ['newPath'], ['path'])"), 'U2': ('Tools.Path', 'path_change_extension', "(['path_in', 'new_extension'], ['S1:cest_path', '.json'], ['newPath'], ['path'])"), 'U9': ('Nipype.Interfaces_dcmstack', 'dcmstack_SplitNifti', "(['in_file', 'out_path', 'split_dim'], ['S1:cest_path', 'U16:outFile', 2], ['out_list'], ['list_path'])"), 'U10': ('Nipype.Interfaces_dcmstack', 'dcmstack_SplitNifti', "(['in_file', 'out_path', 'split_dim'], ['S1:wassr_path', 'U20:outFile', 2], ['out_list'], ['list_path'])"), 'U4': ('FileIO.Json', 'json_open_file', "(['json_file'], ['U2:newPath'], ['dict_json'], ['dict'])"), 'U7': ('FileIO.Json', 'json_open_file', "(['json_file'], ['U3:newPath'], ['dict_json'], ['dict'])"), 'U18': ('Tools.Path', 'path_add_suffixprefix', "(['path_in', 'new_str', 'place'], ['U14:outFile', 'U19:str_conc', 'suffix'], ['newPath'], ['path'])"), 'U12': ('Tools.Path_list', 'path_list_getElement', "(['list_path_in', 'index'], ['U10:out_list', 'C6:slice'], ['outPath'], ['path'])"), 'U11': ('Tools.Path_list', 'path_list_getElement', "(['list_path_in', 'index'], ['U9:out_list', 'C6:slice'], ['outPath'], ['path'])"), 'U6': ('Tools.Dictionnary', 'dict_get_value_dyn', "(['input_dict', 'tag', 'tag_0'], ['U7:dict_json', 'SatTransFreqRanges', 'value'], ['out_value', 'out_value_dict'], ['str', 'dict'])"), 'U5': ('Tools.Dictionnary', 'dict_get_value_dyn', "(['input_dict', 'tag', 'tag_0'], ['U4:dict_json', 'SatTransFreqRanges', 'value'], ['out_value', 'out_value_dict'], ['str', 'dict'])"), 'U1': ('Images.Nifti', 'nifti_open_file', "(['nifti_file'], ['U12:outPath'], ['image', 'dim', 'pixdim'], ['array_float', 'int', 'list_float'])"), 'U0': ('Images.Nifti', 'nifti_open_file', "(['nifti_file'], ['U11:outPath'], ['image', 'dim', 'pixdim'], ['array_float', 'int', 'list_float'])"), 'U8': ('Images.Nifti', 'nifti_save_file', "(['image', 'nifti_path'], ['S0:map_asym', 'U18:newPath'], ['pathFile'], ['path'])")}
['U17:temp_folder', 'U13:temp_folder', 'U10:out_list', 'U12:outPath', 'U11:outPath', 'U9:out_list', 'S1:cest_path', 'S1:wassr_path', 'U15:str_conc', 'S0:map_asym', 'S1:wassr_path', 'S1:cest_path', 'U1:image', 'U0:image', 'U7:dict_json', 'U4:dict_json', 'U2:newPath', 'U3:newPath', 'U5:out_value', 'U6:out_value', 'U19:str_conc', 'U14:outFile', 'U18:newPath', 'U8:pathFile', 'U16:outFile', 'U20:outFile']
{}
['C5:out_map=U8:pathFile']
[interlinks]
[]
