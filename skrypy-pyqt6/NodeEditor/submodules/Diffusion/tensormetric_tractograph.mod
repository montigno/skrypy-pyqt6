[diagram]
link=[N1] node=[C1:wmfod_norm#Node#S0:wmfod_norm]
link=[N0] node=[C2:param#Node#S0:param]
link=[N2] node=[C0:mask_den_unr_preproc_unb#Node#S0:mask_den_unr_preproc_unb]
script=[S0] title=[Script_python] inputs=[['mask_den_unr_preproc_unb', 'in', 'path'], ['wmfod_norm', 'in', 'path'], ['param', 'in', 'list_str']] outputs=[] code=[your code] RectF=[(-125.0, -150.0, 919.0, 1104.0)]
connt=[C0] name=[mask_den_unr_preproc_unb] type=[in] format=[path] valOut=[path] RectF=[(-450.0, 115.39, 70, 24)] 
connt=[C1] name=[wmfod_norm] type=[in] format=[path] valOut=[path] RectF=[(-430.79, 385.59000000000003, 70, 24)] 
connt=[C2] name=[param] type=[in] format=[list_str] valOut=[['']] RectF=[(-435.22, 665.39, 70, 24)] 
[source S0]
['mask_den_unr_preproc_unb=C0:mask_den_unr_preproc_unb', 'param=C2:param', 'wmfod_norm=C1:wmfod_norm']
import subprocess 
import math
import os

data_dir = os.path.dirname(mask_den_unr_preproc_unb)

numberOfStreamlineVector = param[0]
cutoffVector = param[1]
stepSizeVector = param[2]
curvature = param[3]
nThreads = param[4]
siftTypeArray = param[5]
siftValueArray = param[6]

for numberOfStreamLines in numberOfStreamlineVector:
    for cutoff in cutoffVector:
        for stepSize in stepSizeVector:
            strCutoff = ('%.4f' % cutoff)
            angle = round(math.degrees(2 * math.asin(stepSize / (2 * curvature))), 4)
            tracks_file_name = 'tracks_' + str(numberOfStreamLines) + '_cutoff-' + strCutoff + '_minl-0.1_maxl-50' + '_step-' + str(
                            stepSize) + '_angle-' + str(angle)
            out_tracks_file = os.path.join(data_dir, tracks_file_name + '.tck')
            result = subprocess.run(
                         ['tckgen', '-seed_random_per_voxel', mask_den_unr_preproc_unb, str(numberOfStreamLines),
                         '-cutoff', strCutoff, wmfod_norm, '-minlength', '0.1', '-maxlength', '50', '-step',
                         str(stepSize), '-angle', str(angle), out_tracks_file, '-nthreads', str(nThreads)], stdout=subprocess.PIPE)
            print(result.stdout.decode('utf-8'))

            firstTimeSiftStandardFlag = 0
            for siftType in siftTypeArray:
                for siftValue in siftValueArray:
                    print('Performing sift...')

                    if ((siftType == 'standard') and (not(firstTimeSiftStandardFlag))):
                        siftTerminus = '_sift-standard'
                        siftTerminus_file_name = tracks_file_name + siftTerminus
                        out_siftTerminus_file = os.path.join(data_dir, siftTerminus_file_name + '.tck')
                        result = subprocess.run(
                                    ['tcksift', out_tracks_file, wmfod_norm, out_siftTerminus_file, '-nthreads', str(nThreads), '-force'], stdout=subprocess.PIPE)
                        print(result.stdout.decode('utf-8'))
                        firstTimeSiftStandardFlag = 1

                    if (siftType=='term_mu'):
                        siftTerminus = '_sift-term-mu-' + str(siftValue)
                        siftTerminus_file_name = tracks_file_name + siftTerminus
                        out_siftTerminus_file = os.path.join(data_dir, siftStandard_file_name + '.tck')
                        result = subprocess.run(
                                        ['tcksift', '-term_mu', str(siftValue),out_tracks_file, wmfod_norm, out_siftTerminus_file, '-nthreads', str(nThreads), 
                                        '-force'], stdout=subprocess.PIPE)
                        print(result.stdout.decode('utf-8'))

                    if (siftType=='term_ratio'):
                        siftTerminus = '_sift-term-ratio-' + str(siftValue)
                        siftTerminus_file_name = tracks_file_name + siftTerminus
                        out_siftTerminus_file = os.path.join(data_dir, siftTerminus_file_name + '.tck')
                        result = subprocess.run(
                                    ['tcksift', '-term_ratio', str(siftValue), out_tracks_file, wmfod_norm, out_siftTerminus_file, '-nthreads', str(nThreads), 
                                    '-force'], stdout=subprocess.PIPE)
                        print(result.stdout.decode('utf-8'))

                    print('Sift done!!!')
[]
[/source S0]

[execution]
['C0:mask_den_unr_preproc_unb=', 'C1:wmfod_norm=', 'C2:param=']
['S0']
{}
[]
{}
[]
[interlinks]
[]
