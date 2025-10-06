class path_array_getElement():
    def __init__(self, array_path_in=[['path']], index_row=0, index_col=0):
        self.outPath = array_path_in[index_row][index_col]

    def outPath(self: 'path'):
        return self.outPath

###############################################################################


class path_array_flatten():
    def __init__(self, array_path_in=[['path']]):
        self.rt = self.__flatten(array_path_in)

    def __flatten(self, A):
        rt = []
        for i in A:
            if isinstance(i, list):
                rt.extend(self.__flatten(i))
            else:
                rt.append(i)
        return rt

    def flatten_out(self: 'list_path'):
        return self.rt
