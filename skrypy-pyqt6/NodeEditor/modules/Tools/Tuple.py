class tuple_sub_tuple:
    def __init__(self, tuple_in=(0, 1), index_start=0, index_end=1):
        if index_start == index_end:
            self.sub = tuple_in[index_start]
        else:
            self.sub = tuple_in[index_start:index_end]

    def sub_tuple(self: 'tuple'):
        return self.sub

#####################################################################


class tuple_concatenat_dyn:
    def __init__(self, tuple_in=(0,), **dynamicsInputs):
        self.tupleList = list(tuple_in)
        for di in dynamicsInputs:
            self.tupleList.extend(list(dynamicsInputs[di]))
        self.tupleList = tuple(self.tupleList)

    def tuple_list(self: 'list_tuple'):
        return self.tupleList

#############################################################################


class tuple_getElement():
    def __init__(self, tuple_in=(0,), index=0):
        self.out_tup = tuple_in[index]

    def tup_value_to_index(self: 'float'):
        return self.out_tup

#############################################################################


class tuple_length():
    def __init__(self, tuple_in=(0,)):
        self.len = len(tuple_in)

    def out_len(self: 'int'):
        return self.len

############################################################################


class tuple_create_dyn():
    def __init__(self, element='', **dynamicsInputs):
        elem_tuple = [element]
        for di, vi in dynamicsInputs.items():
            elem_tuple.append(vi)
        self.out_tup = tuple(elem_tuple)

    def out_tuple(self: 'tuple'):
        return self.out_tup
