class bruker_search_value():
    """
    Get key-value metadata

    Args:
        file: (path) path of metadata file ('subject', 'acqp', 'reco', 'method' or 'visu_pars')

    Returns:
        value: (various format) value of the corresponding key

    Note:
        GUI: no
    """
    def __init__(self, file='path', param=''):
        import os
        if '=' not in param:
            param += '='
        if os.path.exists(file):
            with open(file, 'r') as stream:
                txt = stream.read()
                tmp = ''
                try:
                    tmp = txt[txt.index(param):]
                except Exception as e:
                    pass
            if tmp:
                try:
                    tmp = tmp[0:tmp.index('##')]
                except Exception as e:
                    pass
                try:
                    tmp = tmp[0:tmp.index('$$')]
                except Exception as e:
                    pass
                if '(' in tmp:
                    tmp = tmp[tmp.index('\n') + 1:]
                else:
                    tmp = tmp[tmp.index('=') + 1:]
                tmp = tmp.strip()
                self.value = tmp
            else:
                self.value = 'parameter or value not found\n'
        else:
            self.value = 'file not found\n'

    def value(self: 'str'):
        return self.value

##############################################################################


class bruker_get_value():
    """
    Get key-value metadata

    Args:
        file: (path) path of metadata file ('subject', 'acqp', 'reco', 'method' or 'visu_pars')
        param: (string) metadata key

    Returns:
        float_array_values: (array of float) return array of float if exits ('None' otherwise)
        float_list_values: (list of float) return list of float if exits ('None' otherwise)
        float_value: (float) return float if exits ('None' otherwise)
        int_array_values: (array of int) return array of int if exits ('None' otherwise)
        int_list_values: (list of int) return list of int if exits ('None' otherwise)
        int_value: (int) return int if exits ('None' otherwise)
        str_value: (string) return string if exits ('None' otherwise)

    Note:
        GUI: no
    """
    def __init__(self, file='path', param=''):
        import os
        import numpy as np

        if '=' not in param:
            param += '='
        dim = 1
        self.float_array_value = None
        self.float_list_value = None
        self.float_value = None
        self.int_array_value = None
        self.int_list_value = None
        self.int_value = None
        self.str_value = None

        if os.path.exists(file):
            with open(file, 'r') as stream:
                txt = stream.read()
                tmp0 = ''
                try:
                    tmp0 = txt[txt.index(param):]
                except Exception as e:
                    pass
            if tmp0:
                try:
                    tmp0 = tmp0[0:tmp0.index('##')]
                except Exception as e:
                    pass
                try:
                    tmp0 = tmp0[0:tmp0.index('$$')]
                except Exception as e:
                    pass
                if '(' in tmp0:
                    dim = eval(tmp0[tmp0.index('('): tmp0.index(')') + 1])
                    tmp0 = tmp0[tmp0.index('\n') + 1:]
                else:
                    tmp0 = tmp0[tmp0.index('=') + 1:]
                tmp0 = tmp0.strip()
                tmp0 = tmp0.replace('\n', '')
                tmp = tmp0.split(' ')
                tmp = np.array(tmp)
                try:
                    tp = type(eval(tmp[0])).__name__
                except Exception as err:
                    tp = 'str'
                if tp == 'int' and '.' not in tmp0:
                    tmp = tmp.astype(np.int32)
                    if type(dim).__name__ == 'tuple':
                        self.int_array_value = np.resize(tmp, dim).tolist()
                    elif len(tmp) > 1:
                        self.int_list_value = tmp.tolist()
                    else:
                        self.int_value = tmp[0]
                elif tp == 'float' or (tp == 'int' and '.' in tmp0):
                    tmp = tmp.astype(np.float64)
                    if type(dim).__name__ == 'tuple':
                        self.float_array_value = np.resize(tmp, dim).tolist()
                    elif len(tmp) > 1:
                        self.float_list_value = tmp.tolist()
                    else:
                        self.float_value = tmp[0]
                else:
                    if len(tmp) == 1:
                        self.str_value = str(tmp[0])
                    else:
                        self.str_value = ' '.join(tmp)

    def float_array_values(self: 'array_float'):
        return self.float_array_value

    def float_list_values(self: 'list_float'):
        return self.float_list_value

    def float_value(self: 'float'):
        return self.float_value

    def int_array_values(self: 'array_int'):
        return self.int_array_value

    def int_list_values(self: 'list_int'):
        return self.int_list_value

    def int_value(self: 'int'):
        return self.int_value

    def str_value(self: 'str'):
        return self.str_value

