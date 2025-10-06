class string_compare:
    def __init__(self,
                 in_string='',
                 compareTo='',
                 type_compare="enumerate(('equal','contains'))"):
        if type_compare == 'equal':
            self.res = in_string == compareTo
        else:
            self.res = in_string in compareTo

    def compare_res(self: 'bool'):
        return self.res

##############################################################################


class string_concatenat_dyn:
    def __init__(self, stringIn='', **dynamicsInputs):

        self.stringConc = stringIn
        for di in dynamicsInputs:
            self.stringConc += str(dynamicsInputs[di])

    def str_conc(self: 'str'):
        return self.stringConc

##############################################################################


class string_replace:
    def __init__(self, string_in='', charactToreplace='', newCharact=''):
        self.newString = string_in.replace(charactToreplace, newCharact)

    def newString(self: 'str'):
        return self.newString

##############################################################################


class string_split:
    def __init__(self, in_string='', expr=''):
        self.listString = in_string.split(expr)

    def list_string(self: 'list_str'):
        return self.listString

##############################################################################


class string_substring:
    def __init__(self, in_string='', start=0, end=0):
        if end == -1:
            self.substr = in_string[start:]
        else:
            self.substr = in_string[start:end + 1]

    def substring(self: 'str'):
        return self.substr

##############################################################################


class string_substring_2:
    def __init__(self, in_string='', begin='', end=''):
        tmp = str(in_string)
        tmp = tmp[tmp.index(begin):]
        self.substr = tmp[0:tmp.index(end)]

    def substring(self: 'str'):
        return self.substr

##############################################################################


class string_to_float_list():
    def __init__(self, inString=''):
        import numpy as np
        tmp = np.array(inString.split(' '))
        tmp = tmp.astype(np.float64)
        self.outval = tmp

    def outListFloat(self: 'list_float'):
        return self.outval

##############################################################################


class string_to_float_array():
    def __init__(self, inString=''):
        from NodeEditor.api.defineTypeVariable import DefineTypeVariable
        typ, val = DefineTypeVariable(inString).returntype()
        if typ == 'arrayfloat':
            self.outval = val
        else:
            self.outval = None

    def outArrayFloat(self: 'array_float'):
        return self.outval

##############################################################################


class string_to_int():
    def __init__(self, inString=''):
        from NodeEditor.api.defineTypeVariable import DefineTypeVariable
        typ, val = DefineTypeVariable(inString).returntype()
        if typ == 'int':
            self.outval = val
        else:
            self.outval = None

    def outInt(self: 'int'):
        return self.outval

##############################################################################


class string_to_int_list():
    def __init__(self, inString=''):
        import numpy as np
        tmp = np.array(inString.split(' '))
        tmp = tmp.astype(np.int64)
        self.outval = tmp

    def outInt(self: 'list_int'):
        return self.outval

##############################################################################


class string_to_int_array():
    def __init__(self, inString=''):
        from NodeEditor.api.defineTypeVariable import DefineTypeVariable
        typ, val = DefineTypeVariable(inString).returntype()
        if typ == 'arrayint':
            self.outval = val
        else:
            self.outval = None

    def outInt(self: 'array_int'):
        return self.outval

##############################################################################


class string_to_list_dyn:
    def __init__(self, string_in='', **dynamicsInputs):
        self.stringList = [string_in]
        for di in dynamicsInputs:
            self.stringList.append(dynamicsInputs[di])

    def list_str(self: 'list_str'):
        return self.stringList

##############################################################################


class string_to_float():
    def __init__(self, inString=''):
        self.outval = float(inString)

    def outFloat(self: 'float'):
        return self.outval

##############################################################################


class string_to_boolean():
    def __init__(self, inString=''):
        from NodeEditor.api.defineTypeVariable import DefineTypeVariable
        typ, val = DefineTypeVariable(inString).returntype()
        if typ == 'bool':
            self.outval = val
        else:
            self.outval = None

    def outBool(self: 'bool'):
        return self.outval

##############################################################################


