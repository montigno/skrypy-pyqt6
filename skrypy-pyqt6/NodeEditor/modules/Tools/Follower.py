class follow_dict():
    def __init__(self, inDict={}):
        self.inDict = inDict

    def outDict(self: 'dict'):
        return self.inDict

##########################################################################


class follow_int_simple():
    def __init__(self, inInt=0):
        self.inInt = inInt

    def outIn(self: 'int'):
        return self.inInt

##########################################################################


class follow_float_simple():
    def __init__(self, inFloat=0.0):
        self.inFloat = inFloat

    def outFloat(self: 'float'):
        return self.inFloat

##########################################################################


class follow_string_simple():
    def __init__(self, inString=''):
        self.inString = inString

    def outString(self: 'str'):
        return self.inString

##########################################################################


class follow_boolean_simple():
    def __init__(self, inBool=True):
        self.inBool = inBool

    def outBool(self: 'bool'):
        return self.inBool

##########################################################################


class follow_int_list():
    def __init__(self, listInt=[0]):
        self.listInt = listInt

    def outListInt(self: 'list_int'):
        return self.listInt

##########################################################################


class follow_float_list():
    def __init__(self, listFloat=[0.0]):
        self.listFloat = listFloat

    def outListFloat(self: 'list_float'):
        return self.listFloat

##########################################################################


class follow_string_list():
    def __init__(self, listString=['']):
        self.listString = listString

    def outListString(self: 'list_str'):
        return self.listString

##########################################################################


class follow_boolean_list():
    def __init__(self, listBool=[True]):
        self.listBool = listBool

    def outListBool(self: 'list_bool'):
        return self.listBool

##########################################################################


class follow_int_array():
    def __init__(self, arrayInt=[[0]]):
        self.arrayInt = arrayInt

    def outArrayInt(self: 'array_int'):
        return self.arrayInt

##########################################################################


class follow_float_array():
    def __init__(self, arrayFloat=[[0.0]]):
        self.arrayFloat = arrayFloat

    def outArrayFloat(self: 'array_float'):
        return self.arrayFloat

##########################################################################


class follow_string_array():
    def __init__(self, arrayString=[['']]):
        self.arrayString = arrayString

    def outArrayString(self: 'array_str'):
        return self.arrayString

##########################################################################


class follow_boolean_array():
    def __init__(self, arrayBool=[[True]]):
        self.arrayBool = arrayBool

    def outArrayBool(self: 'array_bool'):
        return self.arrayBool

##########################################################################


class follow_path_simple():
    def __init__(self, in_path='path'):
        self.outputPath = in_path

    def out_path(self: 'path'):
        return self.outputPath

##############################################################################


class follow_path_list():
    def __init__(self, in_path=['path']):
        self.outputPath = in_path

    def out_path(self: 'list_path'):
        return self.outputPath

##############################################################################
