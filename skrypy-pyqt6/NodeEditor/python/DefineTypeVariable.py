import ast
import numpy as np
import os


class DefineTypeVariable:
    def __init__(self, var):
        self.var = var
        try:
            self.var = ast.literal_eval(var)
        except Exception as e:
            pass

    def returntype(self):
        typVal = self._isPath(self.var)
        typVar = ''
        lenDim, lenVar = 0, 1
        if type(self.var).__name__ in ['memmap', 'ndarray', 'list']:
            lenVar = np.shape(self.var)
            lenDim = len(lenVar)
            if lenDim == 1:
                lenVar = len(self.var)
                typVar = 'list'
                typVal = self._isPath(self.var[0])
            elif lenDim == 2:
                typVar = 'array'
                typVal = self._isPath(self.var[0][0])
            elif lenDim == 3:
                typVar = 'array'
                typVal = self._isPath(self.var[0][0][0])

        elif type(self.var).__name__ in 'tuple':
            lenVar = len(self.var)
            typVar = 'tuple'
            typVal = self._isPath(self.var[0])
        elif type(self.var).__name__ in 'dict':
            lenVar = len(self.var)
            typVar = 'dict'
            values_view = self.var.values()
            value_iterator = iter(values_view)
            first_value = next(value_iterator)
            typVal = self._isPath(first_value)
        if typVar and typVal:
            typVar += '_'
        return typVar + typVal, self.var, lenVar

    def _isPath(self, varble):
        if type(varble).__name__ == 'str':
            if 'path' in varble:
                return 'path'
            elif os.path.isfile(varble) or os.path.isdir(varble):
                return 'path'
            else:
                return type(varble).__name__
        else:
            return type(varble).__name__
