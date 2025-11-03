class openImageJ():
    def __init__(self, files=['path']):
        from subprocess import Popen
        import os

        if not isinstance(files, list):
            if files == 'path':
                files = ['']
            else:
                files = [files]
        list_files = '|||'.join(files)
        script_macro = "run(\"Brightness/Contrast...\");"
        script_macro1 = "arg=" + "\"" + list_files + "\"" + ";"\
                        "list=split(arg,\"|||\");"\
                        "for (i=0;i<list.length;i++) {"\
                        "open(list[i]);\n"\
                        "getDimensions(width, height, channels, slices, frames);\n"\
                        "if (slices != 1)\n"\
                        "    Stack.setSlice(slices/2);\n"\
                        "else if (frames != 1)\n"\
                        "    Stack.setFrame(frames/2);\n"\
                        "else if (channels != 1)\n"\
                        "    Stack.setChannel(channels/2);\n"\
                        "run(\"Enhance Contrast\", \"saturated=0.35\");"\
                        "};"
        try:
            proc = Popen(['ImageJ', '-eval', script_macro1 + script_macro])
        except:
            proc = Popen([os.environ['ImageJ'], '-eval', script_macro1 + script_macro])

##############################################################################


class openImagej_multiFiles():
    def __init__(self, file=['path']):
        from subprocess import Popen
        import os
        list_files = '|||'.join(file)
        script_macro = "run(\"Brightness/Contrast...\");"
        script_macro1 = "arg=" + "\"" + list_files + "\"" + ";"\
                        "list=split(arg,\"|||\");"\
                        "for (i=0;i<list.length;i++) {"\
                        "open(list[i]);\n"\
                        "run(\"Enhance Contrast\", \"saturated=0.35\");"\
                        "};"
        try:
            proc = Popen(['ImageJ', '-eval', script_macro1 + script_macro])
        except:
            proc = Popen([os.environ['ImageJ'], '-eval', script_macro1 + script_macro])

##############################################################################


class ImageJ_atlas():
    def __init__(self, atlas_template='path', atlas_label='path', label_txt='path'):
        from subprocess import Popen
        import os
        import tempfile
        
        scriptfile = 'open("' + atlas_label + '");\nrun(\"Enhance Contrast\", \"saturated=0.35\");\n'\
                     'open("' + atlas_template + '");\nrun(\"Enhance Contrast\", \"saturated=0.35\");\n'
        script = 'var lines=split(File.openAsString("' + label_txt + '"), "\\n");\n ij.run("Synchronize Windows"); \n'
        filemacro = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'macros', 'Atlas.txt')
        scriptmacro = open(filemacro, 'r').read()
        script += scriptmacro + '\n'
        tmp_folder = tempfile.gettempdir()
        tmp_file = os.path.join(tmp_folder, 'tmp.txt')
        file_tmp = open(tmp_file, "w")
        file_tmp.write(script)
        script = 'run("Synchronize Windows");\n'\
                 'run("Install...", "install=' + tmp_file + '");'
        # Popen(['ImageJ', '-eval', scriptfile, '-eval', script], shell=False)
        try:
            proc = Popen(['ImageJ', '-eval', scriptfile, '-eval', script], shell=False)
        except:
            proc = Popen([os.environ['ImageJ'], '-eval', scriptfile, '-eval', script], shell=False)

##############################################################################


