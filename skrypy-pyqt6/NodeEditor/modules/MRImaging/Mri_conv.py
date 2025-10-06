class mri_conv_bruker_to_nifti:
    def __init__(self,
                 Bruker_files=['path'],
                 naming='PatientName/StudyName/CreationDate-SeqNumber-Protocol-SequenceName-AcquisitionTime',
                 path_export='path',
                 bvals_bvecs=False):
        import os
        import sys
        from subprocess import Popen, PIPE

        self.output = []
        if Bruker_files:
            listBruker = ";".join(Bruker_files)
            options_export = "00000"
            if bvals_bvecs:
                options_export = "00013"
            command = 'java -classpath $MRIFilePATH' + \
                      ' BrukerToNifti \"' + listBruker + \
                      '\" ' + path_export + ' ' + naming + \
                      ' [ExportOptions]' + options_export
            print('Bruker : ', command)
            p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            txt, error = p.communicate()
            rc = p.returncode
            txt = txt.decode("utf-8")
            print(txt)
            txt = txt[txt.index("export to ") + 10:]
            for val in txt.split("export to "):
                self.output.append(val[6:val.index("\n")])

    def list_files_exported(self: 'list_path'):
        return self.output

############################################################################################################################


class mri_conv_philips_to_nifti:
    def __init__(self,
                 Philips_files=['path'],
                 naming='PatientName/StudyName/CreationDate-SeqNumber-Protocol-SequenceName-AcquisitionTime',
                 path_export='path',
                 bvals_bvecs=False):
        import os
        import sys
        from subprocess import Popen, PIPE

        self.output = []
        if Philips_files:
            listPhilips = ''
            for ls in Philips_files:
                if '.rec' not in ls.lower():
                    if ls[-1] != '/':
                        ls += '/'
                listPhilips += ls + ";"
            listPhilips = listPhilips[0:-1]
            options_export = "00000"
            if bvals_bvecs:
                options_export = "00013"
            command = 'java -classpath $MRIFilePATH' + \
                      ' PhilipsToNifti \"' + listPhilips + \
                      '\" ' + path_export + ' ' + naming + \
                      ' [ExportOptions]' + options_export
            print('Philips : ', command)
            p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            txt, error = p.communicate()
            rc = p.returncode
            txt = txt.decode("utf-8")
            txt = txt[txt.index("export to ") + 10:]
            for val in txt.split("export to "):
                self.output.append(val[6:val.index("\n")])

    def list_files_exported(self: 'list_path'):
        return self.output

############################################################################################################################


class mri_conv_bids_to_nifti:
    def __init__(self,
                 Bids_dir=['path'],
                 naming='PatientName/StudyName/CreationDate-SeqNumber-Protocol-SequenceName-AcquisitionTime',
                 path_export='path',
                 bvals_bvecs=False):
        import os
        import sys
        from subprocess import Popen, PIPE

        self.output = []
        if Bids_dir:
            listBids = ''
            for ls in Bids_dir:
                listBids += ls + ";"
            listBids = listBids[0:-1]
            options_export = "00000"
            if bvals_bvecs:
                options_export = "00013"
    #         command = 'java -classpath ' + ConfigModuls().getPathConfig('MRIFileManager') + \
            command = 'java -classpath $MRIFilePATH' + \
                      ' BidsToNifti \"' + listBids + \
                      '\" ' + path_export + ' ' + naming + \
                      ' [ExportOptions]' + options_export
            print('BIDS : ', command)
            p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            txt, error = p.communicate()
            rc = p.returncode
            txt = txt.decode("utf-8")
            txt = txt[txt.index("export to ") + 10:]
            for val in txt.split("export to "):
                self.output.append(val[6:val.index("\n")])

    def list_files_exported(self: 'list_path'):
        return self.output

############################################################################################################################


class mri_conv_dicom_to_nifti:
    def __init__(self,
                 Dicom_dir=['path'],
                 naming='PatientName/StudyName/CreationDate-SeqNumber-Protocol-SequenceName-AcquisitionTime',
                 path_export='path',
                 bvals_bvecs=False):
        import os
        import sys
        from subprocess import Popen, PIPE

        self.output = []
        if Dicom_dir:
            listDicom = ''
            for ls in Dicom_dir:
                listDicom += ls + ";"
            listDicom = listDicom[0:-1]
            options_export = "00000"
            if bvals_bvecs:
                options_export = "00013"
    #         command = 'java -classpath ' + ConfigModuls().getPathConfig('MRIFileManager') + \
            command = 'java -classpath $MRIFilePATH' + \
                      ' DicomToNifti \"' + listDicom + \
                      '\" ' + path_export + ' ' + naming + \
                      ' [ExportOptions]' + options_export
            print('Dicom : ', command)
            p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            txt, error = p.communicate()
            rc = p.returncode
            txt = txt.decode("utf-8")
            print(txt)
            txt = txt[txt.index("export to ") + 10:]
            for val in txt.split("export to "):
                self.output.append(val[6:val.index("\n")])

    def list_files_exported(self: 'list_path'):
        return self.output

############################################################################################################################


class mri_conv_GUI:
    def __init__(self, export_path='path', nifti_naming='PatientName/StudyName/Protocol-SerialNumber-SequenceName'):
        import subprocess
        import os
        import pathlib
        from glob import glob

        command = ['java', '-Xms512m', '-Xmx4096m', '-jar', os.environ['MRIFilePATH'], '[ExportNifti] ' + export_path]
        command.append('[ExportToMIA]' + nifti_naming)
        subprocess.call(command)
        list_f = []
        list_f.extend(glob(os.path.join(export_path, '*.json')))
        list_f.sort(key=lambda x: os.path.getmtime(x))
        lastfile = list_f[-1]
        print(lastfile)
        self.outRep = export_path

    def export_path(self: 'path'):
        return self.outRep
