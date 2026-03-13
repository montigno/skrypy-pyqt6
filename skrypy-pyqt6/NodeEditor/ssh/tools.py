import ast
import re


class GetValueInBrackets():

    def __init__(self, line, args):
        self.res = []
        line = line.rstrip()
        for i in range(len(args) - 1):
            tmp = ''
            try:
                # tmp = line[line.index(args[i] + '=') +
                #            len(args[i]) + 1:line.index(args[i + 1] + '=') - 1][1:-1]
                start = line.index(args[i] + '=') + len(args[i]) + 1
                end = line.index(args[i + 1] + '=') - 1
                tmp = line[start:end][1:-1]
            except Exception:
                try:
                    start = line.index(args[i] + '=') + len(args[i]) + 1
                    end = line.index(args[i + 2] + '=') - 1
                    tmp = line[start:end][1:-1]
                    # tmp = line[line.index(args[i] + '=') +
                    #            len(args[i]) +
                    #            1:line.index(args[i + 2] + '=') - 1][1:-1]
                except Exception:
                    pass
            self.res.append(tmp)
        self.res.append(line[line.index(args[-1] + '=') + len(args[-1]) + 1:][1:-1])

    def getValues(self):
        return self.res


# class GetValueInBrackets():
#
#     def __init__(self, line, args):
#         self.res = re.findall(r"\[(.*?)\]", line)
#
#     def getValues(self):
#         print(self.res)
#         return self.res


class SetValueInBrackets():

    def __init__(self, tags, values):
        self.line = ""
        for i in range(len(tags)):
            self.line += "{}=[{}] ".format(tags[i], values[i])

    def getNewLine(self):
        return self.line


class ReorderList():

    def __init__(self, listToOrder):
        listOrder = self.sorted_nicely(listToOrder)
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
                lengt = 1
                if isinstance(self.var[0], list):
                    lengt = 2
                    if isinstance(self.var[0][0], list):
                        lengt = 3
            if lengt == 1:
                typVar = 'list'
                typVal = self.isPath(self.var[0])
            elif lengt == 2:
                typVar = 'array'
                typVal = self.isPath(self.var[0][0])
            elif lengt == 3:
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


class eval_type():
    def __init__(self, value, form):

        self.vout = value

        if not form:
            form = ''
        elif 'enumerate' in form:
            pass
        elif 'path' in form:
            self.vout = self.vout.replace('\\n', '')
        elif form == 'bool':
            self.vout = eval(self.vout)
        elif 'int' in form or 'float' in form:
            self.vout = eval(self.vout)[1]
        elif form == 'list_str':
            self.vout = eval(self.vout)
            tmp = []
            for lstVal in self.vout:
                if '*' in lstVal:
                    tmp.append(lstVal[0:-1])
                else:
                    tmp.append(lstVal)
            self.vout = tmp
        elif 'tuple' in form:
            self.vout = ast.literal_eval(self.vout)
        try:
            self.vout = eval(self.vout)
        except Exception:
            pass

    def getVout(self):
        return self.vout