class ImageJ_atlas_reg():
    def __init__(self, file_in='path', atlas_template='path', atlas_label='path', label_txt='path', other_files=['path']):
        from subprocess import Popen
        import os
        import tempfile

        scriptfile = 'open("' + file_in + '");\nrun(\"Enhance Contrast\", \"saturated=0.35\");\n'\
                     'open("' + atlas_label + '");\nrun(\"Enhance Contrast\", \"saturated=0.35\");\n'\
                     'rename("atlas");\n'\
                     'open("' + atlas_template + '");\nrun(\"Enhance Contrast\", \"saturated=0.35\");\n'\
                     'rename("template");'
        if isinstance(other_files, list):
            if other_files[0] != 'path':
                for fs in other_files:
                    scriptfile += 'open("' + fs + '");\nrun(\"Enhance Contrast\", \"saturated=0.35\");\n'
        else:
            if other_files != 'path':
                scriptfile += 'open("' + other_files + '");\nrun(\"Enhance Contrast\", \"saturated=0.35\");\n'
        script = 'var lines=split(File.openAsString("' + label_txt + '"), "\\n");\n ij.run("Synchronize Windows"); \n'
        filemacro = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'macros', 'Atlas.txt')
        scriptmacro = open(filemacro, 'r').read()
        script += scriptmacro + '\n'

        tmp_folder = tempfile.gettempdir()
        tmp_file = os.path.join(tmp_folder, 'tmp.txt')
        file_tmp = open(tmp_file, "w")
        file_tmp.write(script)
        script = 'run("Synchronize Windows");\n'\
                 'run("Install...", "install=' + tmp_file + '");'
        # Popen(['ImageJ', '-eval', scriptfile, '-eval', script], shell=False)
        try:
            proc = Popen(['ImageJ', '-eval', scriptfile, '-eval', script], shell=False)
        except:
            proc = Popen([os.environ['ImageJ'], '-eval', scriptfile, '-eval', script], shell=False)


##############################################################################


class ImageJ_macro():
    def __init__(self, file_macro='path'):
        from subprocess import Popen
        import os
        option = '-macro'
        # Popen(['ImageJ', option, file_macro])
        try:
            proc = Popen(['ImageJ', option, file_macro])
        except:
            proc = Popen([os.environ['ImageJ'], option, file_macro])

##############################################################################


class ImageJ_macrofile():
    def __init__(self, pathImage='path', filemsacro='path'):
        from subprocess import Popen
        import os
        option = '-macro'
#         subprocess.call(['java','-jar',pathImageJ,pathImage,option,filemacro], shell=False)
        try:
            proc = Popen(['ImageJ', pathImage, option, filemacro])
        except:
            proc = Popen([os.environ['ImageJ'], pathImage, option, filemacro])

##############################################################################


class ImageJ_read_roi():
    def __init__(self, roiIJ_file='path'):
        import read_roi

        if roiIJ_file.endswith('.roi'):
            self.list_rois = read_roi.read_roi_file(roiIJ_file)
        elif roiIJ_file.endswith('.zip'):
            self.list_rois = read_roi.read_roi_zip(roiIJ_file)

    def list_Rois(self: 'dict'):
        return self.list_rois

##############################################################################


class ImageJ_get_pixels_in_roi():
    def __init__(self, image_in=[[0.0]], roiIJ_file='path', roi_name=''):
        from NodeEditor.api.get_mask_ij import get_mask
        import read_roi
        import numpy as np

        try:
            nx, ny, ns, nt = image_in.shape
        except Exception as err:
            nx, ny, ns = image_in.shape

        xq, yq = np.mgrid[:nx, :ny]
        coord_img = np.hstack((xq.reshape(-1, 1), yq.reshape(-1, 1)))

        if roiIJ_file.endswith('.roi'):
            rois = read_roi.read_roi_file(roiIJ_file)
        elif roiIJ_file.endswith('.zip'):
            rois = read_roi.read_roi_zip(roiIJ_file)

        self.coord_masks = []
        for key_roi, val_roi in rois.items():
            if key_roi == roi_name:
                ref = get_mask(ny, nx, val_roi, 'red')
                print(ref.mask_coord().tolist())
                for i in range(nx):
                    for j in range(ny):
                        if [i, j] in ref.mask_coord().tolist():
                            self.coord_masks.append(image_in[j, i, :, :])
                self.coord_masks = np.array(self.coord_masks)
                break

    def coord_mask(self: 'array_float'):
        return self.coord_masks

##############################################################################


