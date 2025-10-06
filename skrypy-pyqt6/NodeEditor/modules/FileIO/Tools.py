class box_dialog_file:
    """
    Open a dialog box from which the user can select a file.

    Args:
        fileDefault: (path) default file
        extension: (string) file name filtering (ex '*.jpg' '*.txt' '.nii .json ')
        title: (string) dialog box title

    Returns:
        filePath: (path) path of the selected file

    Note:
        GUI: yes
    """
    def __init__(self, fileDefault='path',
                 extension='*', title='Select a file'):
        import os.path
        from PyQt6.QtWidgets import QFileDialog, QApplication

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        self.fileChosen = ''
        dirdefault = ''
        if os.path.exists(fileDefault):
            dirdefault = os.path.dirname(fileDefault)
        fileCh = QFileDialog.getOpenFileName(
                            None,
                            title,
                            dirdefault,
                            extension,
                            None,
                            QFileDialog.Option.DontUseNativeDialog)
        if fileCh[0]:
            self.fileChosen = fileCh[0]

    def filePath(self: 'path'):
        return self.fileChosen

##############################################################################


class compare_two_files:
    """
    """
    def __init__(self, file1='path', file2='path'):
        from subprocess import Popen, PIPE

        p = Popen(['diff', '--normal', file1, file2], stdout=PIPE)
        self.output, err = p.communicate()

    def compare_out(self: 'str'):
        return self.output

##############################################################################


class box_dialog_files:
    """
    Open a dialog box from which the user can select multiple files.

    Args:
        fileDefault: (path) default file
        extension: (string) file name filtering (ex '*.jpg' '*.txt' '.nii .json ')
        title: (string) dialog box title

    Returns:
        filesPath: (list of file paths) path of the selected file
        numberOfFiles: (int) number of selected files

    Note:
        GUI: yes
    """
    def __init__(self, filesDefault='path',
                 extension='*', title='Open files'):
        import os.path
        from PyQt6.QtWidgets import QFileDialog, QApplication

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        self.filesSource = []
        filesExists = False
        # for lf in filesDefault:
        #     if os.path.exists(lf):
        #         filesExists = True
        #     else:
        #         filesExists = False
        #         break
        dirdefault = ''
        if os.path.exists(filesDefault):
            dirdefault = os.path.dirname(filesDefault)
        filesCh = QFileDialog.getOpenFileNames(
                            None,
                            title,
                            dirdefault,
                            extension,
                            None,
                            QFileDialog.Option.DontUseNativeDialog)
        if filesCh[0]:
            self.filesSource = filesCh[0]
        self.nb = len(self.filesSource)

    def filesPath(self: 'list_path'):
        return self.filesSource

    def numberOfFiles(self: 'int'):
        return self.nb

##############################################################################


class box_dialog_directory:
    """
    Open a dialog box from which the user can select a directory.

    Args:
        RepDefault: (path) default directory
        title: (string) dialog box title

    Returns:
        filePath: (path) path of the selected directory

    Note:
        GUI: yes
    """
    def __init__(self, RepDefault='path', title='Select a directory'):
        import os.path
        from PyQt6.QtWidgets import QFileDialog, QApplication

        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        dirdefault = ''
        if os.path.exists(RepDefault):
            dirdefault = os.path.dirname(RepDefault)
        self.repChosen = QFileDialog.getExistingDirectory(None, title, dirdefault)

    def filePath(self: 'path'):
        return self.repChosen

##############################################################################


class copy_file():
    """
    copy the content of source file to destination file or directory.

    Args:
        src_file: (path) source file
        dest_file: (path) destination file or directory

    Returns:
        copied_file: (path) path of the copied file or directory

    Note:
        GUI: no
    """

    def __init__(self, src_file='path', dest_file='path'):
        from shutil import copy2
        if dest_file != src_file:
            self.cf = copy2(src_file, dest_file)

    def copied_file(self: 'path'):
        return self.cf

##############################################################################


class create_directory:
    def __init__(self, dir_in='path'):
        import os
        self.dir_out = ''
        if not os.path.exists(dir_in):
            os.makedirs(dir_in)
        self.dir_out = dir_in

    def out_dir(self: 'path'):
        return self.dir_out

##############################################################################


class create_directory_recursive:
    def __init__(self, dir_in='path'):
        import os
        self.dir_out = ''
        path = dir_in
        if not os.path.exists(dir_in):
            os.makedirs(path)
        else:
            counter = 1
            path = dir_in
            while os.path.exists(path):
                path = '{}_{}'.format(dir_in, counter)
                counter += 1
            os.makedirs(path)
        self.dir_out = path

    def out_dir(self: 'path'):
        return self.dir_out

##############################################################################