class string_to_boolean_list():
    def __init__(self, inString=''):
        from NodeEditor.api.defineTypeVariable import DefineTypeVariable
        typ, val = DefineTypeVariable(inString).returntype()
        if typ == 'listbool':
            self.outval = val
        else:
            self.outval = None

    def outListBool(self: 'list_bool'):
        return self.outval

##############################################################################


class string_to_boolean_array():
    def __init__(self, inString=''):
        from NodeEditor.api.defineTypeVariable import DefineTypeVariable
        typ, val = DefineTypeVariable(inString).returntype()
        if typ == 'arraybool':
            self.outval = val
        else:
            self.outval = None

    def outArrayBool(self: 'array_bool'):
        return self.outval

##############################################################################


class string_to_path():
    def __init__(self, inString=''):
        from NodeEditor.api.defineTypeVariable import DefineTypeVariable
        typ, val = DefineTypeVariable(inString).returntype()
        if typ == 'path':
            self.outval = val
        else:
            self.outval = None

    def outPath(self: 'path'):
        return self.outval

##############################################################################


class string_to_path_list():
    def __init__(self, inString=''):
        self.outval = eval(inString)

    def outPath(self: 'list_path'):
        return self.outval

##############################################################################


class string_to_path_array():
    def __init__(self, inString=''):
        from NodeEditor.api.defineTypeVariable import DefineTypeVariable
        typ, val = DefineTypeVariable(inString).returntype()
        if typ == 'arraypath':
            self.outval = val
        else:
            self.outval = None

    def outPath(self: 'array_path'):
        return self.outval

##############################################################################


class string_to_dict():
    def __init__(self, inString=''):
        from NodeEditor.api.defineTypeVariable import DefineTypeVariable
        typ, val = DefineTypeVariable(inString).returntype()
        if typ == 'dict':
            self.outval = val
        else:
            self.outval = None

    def outInt(self: 'dict'):
        return self.outval

##############################################################################


class string_to_tuple_dyn:
    def __init__(self, inString='', **dynamicsInputs):
        self.tupleAppen = (inString,)
        for di in dynamicsInputs:
            self.tupleAppen = (*self.tupleAppen, dynamicsInputs[di])

    def out_tuple(self: 'tuple'):
        return self.tupleAppen

##############################################################################


class String_eval():
    def __init__(self, inString=''):
        from NodeEditor.api.defineTypeVariable import DefineTypeVariable
        listType = ['float',
                    'int',
                    'str',
                    'bool',
                    'path',
                    'listfloat',
                    'listint',
                    'liststr',
                    'listbool',
                    'listpath',
                    'arrayfloat',
                    'arrayint',
                    'arraystr',
                    'arraybool',
                    'arraypath',
                    'tuple']
        self.listVar = []
        for i in range(0, len(listType)):
            self.listVar.append(None)
        typ, val = DefineTypeVariable(inString).returntype()
        ind = listType.index(typ)
        self.listVar[ind] = val

    def Float(self: 'float'):
        return self.listVar[0]

    def Int(self: 'int'):
        return self.listVar[1]

    def String(self: 'str'):
        return self.listVar[2]

    def Boolean(self: 'bool'):
        return self.listVar[3]

    def Path(self: 'path'):
        return self.listVar[4]

    def List_Float(self: 'list_float'):
        return self.listVar[5]

    def List_Int(self: 'list_int'):
        return self.listVar[6]

    def List_String(self: 'list_str'):
        return self.listVar[7]

    def List_Boolean(self: 'list_bool'):
        return self.listVar[8]

    def List_Path(self: 'list_path'):
        return self.listVar[9]

    def Array_Float(self: 'array_float'):
        return self.listVar[10]

    def Array_Int(self: 'array_int'):
        return self.listVar[11]

    def Array_String(self: 'array_str'):
        return self.listVar[12]

    def Array_Boolean(self: 'array_bool'):
        return self.listVar[13]

    def Array_Path(self: 'array_path'):
        return self.listVar[14]

    def Tuple(self: 'tuple'):
        return self.listVar[15]
