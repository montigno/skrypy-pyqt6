import ast
import re
import os
from cryptography.fernet import Fernet


class GetValueInBrackets():

    def __init__(self, line, args):
        self.res = []
        line = line.rstrip()
        for i in range(len(args) - 1):
            tmp = ''
            try:
                tmp = line[line.index(args[i] + '=') + len(args[i]) + 1:line.index(args[i + 1] + '=') - 1][1:-1]
            except Exception as e:
                try:
                    tmp = line[line.index(args[i] + '=') + len(args[i]) + 1:line.index(args[i + 2] + '=') - 1][1:-1]
                except Exception as e:
                    pass
            self.res.append(tmp)
        self.res.append(line[line.index(args[-1] + '=') + len(args[-1]) + 1:][1:-1])

    def getValues(self):
        return self.res


class SetValueInBrackets():

    def __init__(self, tags, values):
        self.line = ""
        for i in range(len(tags)):
            self.line += "{}=[{}] ".format(tags[i], values[i])

    def getNewLine(self):
        return self.line


class ReorderList():

    def __init__(self, list):
        listOrder = self.sorted_nicely(list)
        self.list = listOrder

    def sorted_nicely(self, lst):
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(lst, key=alphanum_key)

    def getNewList(self):
        return self.list


class DefinitType():

    def __init__(self, var):
        self.var = var
        # print(var, ' : ', type(var).__name__)

    def returntype(self):
        if type(self.var).__name__ == 'str':
            if self.var == 'path':
                typVal = 'path'
            else:
                typVal = type(self.var).__name__
        else:
            typVal = type(self.var).__name__

        typVar = ''
        if 'list' in type(self.var).__name__:
            if isinstance(self.var, list):
                len = 1
                if isinstance(self.var[0], list):
                    len = 2
                    if isinstance(self.var[0][0], list):
                        len = 3
            if len == 1:
                typVar = 'list'
                typVal = self.isPath(self.var[0])
            elif len == 2:
                typVar = 'array'
                typVal = self.isPath(self.var[0][0])
            elif len == 3:
                typVar = 'array'
                typVal = self.isPath(self.var[0][0][0])

        elif 'tuple' in type(self.var).__name__:
            typVar = 'tuple'
            typVal = self.isPath(self.var[0])

        elif 'enumerate' in type(self.var).__name__:
            typVar = 'enumerate'
            typVal = 'str'

        if typVar == '':
            return typVal
        # elif typVar == 'enumerate':
        #     return typVar
        else:
            return typVar + '_' + typVal

    def isPath(self, varble):
        if type(varble).__name__ == 'str':
            if 'path' in varble:
                return 'path'
            else:
                return type(varble).__name__
        else:
            return type(varble).__name__


class set_dph():
    def __init__(self, var):
        self.fk = Fernet.generate_key()
        # filek = os.path.expanduser('~')
        # filek = os.path.join(filek, '.skrypy', 'sv_gh.txt')
        # with open(filek, 'wb') as kfile:
        #     kfile.write(fk)
        fernet = Fernet(self.fk)
        slopw = var[::-1]
        slopw = slopw[2:] + slopw[0:2]
        slopw = slopw.encode("utf-8")
        token = fernet.encrypt(slopw)
        self.token = fernet.encrypt(token)

    def get_shn(self):
        return self.token

    def get_fk(self):
        return self.fk


class get_dph():
    def __init__(self, var, fk):
        # filek = os.path.expanduser('~')
        # filek = os.path.join(filek, '.skrypy', 'sv_gh.txt')
        # with open(filek, 'rb') as kfile:
        #     fk = kfile.read()
        fernet = Fernet(fk)
        untoken = fernet.decrypt(var).decode()
        untoken = fernet.decrypt(untoken).decode()
        untoken = untoken[::-1]
        self.untoken = untoken[2:] + untoken[0:2]

    def get_ushn(self):
        return self.untoken


# class set_dph():
#     def __init__(self, msg):
#         self.fk = Fernet.generate_key()
#         # filek = os.path.expanduser('~')
#         # filek = os.path.join(filek, '.skrypy', 'sv_gh.txt')
#         # with open(filek, 'wb') as kfile:
#         #     kfile.write(self.fk)
#         fernet = Fernet(self.fk)
#         self.token = fernet.encrypt(msg.encode())
#
#     def get_shn(self):
#         return self.token
#
#     def get_fk(self):
#         return self.fk


# class get_dph():
#     def __init__(self, msg, fk):
#         # filek = os.path.expanduser('~')
#         # filek = os.path.join(filek, '.skrypy', 'sv_gh.txt')
#         # with open(filek, 'rb') as kfile:
#         #     fk = kfile.read()
#         fernet = Fernet(fk)
#         self.untoken = fernet.decrypt(msg).decode()
#
#     def get_ushn(self):
#         return self.untoken


class eval_type():
    def __init__(self, value, format):

        self.vout = value

        if not format:
            format = ''
        elif 'enumerate' in format:
            pass
        elif 'path' in format:
            self.vout = self.vout.replace('\\n', '')
        elif format == 'bool':
            self.vout = eval(self.vout)
        elif 'int' in format or 'float' in format:
            self.vout = eval(self.vout)[1]
        elif format == 'list_str':
            self.vout = eval(self.vout)
            tmp = []
            for lstVal in self.vout:
                if '*' in lstVal:
                    tmp.append(lstVal[0:-1])
                else:
                    tmp.append(lstVal)
            self.vout = tmp
        elif 'tuple' in format:
            self.vout = ast.literal_eval(self.vout)
        try:
            self.vout = eval(self.vout)
        except Exception as er:
            pass

    def getVout(self):
        return self.vout
