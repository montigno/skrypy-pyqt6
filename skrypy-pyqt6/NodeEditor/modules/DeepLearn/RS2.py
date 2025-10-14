class RS2_predict():
    '''
    Contains the RSS-Net framework for the task of rodent MRI skull stripping

    Note:
        link_web:  https://github.com/VitoLin21/Rodent-Skull-Stripping
                        (click Ctrl + U)
    '''
    def __init__(self, input_folder='path', output_folder='path', pretrained_model_path='path', **options):
        import subprocess

        lso = ["RS2_predict", "-i", input_folder, '-o', output_folder, '-m', pretrained_model_path]
        for ef, ev in options.items():
            if ef in ['save_probabilities', 'continue_prediction', 'verbose']:
                if ev:
                    lso.append('--' + ef)
            else:
                lso.append('-' + ef)
                lso.append(str(ev))
        command = " ".join(lso)
        print(command)
        p = subprocess.run(command, stdout=subprocess.PIPE, shell=True, check=True)
        out_txt = p.stdout.decode("utf8").splitlines()
        self.out_list = []
        for ln_txt in out_txt:
            print(ln_txt)
            if 'done with ' in ln_txt:
                self.out_list.append("{}/{}{}".format(output_folder, ln_txt[10:], "_0000.nii.gz"))
                # self.out_list.append(ln_txt[10:] + "_0000.nii.gz")

    def output_files(self: 'list_path'):
        return self.out_list

##############################################################################


class RS2_predict_datamanagement():
    '''
    Contains the RSS-Net framework for the task of rodent MRI skull stripping.
    With complete data management (compression to nii.gz and add extension _0000)

    Note:
        link_web:  https://github.com/VitoLin21/Rodent-Skull-Stripping
                        (click Ctrl + U)
    '''
    def __init__(self, list_files=['path'], output_folder='path', pretrained_model_path='path', **options):
        import subprocess
        import shutil
        import gzip
        import os

        tmp_folder = os.path.join(output_folder, 'tmp_rss')
        if not os.path.exists(tmp_folder):
            os.makedirs(tmp_folder)

        if not isinstance(list_files, list):
            list_files = [list_files]

        for cur_file in list_files:
            if cur_file.endswith('.nii'):
                if os.path.exists(cur_file):
                    with open(cur_file, 'rb') as f_in:
                        print('Processing in progress for {}'.format(cur_file))
                        tmp = os.path.basename(cur_file)
                        lsfield = tmp.split('.')
                        name = ('.').join(tmp.split('.')[:-1])
                        ext = tmp.split('.')[-1]
                        new_name_file = os.path.join(tmp_folder, name + '_0000.nii')
                        with gzip.open(new_name_file + '.gz', 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)

        lso = ["RS2_predict", "-i", tmp_folder, '-o', output_folder, '-m', pretrained_model_path]
        for ef, ev in options.items():
            if ef in ['save_probabilities', 'continue_prediction', 'verbose']:
                if ev:
                    lso.append('--' + ef)
            else:
                lso.append('-' + ef)
                lso.append(str(ev))
        command = " ".join(lso)
        print(command)
        p = subprocess.run(command, stdout=subprocess.PIPE, shell=True, check=True)
        out_txt = p.stdout.decode("utf8").splitlines()
        self.out_list = []
        for ln_txt in out_txt:
            print(ln_txt)
            if 'done with ' in ln_txt:
                self.out_list.append("{}/{}{}".format(output_folder, ln_txt[10:], "_0000.nii.gz"))
                # self.out_list.append(ln_txt[10:] + "_0000.nii.gz")
        shutil.rmtree(tmp_folder)

    def output_files(self: 'list_path'):
        return self.out_list