class delete_file:

    def __init__(self, input_file='path'):
        import os
        try:
            os.remove(input_file)
        except OSError as e:
            print("Error : %s : %s" % (input_file, e.strerror))

##############################################################################


class delete_files:

    def __init__(self, input_files=['path']):
        import os
        for lst_f in input_files:
            try:
                os.remove(lst_f)
            except OSError as e:
                print("Error : %s : %s" % (lst_f, e.strerror))

##############################################################################


class delete_files_model:

    def __init__(self, input_dir='path', model='*.txt'):
        import os
        import glob

        files = glob.glob(os.path.join(input_dir, model))

        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print('Error : %s : %s' % (f, e.strerror))

##############################################################################


class delete_folder:

    def __init__(self, input_folder='path', ignore_errors=False):
        import shutil
        shutil.rmtree(input_folder, ignore_errors=ignore_errors)

##############################################################################


class filter_directory_files_pattern:

    def __init__(self,
                 directory='path',
                 operator='enumerate(("==",\
                                      "!=",\
                                      "contains",\
                                      "not contains",\
                                      "in",\
                                      "not in"))',
                 pattern=''):
        import os
        self.outfiles = []
        for file in os.listdir(directory):
            if operator == '==':
                if file == pattern:
                    self.outfiles.append(os.path.join(directory, file))
            elif operator == '!=':
                if file != pattern:
                    self.outfiles.append(os.path.join(directory, file))
            elif operator == 'contains':
                if pattern in file:
                    self.outfiles.append(os.path.join(directory, file))
            elif operator == 'not contains':
                if pattern not in file:
                    self.outfiles.append(os.path.join(directory, file))
            elif operator == 'in':
                if file in pattern.strip():
                    self.outfiles.append(os.path.join(directory, file))
            elif operator == 'not in':
                if file not in pattern.strip():
                    self.outfiles.append(os.path.join(directory, file))

    def output_filtered_files(self: 'list_path'):
        return self.outfiles

##############################################################################


class filter_input_files_pattern:

    def __init__(self,
                 input_files=['path'],
                 operator='enumerate(("==",\
                                      "!=","contains",\
                                      "not contains",\
                                      "in",\
                                      "not in"))',
                 pattern=''):
        import os
        self.outfiles = []
        for filePath in input_files:
            file = os.path.basename(filePath)
            if operator == '==':
                if file == pattern:
                    self.outfiles.append(filePath)
            elif operator == '!=':
                if file != pattern:
                    self.outfiles.append(filePath)
            elif operator == 'contains':
                if pattern in file:
                    self.outfiles.append(filePath)
            elif operator == 'not contains':
                if pattern not in file:
                    self.outfiles.append(filePath)
            elif operator == 'in':
                if file in pattern.strip():
                    self.outfiles.append(filePath)
            elif operator == 'not in':
                if file not in pattern.strip():
                    self.outfiles.append(filePath)

    def output_filtered_files(self: 'list_path'):
        return self.outfiles

##############################################################################


class filter_files_extension:

    def __init__(self, input_files=['path'], extension='.nii .json'):
        self.outfiles = []
        for filePath in input_files:
            if filePath.endswith(tuple(extension.split(' '))):
                self.outfiles.append(filePath)

    def output_filtered_files(self: 'list_path'):
        return self.outfiles

##############################################################################


class filter_directory_files_extension:

    def __init__(self, directory='path', extension='.nii .json'):
        import os
        self.outfiles = []
        for filePath in os.listdir(directory):
            if filePath.endswith(tuple(extension.split(' '))):
                self.outfiles.append(filePath)

    def output_filtered_files(self: 'list_path'):
        return self.outfiles

##############################################################################


class list_files_in_directory:
    """
    Get a list of subdirectories in a directory

    Args:
        RepDefault: (path) the root directory path

    Retuns:
        listFiles: (list of file paths) file paths in the selected directory

    Note:
        GUI: no
    """
    def __init__(self, RepDefault='path', filter="*", recursive=False):
        import os
        import glob
        self.lstfiles = []
        if RepDefault:
            if os.path.isdir(RepDefault):
                if recursive:
                    self.lstfiles = [f for f in glob.glob(os.path.join(RepDefault, "**", filter), recursive=True) if os.path.isfile(f)]
                else:
                    self.lstfiles = [f for f in glob.glob(os.path.join(RepDefault, filter)) if os.path.isfile(f)]

    def listFiles(self: 'list_path'):
        return self.lstfiles

##############################################################################


class list_directories_in_directory:
    def __init__(self, RepDefault='path'):
        import os
        import glob
        self.lstdir = []
        if RepDefault:
            if os.path.isdir(RepDefault):
                self.lstdir = [f for f in glob.glob(RepDefault + "/*") if os.path.isdir(f)]

    def listDirectories(self: 'list_path'):
        return self.lstdir