class ImageJ_get_coord_roi():
    def __init__(self, image_in=[[0.0]], roiIJ_file='path', roi_name=''):
        from NodeEditor.api.get_mask_ij import get_mask
        import read_roi
        import numpy as np

        nx, ny, ns, nt = image_in.shape

        xq, yq = np.mgrid[:nx, :ny]
        coord_img = np.hstack((xq.reshape(-1, 1), yq.reshape(-1, 1)))

        if roiIJ_file.endswith('.roi'):
            rois = read_roi.read_roi_file(roiIJ_file)
        elif roiIJ_file.endswith('.zip'):
            rois = read_roi.read_roi_zip(roiIJ_file)

        for key_roi, val_roi in rois.items():
            if key_roi == roi_name:
                ref = get_mask(ny, nx, val_roi, 'red')
                self.coord_masks = ref.mask_coord()
                break

    def coord_roi(self: 'list_float'):
        return self.coord_masks

##############################################################################


class ImageJ_command():
    def __init__(self, command='', verbose=True):
        from subprocess import Popen
        # subprocess.Popen(['ImageJ', '-eval', command], shell=False)
        try:
            proc = Popen(['ImageJ', '-eval', command], shell=False)
        except:
            proc = Popen([os.environ['ImageJ'], '-eval', command], shell=False)
        
        if verbose:
            print(command)

##############################################################################


class ImageJ_RelaxationTime_profil():

    def __init__(self,
                 image='path',
                 relax_Time='path',
                 Intensity='path',
                 Shift='path',
                 ListTime=[0.0],
                 time_type="enumerate(('EchoTime',\
                                       'RepetitionTime',\
                                       'InversionTime'))"):
        from subprocess import Popen
        import os
        import tempfile

        scriptfile = 'open("' + image + '");run(\"Enhance Contrast\", \"saturated=0.35\");\n'\
                     'open("' + relax_Time + '");run(\"Enhance Contrast\", \"saturated=0.35\");\n'\
                     'open("' + Intensity + '");run(\"Enhance Contrast\", \"saturated=0.35\");\n'
        script = 'var img1="' + os.path.basename(image) + '"; var img2="' + os.path.basename(relax_Time) + '"; var img3="' + os.path.basename(Intensity) + '";'
        if Shift != 'path':
            scriptfile += 'open("' + Shift + '");run(\"Enhance Contrast\", \"saturated=0.35\");\n'
            script += 'var img4="' + os.path.basename(Shift) + '";'
            if time_type == 'EchoTime':
                filemacro = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'macros', 'Macro_Profil_T2_with_shift.txt')
            elif time_type == 'RepetitionTime':
                filemacro = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'macros', 'Macro_Profil_T1_with_shift.txt')
            elif time_type == 'InversionTime':
                filemacro = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'macros', 'Macro_Profil_TInv_with_shift.txt')
        else:
            if time_type == 'EchoTime':
                filemacro = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'macros', 'Macro_Profil_T2.txt')
            elif time_type == 'RepetitionTime':
                filemacro = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'macros', 'Macro_Profil_T1.txt')
            elif time_type == 'InversionTime':
                filemacro = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'macros', 'Macro_Profil_TInv.txt')

        scriptmacro = open(filemacro, 'r').read()
        script += '\nvar Times=newArray(' + str(ListTime).strip('[]') + ');\n' + scriptmacro + '\n'

        tmp_folder = tempfile.gettempdir()
        tmp_file = os.path.join(tmp_folder, 'tmp.txt')
        file_tmp = open(tmp_file, "w")
        file_tmp.write(script)
        script = 'run("Install...", "install=' + tmp_file + '");'
        # Popen(['ImageJ', '-eval', scriptfile, '-eval', script], shell=False)
        try:
            proc = Popen(['ImageJ', '-eval', scriptfile, '-eval', script], shell=False)
        except:
            proc = Popen([os.environ['ImageJ'], '-eval', scriptfile, '-eval', script], shell=False)
