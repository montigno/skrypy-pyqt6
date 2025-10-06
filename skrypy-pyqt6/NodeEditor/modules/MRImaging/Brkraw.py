class brkraw_tonii():
    """
    Convert raw data from Bruker to Nifti format

    Args:
        raw_data: (path) root directory

    Returns:
        out_files: (path) list of files converted

    Note:
        GUI: no
        dependencies: brkraw
        link_web:  https://brkraw.github.io/
                    (click Ctrl + U)
    """
    def __init__(self, raw_data='path', **options):
        import subprocess
        import os
        lso = ["brkraw tonii"]
        for ef, ev in options.items():
            lso.append(ef)
            lso.append(ev)
        lso.append(raw_data)
        command = " ".join(lso)
        print(command)
        p = subprocess.run(command, stdout=subprocess.PIPE, shell=True, check=True)
        out_txt = p.stdout.decode("utf8").splitlines()
        self.out_list = []
        for ln_txt in out_txt:
            print(ln_txt)
            if 'NifTi file is generated' in ln_txt:
                self.out_list.append(ln_txt[ln_txt.find("[")+1:ln_txt.find("]")] + ".nii.gz")

    def out_files(self: 'list_path'):
        return self.out_list