##############################################################################


class move_files:
    def __init__(self, files_input=['path'], move_to_dir='path'):
        import shutil
        import os
        self.listfiles_moved = []
        if not os.path.exists(move_to_dir):
            os.makedirs(move_to_dir)
        for lst in files_input:
            if os.path.isfile(lst):
                name_f = os.path.split(lst)[-1]
                tmp = os.path.join(move_to_dir, name_f)
                shutil.move(lst, tmp)
                self.listfiles_moved.append(tmp)

    def outfiles_moved(self: 'list_path'):
        return self.listfiles_moved

##############################################################################


class numberOfFiles():
    def __init__(self, list_files=['path']):
        self.nb = len(list_files)

    def number_files(self: 'int'):
        return self.nb

##############################################################################


class rename_file:
    def __init__(self, file_origin='path', file_new_name=''):
        import shutil
        import os
        dir = os.path.dirname(file_origin)
        self.outfile_new = os.path.join(dir, file_new_name)
        shutil.move(file_origin, self.outfile_new)

    def output_file(self: 'path'):
        return self.outfile_new

##############################################################################


class rename_file_options:
    """
    Rename the file by adding a suffix and/or a prefix.

    Args:
        file_origin: (path) original file

    Returns:
        output_file: (path) new file name

    Note:
        GUI: no
    """
    def __init__(self, file_origin='path', **options):
        import shutil
        import os
        dir = os.path.dirname(file_origin)
        tmp = os.path.basename(file_origin)
        name = ('.').join(tmp.split('.')[:-1])
        ext = tmp.split('.')[-1]
        if 'extension_number' in options:
            if options['extension_number'] == 2:
                lsfield = tmp.split('.')
                name = ('.').join(lsfield[:-2])
                ext = lsfield[-2] + '.' + lsfield[-1]
        if 'add_suffix' in options:
            new_str = options['add_suffix']
            self.outfile_new = os.path.join(dir, name + new_str + '.'+ext)
        if 'add_prefix' in options:
            new_str = options['add_prefix']
            self.outfile_new = os.path.join(dir, new_str + name + '.'+ext)
        shutil.move(file_origin, self.outfile_new)

    def output_file(self: 'path'):
        return self.outfile_new

##############################################################################


class search_files:
    def __init__(self, directory_path='path', file_to_find='', recursive=False):
        from glob import glob
        import os

        self.list_f = []

        if recursive:
            for dir, _, _ in os.walk(directory_path):
                self.list_f.extend(glob(os.path.join(dir, file_to_find)))
        else:
            self.list_f.extend(glob(os.path.join(directory_path, file_to_find)))

    def list_files(self: 'list_path'):
        return self.list_f

##############################################################################


class get_file_most_recently:
    def __init__(self, files_list=['path']):
        import os
        import glob

        files_list.sort(key=lambda x: os.path.getmtime(x))
        self.lastfile = files_list[-1]

    def lastfile(self: 'path'):
        return self.lastfile

##############################################################################


class search_files_pattern:
    def __init__(self, list_files=['path'], pattern=''):
        import re

        self.list_f = []

        for file in list_files:
            if pattern in file:
                self.list_f.append(file)

    def list_files(self: 'list_path'):
        return self.list_f

##############################################################################


class search_files_patterns_dyn:
    def __init__(self, list_files=['path'], compare_type="enumerate(('OR', 'AND'))", pattern='', **dynamicsInputs):
        import re
        import os

        self.list_f = []
        list_pattern = [pattern]
        list_pattern.extend(dynamicsInputs.values())
        reg_lst = []
        for raw_regex in list_pattern:
            reg_lst.append(re.compile('.*{}'.format(raw_regex)))

        if compare_type == 'OR':
            for file in list_files:
                print(os.path.basename(file))
                if any(re.match(compiled_reg, os.path.basename(file)) for compiled_reg in reg_lst):
                    self.list_f.append(file)
        else:
            for file in list_files:
                if all(re.match(compiled_reg, os.path.basename(file)) for compiled_reg in reg_lst):
                    self.list_f.append(file)

    def list_files(self: 'list_path'):
        return self.list_f

##############################################################################


class wait_file_exists():
    def __init__(self, file_in='path', **options):
        import os.path
        import time

        timeout_start = time.time()
        self.out = 'not file'
        if 'timeout' in options:
            while (not os.path.exists(file_in) and
                   time.time() < timeout_start + options['timeout']):
                time.sleep(1)
        else:
            while not os.path.exists(file_in):
                time.sleep(1)

        if os.path.isfile(file_in):
            self.out = file_in
        else:
            raise ValueError("%s isn't a file!" % file_in)

    def out_file(self: 'path'):
        return self.out
