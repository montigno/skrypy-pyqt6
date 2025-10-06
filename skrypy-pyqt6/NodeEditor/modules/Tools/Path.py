class path_root():
    def __init__(self, path_in='path'):
        import os
        self.dir = os.path.dirname(os.path.abspath(path_in))

    def root_dir(self: 'path'):
        return self.dir

###############################################################################


class path_exists():
    def __init__(self, path_in='path'):
        import os
        self.file_exists = False
        if path_in != 'path':
            self.file_exists = os.path.exists(path_in)

    def file_exists(self: 'bool'):
        return self.file_exists

###############################################################################


class path_get_fileName():
    def __init__(self, path_in='path'):
        import os

        self.filename = None
        try:
            self.filename = os.path.basename(path_in)
        except Exception as err:
            print("error with path:", err)

    def file_name(self: 'str'):
        return self.filename

###############################################################################


class path_separate():
    def __init__(self, path_in="path"):
        import os
        self.dir = os.path.dirname(path_in)
        tmp = os.path.basename(path_in)
        lst_fd = tmp.split('.')
        self.name = ('.').join(lst_fd[:-1])
        self.ext = lst_fd[-1]

    def directory(self: 'path'):
        return self.dir

    def nameFile(self: 'str'):
        return self.name

    def extension(self: 'str'):
        return self.ext

###############################################################################


class path_separate_2ext():
    def __init__(self, path_in="path"):
        import os
        self.dir = os.path.dirname(path_in)
        tmp = os.path.basename(path_in)
        lst_fd = tmp.split('.')
        self.name = ('.').join(lst_fd[:-2])
        self.ext = ('.').join(lst_fd[-2:])

    def directory(self: 'path'):
        return self.dir

    def nameFile(self: 'str'):
        return self.name

    def extension(self: 'str'):
        return self.ext

###############################################################################


class path_join_dyn():
    def __init__(self, path_in='path', path_name='', **dynamicsInputs):
        import os
        self.outputFile = os.path.join(path_in, str(path_name))
        for di in dynamicsInputs:
            self.outputFile = os.path.join(self.outputFile, str(dynamicsInputs[di]))

    def outFile(self: 'path'):
        return self.outputFile

###############################################################################


class path_to_list_dyn():
    def __init__(self, path_in='path', **dynamicsInputs):
        self.outListPath = [path_in]
        for di in dynamicsInputs:
            self.outListPath.append(dynamicsInputs[di])

    def ListPath(self: 'list_path'):
        return self.outListPath

###############################################################################


class path_rstrip:
    def __init__(self, path_in='path', chr=''):
        self.outPath = path_in.rstrip(chr)

    def newPath(self: 'path'):
        return self.outPath

###############################################################################


class path_change_extension:
    def __init__(self, path_in='path', new_extension='.txt'):
        import os
        pre, ext = os.path.splitext(path_in)
        self.outPath = os.path.join(pre + new_extension)

    def newPath(self: 'path'):
        return self.outPath

###############################################################################


class path_change_extension_2ext:
    def __init__(self, path_in='path', new_extension='.txt'):
        import os
        pre, ext1 = os.path.splitext(path_in)
        pre, ext2 = os.path.splitext(pre)
        self.outPath = os.path.join(pre + new_extension)

    def newPath(self: 'path'):
        return self.outPath

###############################################################################


class path_add_suffixprefix:
    def __init__(self,
                 path_in='path',
                 new_str='',
                 place="enumerate(('suffix','prefix'))"):
        import os
        dir = os.path.dirname(path_in)
        tmp = os.path.basename(path_in)
        name = ('.').join(tmp.split('.')[:-1])
        ext = tmp.split('.')[-1]
        if place == 'suffix':
            self.outPath = os.path.join(dir, name + new_str + '.'+ext)
        elif place == 'prefix':
            self.outPath = os.path.join(dir, new_str + name + '.'+ext)

    def newPath(self: 'path'):
        return self.outPath

###############################################################################


class path_add_suffixprefix_2ext:
    def __init__(self,
                 path_in='path',
                 new_str='',
                 place="enumerate(('suffix','prefix'))"):
        import os
        dir = os.path.dirname(path_in)
        tmp = os.path.basename(path_in)
        lsfield = tmp.split('.')
        name = ('.').join(lsfield[:-2])
        ext = lsfield[-2] + '.' + lsfield[-1]
        if place == 'suffix':
            self.outPath = os.path.join(dir, name + new_str + '.'+ext)
        elif place == 'prefix':
            self.outPath = os.path.join(dir, new_str + name + '.'+ext)

    def newPath(self: 'path'):
        return self.outPath

###############################################################################


class path_change_name:
    def __init__(self, path_in='path', new_name='myname.txt'):
        import os
        dir = os.path.dirname(path_in)
        self.newPath = os.path.join(dir, new_name)

    def out_new_file(self: 'path'):
        return self.newPath

###############################################################################


class path_last_path:
    def __init__(self, path_in='path'):
        import os
        self.last_path = os.path.basename(os.path.normpath(path_in))

    def last_dir(self: 'path'):
        return self.last_path
