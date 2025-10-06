class gz_compress:
    def __init__(self, file_in='path', delete_file=False):
        import gzip
        import shutil
        import os
        self.out_gz = ''
        with open(file_in, 'rb') as f_in:
            with gzip.open(file_in+'.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                self.out_gz = file_in+'.gz'
        if delete_file:
            try:
                os.remove(file_in)
            except OSError as e:
                print("Error : %s : %s" % (input_file, e.strerror))

    def out_file(self: 'path'):
        return self.out_gz

##############################################################################


class gz_decompress():
    def __init__(self, input_gz='path'):
        import gzip
        import shutil
        import os

        dir = os.path.dirname(input_gz)

        tmp = os.path.basename(input_gz)
        lst_fd = tmp.split('.')
        name = ('.').join(lst_fd[:-1])

        self.out_ungzip = os.path.join(dir, name)

        with gzip.open(input_gz, 'rb') as f_in:
            with open(self.out_ungzip, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    def outfile(self: 'path'):
        return self.out_ungzip
