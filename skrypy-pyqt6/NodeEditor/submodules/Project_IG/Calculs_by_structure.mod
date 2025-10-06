[diagram]
link=[N5] node=[C4:Atlas_label_text#Node#S0:Atlas_label_text]
link=[N2] node=[C2:Diff_MD_nifti#Node#U0:path_in_1]
link=[N1] node=[C1:Diff_FA_nifti#Node#U0:path_in_0]
link=[N0] node=[C0:T1_Flash_nifti#Node#U0:path_in]
link=[N3] node=[U0:ListPath#Node#S0:list_files]
link=[N4] node=[C5:output_result#Node#S0:output_result]
link=[N6] node=[C3:Atlas_label_nifti#Node#S0:Atlas_label_nifti]
script=[S0] title=[Script_editor] inputs=[['list_files', 'in', 'list_path'], ['Atlas_label_nifti', 'in', 'path'], ['Atlas_label_text', 'in', 'path'], ['output_result', 'in', 'path']] outputs=[] code=[your code] RectF=[(175.0, -325.0, 626.0, 1193.0)]
connt=[C2] name=[Diff_MD_nifti] type=[in] format=[path] valOut=[path] RectF=[(-475.0, 0.0, 70, 24)] 
connt=[C1] name=[Diff_FA_nifti] type=[in] format=[path] valOut=[path] RectF=[(-475.0, -100.0, 70, 24)] 
connt=[C0] name=[T1_Flash_nifti] type=[in] format=[path] valOut=[path] RectF=[(-475.0, -200.0, 70, 24)] 
block=[U0] category=[Tools.Path] class=[path_to_list_dyn] valInputs=[(['path_in', 'path_in_0', 'path_in_1'], ['Node(N0)', 'Node(N1)', 'Node(N2)'], ['ListPath'], ['list_path'])] RectF=[(-275.0, -175.0, 175.0, 150.0)] 
connt=[C3] name=[Atlas_label_nifti] type=[in] format=[path] valOut=[path] RectF=[(-200.0, 125.0, 70, 24)] 
connt=[C4] name=[Atlas_label_text] type=[in] format=[path] valOut=[path] RectF=[(-200.0, 375.0, 70, 24)] 
connt=[C5] name=[output_result] type=[in] format=[path] valOut=[path] RectF=[(-200.0, 625.0, 70, 24)] 
[source S0]
['Atlas_label_nifti=C3:Atlas_label_nifti', 'output_result=C5:output_result', 'list_files=U0:ListPath', 'Atlas_label_text=C4:Atlas_label_text']
import numpy as np
import nibabel as nib
import os
import pathlib
import csv
import collections
from skimage.morphology import erosion

print(list_files)

fileSet = {}
for seq in list_files:
    base_seq = os.path.basename(seq)
    base_seq=('.').join(base_seq.split('.')[:-1])
    fileSet[base_seq] = nib.load(seq).get_fdata()

base_mas = os.path.basename(Atlas_label_nifti)
base_mas=('.').join(base_mas.split('.')[:-1])
masks_struct = nib.load(Atlas_label_nifti).get_fdata()

hdr =  nib.load(Atlas_label_nifti).header
list_dim = (hdr['pixdim']).tolist()
voxel_dim = list_dim[1] * list_dim[2] * list_dim[3]

list_struct = []
with open(Atlas_label_text) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                list_struct.append(row)
list_struct = list_struct[15:249]
# list_struct = list_struct[15:20]
list_idx = {}
for lst_str in list_struct:
    elemts = lst_str[0].split('\t')
    list_idx[int(elemts[0])]= elemts[7][1:-1]

od = collections.OrderedDict(sorted(list_idx.items()))

with open(output_result, 'w') as results:
    results.write('Labels|Sequences|Vol(mm3)|Mean|Stdv\n')
    for k, v in od.items():
        tmp_masks = masks_struct.copy()
        tmp_masks[tmp_masks<k] = 0.0
        tmp_masks[tmp_masks>k] = 0.0
        tmp_masks[tmp_masks==k] = 1.0
        sum_mask = np.sum(tmp_masks)
        results.write(v + '||' + str(round(sum_mask*voxel_dim, 2)) + '||\n')
        for seq_k, seq_v in fileSet.items():
            mul = np.multiply(seq_v, tmp_masks)
            mul[mul == 0.0] = 'nan'
            mean = np.nanmean(mul)
            stdv = np.nanstd(mul)
            results.write( '|' + seq_k + '|''|' + str(mean) + '|' + str(stdv) + '\n')

        tmp_masks = erosion(np.array(tmp_masks))
        sum_mask = np.sum(tmp_masks)
        results.write(v+ '_eroded' + '||' + str(round(sum_mask*voxel_dim, 2)) + '||\n')
        for seq_k, seq_v in fileSet.items():
            mul = np.multiply(seq_v, tmp_masks)
            mul[mul == 0.0] = 'nan'
            mean = np.nanmean(mul)
            stdv = np.nanstd(mul)
            results.write( '|' + seq_k + '|''|' + str(mean) + '|' + str(stdv) + '\n')
results.close()


[]
[/source S0]

[execution]
['C0:T1_Flash_nifti=', 'C1:Diff_FA_nifti=', 'C2:Diff_MD_nifti=', 'C3:Atlas_label_nifti=', 'C4:Atlas_label_text=', 'C5:output_result=']
['U0', 'S0']
{'U0': ('Tools.Path', 'path_to_list_dyn', "(['path_in', 'path_in_0', 'path_in_1'], ['C0:T1_Flash_nifti', 'C1:Diff_FA_nifti', 'C2:Diff_MD_nifti'], ['ListPath'], ['list_path'])")}
['U0:ListPath']
{}
[]
[interlinks]
[]
