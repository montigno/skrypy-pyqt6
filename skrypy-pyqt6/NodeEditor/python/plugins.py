import importlib
import inspect
import os
import sys


class Plugin():
    def __init__(self, parent=None):
        plugins_path = os.path.dirname(os.path.realpath(__file__))
        plugins_path = os.path.join(plugins_path, '..', '..', 'Plugins')
        self.path = plugins_path

    def plugins_load(self):
        list_imp = {}
        for (dirpath, dirs, files) in os.walk(self.path):
            for file in files:
                (name, ext) = os.path.splitext(file)
                if ext == ".py" and name != '__init__':
                    filePy = 'Plugins' + '.' + str(name)
                    imp = importlib.import_module(filePy)
                    importlib.reload(imp)
                    for nameClass, obj in inspect.getmembers(imp):
                        if inspect.isclass(obj):
                            if obj.__name__.lower() in imp.__name__.lower():
                                list_imp[obj.__name__] = imp.__name__
        return list_imp
