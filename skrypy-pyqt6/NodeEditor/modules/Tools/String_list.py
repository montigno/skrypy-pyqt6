class string_list_to_array_dyn:
    def __init__(self, string_list_in=[''], **dynamicsInputs):
        self.stringArray = [string_list_in]
        for di in dynamicsInputs:
            self.stringArray.append(dynamicsInputs[di])

    def str_array(self: 'array_str'):
        return self.stringArray

##############################################################################


class string_list_to_float_list():
    def __init__(self, listStr=['']):
        import numpy as np
        listStr = np.array(listStr)
        self.outlistfloat = list(listStr.astype(float))

    def outArrayFloat(self: 'list_float'):
        return self.outlistfloat

##############################################################################


class string_list_to_int_list():
    def __init__(self, ListString=['']):
        from NodeEditor.api.defineTypeVariable import DefineTypeVariable
        typ, val = DefineTypeVariable(ListString).returntype()
        if typ == 'liststr':
            self.outval = []
            for el in ListString:
                self.outval.append(int(el))
        else:
            self.outval = None

    def outPath(self: 'list_int'):
        return self.outval

##############################################################################


class string_list_to_tuple():
    def __init__(self, ListString=['']):
        from NodeEditor.api.defineTypeVariable import DefineTypeVariable
        typ, val = DefineTypeVariable(ListString).returntype()
        if typ == 'liststr':
            self.outval = tuple(ListString)
        else:
            self.outval = None

    def outTuple(self: 'tuple'):
        return self.outval

##############################################################################


class string_list_add_element_dyn:
    def __init__(self, list_stringIn=[''], elem='', **dynamicsInputs):
        self.stringList1 = list_stringIn.copy()
        self.stringList1.append(elem)
        for di in dynamicsInputs:
            self.stringList1.append(dynamicsInputs[di])

    def str_list(self: 'list_str'):
        return self.stringList1

###############################################################################


class string_list_length():
    def __init__(self, list_string_In=['']):
        self.str_length = len(list_string_In)

    def file_length(self: 'int'):
        return self.str_length

##############################################################################


class string_list_extend_dyn:
    def __init__(self, list_string_In=[''], **dynamicsInputs):
        self.stringList2 = list_string_In.copy()
        for di in dynamicsInputs:
            self.stringList2.extend(dynamicsInputs[di])

    def out_list(self: 'list_str'):
        return self.stringList2

##############################################################################


class string_list_index_sublist:
    def __init__(self, in_string_list=[''], index_start=0, index_end=1):
        self.res = in_string_list[index_start:index_end]

    def out_subarray(self: 'list_str'):
        return self.res

##############################################################################


class string_list_index:
    def __init__(self, in_string_list=[''], index=0):
        self.res = in_string_list[index]

    def out_element(self: 'str'):
        return self.res

##############################################################################


class string_list_join:
    def __init__(self, in_string_list=[''], separator=', '):
        self.str_join = separator.join(in_string_list)

    def join_string(self: 'str'):
        return self.str_join

##############################################################################


class string_list_remove_duplicate:
    def __init__(self, in_string_list=['']):
        self.new_list = list(set(in_string_list))

    def new_string_list(self: 'list_str'):
        return self.new_list

##############################################################################


class string_list_sort:
    def __init__(self, in_string_list=[''], reverse=False):
        self.new_list = sorted(in_string_list, reverse=reverse)

    def sorted_string_list(self: 'list_str'):
        return self.new_list

##############################################################################


class string_get_index:
    def __init__(self, in_string_list=[''], element_to_search=''):
        self.indexf = in_string_list.index(element_to_search)

    def index_element(self: 'int'):
        return self.indexf

##############################################################################
