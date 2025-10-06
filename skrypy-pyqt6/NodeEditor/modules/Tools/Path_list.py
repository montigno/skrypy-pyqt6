class path_list_add_element_dyn():
    def __init__(self,
                 list_path_in=['path'],
                 path_in='path',
                 **dynamicsInputs):
        self.newList = list_path_in.copy()
        self.newList.extend(list_path_in)
        self.newList.append(path_in)
        for di in dynamicsInputs:
            self.newList.append(dynamicsInputs[di])

    def newList_path(self: 'list_path'):
        return self.newList

###############################################################################


class path_list_getElement():
    def __init__(self, list_path_in=['path'], index=0):
        self.outPath = list_path_in[index]

    def outPath(self: 'path'):
        return self.outPath

###############################################################################


class path_list_length():
    def __init__(self, list_path_in=['path']):
        self.file_length = len(list_path_in)

    def file_length(self: 'int'):
        return self.file_length

###############################################################################


class path_list_to_array_dyn:
    def __init__(self, list_path_in=['path'], **dynamicsInputs):
        self.pathArray = [list_path_in.copy()]
        for di in dynamicsInputs:
            self.pathArray.append(dynamicsInputs[di])

    def path_list(self: 'array_path'):
        return self.pathArray

###############################################################################


class path_list_to_str:
    def __init__(self, list_path_in=['path']):
        self.pathstr = str(list_path_in.copy())

    def path_str(self: 'str'):
        return self.pathstr

###############################################################################


class path_list_order:
    def __init__(self, list_path_in=['path'], reverse=False):
        self.out_list = sorted(list_path_in, reverse=reverse)

    def list_out(self: 'list_path'):
        return self.out_list

###############################################################################


class path_list_extend_dyn:
    def __init__(self, list_path_in=['path'], **dynamicsInputs):
        self.pathList = list_path_in.copy()
        for di in dynamicsInputs:
            self.pathList.extend(dynamicsInputs[di])

    def path_list(self: 'list_path'):
        return self.pathList

##############################################################################


class path_list_sublist:
    def __init__(self, list_path_in=['path'], indexes=[0, 1]):
        self.pathList = list_path_in.copy()[indexes[0]:indexes[1]]

    def path_list(self: 'list_path'):
        return self.pathList
