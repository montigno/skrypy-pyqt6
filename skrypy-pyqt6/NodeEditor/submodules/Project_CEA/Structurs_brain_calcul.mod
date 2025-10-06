[diagram]
link=[N7] node=[C6:Atlas_label_text#Node#S0:Atlas_label_text]
link=[N5] node=[C4:mask_nifti#Node#S0:mask_nifti]
link=[N4] node=[C3:Diff_MD#Node#U0:path_in_2]
link=[N3] node=[C2:Diff_FA#Node#U0:path_in_1]
link=[N2] node=[C1:T1_relative#Node#U0:path_in_0]
link=[N1] node=[C0:Bvf#Node#U0:path_in]
link=[N0] node=[U0:ListPath#Node#S0:list_files]
link=[N6] node=[C5:Atlas_nifti#Node#S0:Atlas_nifti]
link=[N8] node=[C7:output_volumes#Node#S0:output_volumes]
connt=[C7] name=[output_volumes] type=[in] format=[path] valOut=[path] RectF=[(-753.84, 369.82, 70, 24)] 
connt=[C6] name=[Atlas_label_text] type=[in] format=[path] valOut=[path] RectF=[(-749.97, 288.64, 70, 24)] 
connt=[C5] name=[Atlas_nifti] type=[in] format=[path] valOut=[path] RectF=[(-748.6800000000001, 216.48000000000002, 70, 24)] 
connt=[C4] name=[mask_nifti] type=[in] format=[path] valOut=[path] RectF=[(-753.83, 152.06, 70, 24)] 
connt=[C3] name=[Diff_MD] type=[in] format=[path] valOut=[path] RectF=[(-754.1, 75.32000000000001, 70, 24)] 
connt=[C2] name=[Diff_FA] type=[in] format=[path] valOut=[path] RectF=[(-752.8100000000001, -0.2, 70, 24)] 
connt=[C1] name=[T1_relative] type=[in] format=[path] valOut=[path] RectF=[(-751.52, -56.39, 70, 24)] 
connt=[C0] name=[Bvf] type=[in] format=[path] valOut=[path] RectF=[(-754.09, -119.02, 70, 24)] 
block=[U0] category=[Tools.Path] class=[path_to_list_dyn] valInputs=[(['path_in', 'path_in_0', 'path_in_1', 'path_in_2'], ['Node(N1)', 'Node(N2)', 'Node(N3)', 'Node(N4)'], ['ListPath'], ['list_path'])] RectF=[(-550.23, -81.18, 163.03, 103.19)] 
script=[S0] title=[Script_python] inputs=[['list_files', 'in', 'list_path'], ['mask_nifti', 'in', 'path'], ['Atlas_nifti', 'in', 'path'], ['Atlas_label_text', 'in', 'path'], ['output_volumes', 'in', 'path']] outputs=[] code=[your code] RectF=[(-184.4, -368.64, 714.0, 1217.0)]
[source S0]
['output_volumes=C7:output_volumes', 'Atlas_nifti=C5:Atlas_nifti', 'list_files=U0:ListPath', 'mask_nifti=C4:mask_nifti', 'Atlas_label_text=C6:Atlas_label_text']
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

base_mas = os.path.basename(Atlas_nifti)
base_mas=('.').join(base_mas.split('.')[:-1])
masks_struct = nib.load(Atlas_nifti).get_fdata()
mask = nib.load(mask_nifti).get_fdata()

hdr =  nib.load(mask_nifti).header
list_dim = (hdr['pixdim']).tolist()
voxel_dim_mask = list_dim[1] * list_dim[2] * list_dim[3]

hdr =  nib.load(Atlas_nifti).header
list_dim = (hdr['pixdim']).tolist()
voxel_dim = list_dim[1] * list_dim[2] * list_dim[3]

list_struct = []
with open(Atlas_label_text) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                list_struct.append(row)
list_struct = list_struct[1:]
# list_struct = list_struct[:65]
# list_struct = list_struct[15:20]
list_idx = {}
for lst_str in list_struct:
    elemts = lst_str[0].split('\t')
    list_idx[int(elemts[0])]= elemts[7]

od = collections.OrderedDict(sorted(list_idx.items()))

with open(output_volumes, 'w') as results:
    results.write('Labels\tSequences\tVol(mm3)\tNech\tMean\tStdv\tMean(eroded)\tStdv(eroded)\n')
    sum_mask = np.sum(mask)
    results.write('Brain' + '\t\t' + str(round(sum_mask*voxel_dim_mask, 2)) + '\t' + str(sum_mask) + '\t\t\t\t\n')
    for k, v in od.items():
        tmp_masks = masks_struct.copy()
        tmp_masks[tmp_masks<k] = 0.0
        tmp_masks[tmp_masks>k] = 0.0
        tmp_masks[tmp_masks==k] = 1.0
        sum_mask = np.sum(tmp_masks)
        tmp_masks_er = erosion(np.array(tmp_masks))
        results.write(v + '\t\t' + str(round(sum_mask*voxel_dim, 2)) + '\t' + str(sum_mask) + '\t\t\t\t\n')
        for seq_k, seq_v in fileSet.items():
            mul = np.multiply(seq_v, tmp_masks)
            mul[mul == 0.0] = 'nan'
            mean = np.nanmean(mul)
            stdv = np.nanstd(mul)
            mul = np.multiply(seq_v, tmp_masks_er)
            mul[mul == 0.0] = 'nan'
            mean_er = np.nanmean(mul)
            stdv_er = np.nanstd(mul)            
            results.write( '\t' + seq_k + '\t\t\t' + str(mean) + '\t' + str(stdv) + '\t' + str(mean_er) + '\t' + str(stdv_er) +'\n')

results.close()


[]
[/source S0]

[execution]
['C0:Bvf=', 'C1:T1_relative=', 'C2:Diff_FA=', 'C3:Diff_MD=', 'C4:mask_nifti=', 'C5:Atlas_nifti=', 'C6:Atlas_label_text=', 'C7:output_volumes=']
['U0', 'S0']
{'U0': ('Tools.Path', 'path_to_list_dyn', "(['path_in', 'path_in_0', 'path_in_1', 'path_in_2'], ['C0:Bvf', 'C1:T1_relative', 'C2:Diff_FA', 'C3:Diff_MD'], ['ListPath'], ['list_path'])")}
['U0:ListPath']
{}
[]
[interlinks]
[]
