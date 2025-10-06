class dict_new_value():
    def __init__(self, key='', value=0.0):
        self.new_dict = {}
        self.new_dict[key] = value

    def out_dict(self: 'dict'):
        return self.new_dict

###############################################################################


class dict_get_value_dyn():
    def __init__(self, input_dict={}, tag='', **dynamicsInputs):
        if tag in input_dict:
            self.outValue = input_dict[tag]
            for di, vi in dynamicsInputs.items():
                if vi in self.outValue:
                    self.outValue = self.outValue[vi]
                else:
                    self.outValue = None
                    break
        else:
            self.outValue = None

    def out_value(self: 'str'):
        return self.outValue

    def out_value_dict(self: 'dict'):
        if isinstance(self.outValue, dict):
            return dict(self.outValue)
        else:
            return {}

###############################################################################


class dict_set_value_dyn():
    def __init__(self, input_dict={}, key_value={}, **dynamicsInputs):
        self.outValue = input_dict.copy()
        self.outValue.update(key_value)
        for di, vi in dynamicsInputs.items():
            self.outValue.update(vi)

    def new_dict(self: 'dict'):
        return self.outValue

###############################################################################


class dict_to_string():
    def __init__(self, input_dict={}):
        self.outValue = str(input_dict.copy())

    def dict_str(self: 'str'):
        return self.outValue

###############################################################################


class dict_zip_keys_values():
    def __init__(self, coord=[''], value=['']):
        self.setzip = zip(coord, value)

    def out_zipped(self: 'dict'):
        return dict(self.setzip)

###############################################################################


class dict_to_array():
    def __init__(self, dict_in={}):
        self.dictlist = []
        for key, value in dict_in.items():
            temp = [key, value]
            self.dictlist.append(temp)

    def array_dict(self: 'array_str'):
        return self.dictlist

###############################################################################


class dict_list_keys_values():
    def __init__(self, dict_in={}):
        self.keyslist, self.valueslist = [], []
        for key, value in dict_in.items():
            self.keyslist.append(key)
            self.valueslist.append(value)

    def keys_dict(self: 'list_str'):
        return self.keyslist

    def values_dict(self: 'list_str'):
        return self.valueslist
