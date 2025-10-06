##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

from importlib import reload
import importlib
import inspect
import list_imports
import os


class getlistModules:

    def __init__(self, rep):
        modules = os.path.dirname(__file__)
        modules, last = os.path.split(modules)
        modules = os.path.join(modules, 'modules', rep)

        if os.path.exists(os.path.join(modules, rep + '.png')):
            self.icon = os.path.join(modules, rep + '.png')
        else:
            self.icon = os.path.join(modules, '..', '..', '..', 'ressources', 'Python.png')

        self.category = {}
        self.config = []
        self.objectsInModul = []
        self.listLib = []

        for name in os.listdir(modules):
            if name.endswith(".py"):
                filePy = 'NodeEditor.modules.' + \
                         rep + \
                         '.' + \
                         str(name.replace('.py', ''))
                # filePyAbsolute = os.path.join(modules, name)
                # first_line = ''
                # with open(filePyAbsolute) as f:
                #     first_line = f.readline()
                # if "skrypy_modules" in first_line:
                #     print(first_line, name)
                imp = importlib.import_module(filePy)
                importlib.reload(imp)
                self.objectsInModul = list_imports.get(os.path.join(modules, name))
                listClass = []
                for nameClass, obj in inspect.getmembers(imp):
                    # print(nameClass," : ",inspect.getcomments(obj))
                    if inspect.isclass(obj):
                        try:
                            src = inspect.getsource(obj)
                            for lb in self.objectsInModul:
                                if lb:
                                    if ('NodeEditor' not in lb and
                                            'PyQt6' not in lb):
                                        try:
                                            lb = lb[0:lb.index(".")]
                                        except Exception as e:
                                            pass
                                        self.listLib.append(lb)
                            listOrderClass = self.findClassOrder(src)

                            if obj.__module__.find('modules.sources') == -1:
                                listArgs = inspect.getfullargspec(obj)
                                listArgs[0].remove('self')
                                # print('before :', listArgs[3])
                                result = None
                                if listArgs[3]:
                                    result = []
                                    lst_tmp = list(listArgs[3])
                                    for el in lst_tmp:
                                        try:
                                            if 'enumerate' in el:
                                                # result.append(el.replace(" ", ""))
                                                result.append(el.strip())
                                            else:
                                                result.append(el)
                                        except Exception as err:
                                            result.append(el)
                                    result = tuple(result)
                                # print('after  :', result)
                                listArgs = (listArgs[0], listArgs[1], listArgs[2], result)
                                listFunctionFound = inspect.getmembers(obj, inspect.isfunction)
                                listFunction = []
                                listTypeOut = []
                                for listF in listFunctionFound:
                                    if (listF[0] != '__init__' and
                                            str(listF[0])[0] != '_'):
                                        try:
                                            a = listF[1].__annotations__['self']
                                            listTypeOut.append(a)
                                            listFunction.append(listF[0])
                                        except Exception as e:
                                            print(listF[1]
                                                  + 'has not annotation')

                                # to put list out in order
                                k = len(listFunction)
                                srf = []
                                for k in listOrderClass:
                                    srf.append(listFunction.index(k))
                                listTypeOut = [listTypeOut[i] for i in srf]
                                listClass.append((nameClass,
                                                  listArgs[0],
                                                  listArgs[3],
                                                  listOrderClass,
                                                  listTypeOut))
                        except Exception as e:
                            pass

                self.category[name.replace('.py', '')] = list(listClass)

    def findClassOrder(self, txtClass):
        list = []
        for line in txtClass.splitlines():
            if ('def ' in line and
                    'def __init__' not in line and
                    'def _' not in line):
                list.append(line[line.index('def ') + 4:line.index('(self')])
#         list.sort()
        return list

    def getIconPath(self):
        return self.icon

    def listInspect(self):
        return self.category

    def listDepends(self):
        return set(self.listLib)