##############################################################################


class bruker_get_value2():
    def __init__(self, file='path', param=''):
        import os
        import numpy as np

        if '=' not in param:
            param += '='
        dim = 1
        self.float_array_value = None
        self.float_list_value = None
        self.float_value = None
        self.int_array_value = None
        self.int_list_value = None
        self.int_value = None
        self.str_value = None

        if os.path.exists(file):
            with open(file, 'r') as stream:
                txt = stream.read()
                tmp = ''
                try:
                    tmp = txt[txt.index(param):]
                except Exception as e:
                    pass
            if tmp:
                try:
                    tmp = tmp[0:tmp.index('##')]
                except Exception as e:
                    pass
                try:
                    tmp = tmp[0:tmp.index('$$')]
                except Exception as e:
                    pass
                if '(' in tmp:
                    dim = eval(tmp[tmp.index('('): tmp.index(')') + 1])
                    tmp = tmp[tmp.index('\n') + 1:]
                else:
                    tmp = tmp[tmp.index('=') + 1:]
                tmp = tmp.strip()
                tmp = tmp.replace('\n', '')
                self.str_value = tmp

    def str_value(self: 'str'):
        return self.str_value

##############################################################################


class bruker_normalize_image:
    """
    Image normalization. apply the multiplier coefficient and the offset:

        image_normalized = image*slope + offsets

    Args:
        image: (matrix) matrix of the image
        slope: (list of float) the multiplier coefficient
        offsets: (list of float) the offsets

    Returns:
        image_normalized: (matrix) matrix of the normalized image

    Note:
        GUI: no
    """
    def __init__(self, image=[[0.0]], slope=[0.0], offsets=[0.0]):
        import numpy as np
        dim = image.shape
        if len(dim) == 3:
            self.img_norm = np.zeros((dim[0], dim[1], dim[2]))
            if isinstance(slope, list) and isinstance(offsets, list):
                for sl in range(0, dim[2]):
                    self.img_norm[:, :, sl] = image[:, :, sl] * slope[sl] + offsets[sl]
            else:
                for sl in range(0, dim[2]):
                    self.img_norm[:, :, sl] = image[:, :, sl] * slope + offsets
        elif len(dim) == 4:
            self.img_norm = np.zeros((dim[0], dim[1], dim[2], dim[3]))
            if isinstance(slope, list) and isinstance(offsets, list):
                for sl in range(0, dim[3]):
                    self.img_norm[:, :, :, sl] = image[:, :, :, sl] * slope[sl] + offsets[sl]
            else:
                for sl in range(0, dim[2]):
                    self.img_norm[:, :, :, sl] = image[:, :, :, sl] * slope + offsets
        else:
            self.img_norm = [[0.0]]

    def image_normalized(self: 'array_float'):
        return self.img_norm

##############################################################################


class bruker_get_metadata_files:
    """
    Allows to get metadata files 'subject', 'acqp', 'reco', 'method' and 'visu_pars' from the file '2dseq'

    Args:
        bruker_file: (path) '2dseq' file path

    Returns:
        subject_file: (path) 'subject' file path
        visupars_file: (path) 'visupars' file path
        reco: (path) 'reco' file path
        method: (path) 'method' file path
        acqp: (path) 'acqp' file path
    Note:
        GUI: no
    """
    def __init__(self, bruker_file='path'):
        import os
        if bruker_file.endswith('2dseq'):
            dir = os.path.dirname(bruker_file)
            self.visupars_file = os.path.join(dir, 'visu_pars')
            if not os.path.exists(self.visupars_file):
                self.visupars_file = ''
            self.reco_file = os.path.join(dir, 'reco')
            if not os.path.exists(self.reco_file):
                self.reco_file = ''
            dir = os.path.dirname(os.path.dirname(dir))
            self.acqp_file = os.path.join(dir, 'acqp')
            if not os.path.exists(self.acqp_file):
                self.acqp_file = ''
            self.method_file = os.path.join(dir, 'method')
            if not os.path.exists(self.method_file):
                self.method_file = ''
            dir = os.path.dirname(dir)
            self.subject_file = os.path.join(dir, 'subject')
            if not os.path.exists(self.subject_file):
                self.subject_file = ''

    def subject_file(self: 'path'):
        return self.subject_file

    def visupars_file(self: 'path'):
        return self.visupars_file

    def reco_file(self: 'path'):
        return self.reco_file

    def method_file(self: 'path'):
        return self.method_file

    def acqp_file(self: 'path'):
        return self.acqp_file

##############################################################################
