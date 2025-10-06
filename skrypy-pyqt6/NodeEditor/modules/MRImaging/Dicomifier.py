class dicomifier_bruker_to_nifti:
    def __init__(self, rep_data_bruker='path', rep_out='path'):
        import subprocess
        import os
        listRep1 = os.listdir(rep_out)
        lso = ("dicomifier to-nifti", rep_data_bruker, rep_out)
        command = " ".join(lso)
        print(command)
        subprocess.run(command, shell=True, check=True)
        listRep2 = os.listdir(rep_out)
        tmp = [item for item in listRep2 if item not in listRep1]
        try:
            self.output_directory = os.path.join(rep_out, tmp[0])
        except Exception as e:
            self.output_directory = ''

    def out_directory(self: 'path'):
        return self.output_directory

##############################################################################


class dicomifier_dicom_to_nifti():

    def __init__(self, rep_data_dicom='path', rep_out='path'):
        import subprocess
        import os
        # listRep1 = os.listdir(rep_out)
        lso = ("dicomifier to-nifti", rep_data_dicom, rep_out)
        command = " ".join(lso)
        subprocess.run(command, shell=True, check=True)
        # listRep2 = os.listdir(rep_out)
        # tmp = [item for item in listRep2 if item not in listRep1]
        try:
            self.output_directory = os.path.join(rep_out, os.listdir(rep_out)[0])
        except Exception as e:
            self.output_directory = ''

    def out_directory(self: 'path'):
        return self.output_directory

##############################################################################


class dicomifier_bruker_to_dicom():

    def __init__(self, rep_data_bruker='path', rep_out='path'):
        import subprocess
        import os
        listRep1 = os.listdir(rep_out)
        lso = ("dicomifier to-dicom", rep_data_bruker, rep_out)
        command = " ".join(lso)
        subprocess.run(command, shell=True, check=True)
        listRep2 = os.listdir(rep_out)
        tmp = [item for item in listRep2 if item not in listRep1]
        try:
            self.output_directory = os.path.join(rep_out, tmp[0])
        except Exception as e:
            self.output_directory = ''

    def out_directory(self: 'path'):
        return self.output_directory

##############################################################################


class dicomifier_diffusion_scheme_fsl():
    def __init__(self, source_img='path', source_json='path', out_bvecs='path', out_bvals='path', **options):
        import subprocess
        import os
        list_op = []
        for ef in options:
            list_op.append(ef)
            list_op.append(options[ef])
        list_op = tuple(list_op)
        lso = ("dicomifier diffusion-scheme", "--image", source_img, source_json, 'fsl', out_bvecs, out_bvals) + list_op
        command = " ".join(lso)
        subprocess.run(command, shell=True, check=True)
        self.output_files = [out_bvecs, out_bvals]

    def out_files(self: 'list_path'):
        return self.output_files

##############################################################################


class dicomifier_diffusion_scheme_mrtrix():
    def __init__(self, source_json='path', destination='path', **options):
        import subprocess
        import os
        list_op = []
        for ef in options:
            list_op.append(ef)
            list_op.append(options[ef])
        list_op = tuple(list_op)
        lso = ("dicomifier diffusion-scheme", source_json, 'mrtrix', destination) + list_op
        command = " ".join(lso)
        subprocess.run(command, shell=True, check=True)
        self.output_file = destination

    def out_file(self: 'path'):
        return self.output_file
