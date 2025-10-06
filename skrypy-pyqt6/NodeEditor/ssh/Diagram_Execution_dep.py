##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

import ast
import importlib
from multiprocessing import Process, Semaphore, Pool
import os
import sys
import re
import threading
import time

from NodeEditor.python.classForProbe2 import printProbe


class execution2():

    def __init__(self, n_cpu, parent=None):
        super().__init__()
        self.n_cpu = n_cpu
        self.must_stopped = False

    def check_button(self, status):
        self.must_stopped = True

    def alphaNumOrder(self, string):
        return ''.join([format(int(x), '05d') if x.isdigit()
                       else x for x in re.split(r'(\d+)', string)])

    @classmethod
    def methodForMultiprocessing(cls, n_cpu, *args):
        execution2.must_stopped = False
        return execution2.go_execution(execution2(n_cpu), *args)

    def go_execution(self, diagram, listDynamicValue, sema):

        if sema:
            sema.acquire()

        # compiles a list of items
        listConnctIn = []
        listBlockExecution = []
        listBlock = {}
        listOut = []
        listModul = {}
        listConnctOut = []

        error_color = '\33[31m'

        for i, ln in enumerate(diagram.splitlines()):
            if i == 0:
                listConnctIn.append(ast.literal_eval(ln))
                listConnctIn = listConnctIn[0]
            if i == 1:
                listBlockExecution.append(ast.literal_eval(ln))
                listBlockExecution = listBlockExecution[0]
            if i == 2:
                listBlock = ast.literal_eval(ln)
            if i == 3:
                listOut.append(ast.literal_eval(ln))
                listOut = listOut[0]
            if i == 4:
                listModul = ast.literal_eval(ln)
            if i == 5:
                listConnctOut.append(ast.literal_eval(ln))
                listConnctOut = listConnctOut[0]
            if i == 6:
                break

        # print('listConnctIn:', listConnctIn)
        # print('listBlockExecution:', listBlockExecution)
        # print('listBlock:', listBlock)
        # print('listOut:', listOut)
        # print('listModul:', listModul)
        # print('listConnctOut:', listConnctOut)


        listNodeValue = list(set(listOut))

        listDynamicValueSub = {}

        listOutsInter = []
        try:
            tmp = diagram[diagram.index('[interlinks]'):len(diagram)]
            tmp1ine = tmp.splitlines()[1]
            listOutsInter = eval(tmp1ine)
        except Exception as err:
            pass

        for lstOut in listOutsInter:
            try:
                listDynamicValueSub[lstOut] = listDynamicValue[lstOut]
            except Exception as err:
                pass

        listModExecution, listScriptExecution = {}, {}
        listForExecution, listIfExecution = {}, {}

        for ls in listBlockExecution:

            if 'M' in ls:
                tmp = diagram[diagram.index('[submod ' + ls + ']'):len(diagram)]
                tmp1ine = ''
                for i, ln in enumerate(tmp.splitlines()):
                    if i > 0 and i <= 6:
                        tmp1ine += ln + '\n'
                    elif i > 6:
                        break
                listModExecution[ls] = tmp1ine
            elif 'F' in ls:
                tmp = diagram[diagram.index('[loopfor ' + ls + ']'):len(diagram)]
                tmp1ine = ''
                for i, ln in enumerate(tmp.splitlines()):
                    if i > 0 and i <= 6:
                        tmp1ine += ln + '\n'
                    elif i > 6:
                        break
                listForExecution[ls] = tmp1ine
            elif 'I' in ls:
                tmp = diagram[diagram.index('[loopif ' + ls + ' True]'):len(diagram)]
                tmp1ine = ''
                for i, ln in enumerate(tmp.splitlines()):
                    if i == 1 or i == 2 or i == 3 or i == 4 or i == 5 or i == 6:
                        tmp1ine += ln + '\n'
                    elif i > 6:
                        break
                listIfExecution[ls + '-true'] = tmp1ine
                tmp = diagram[diagram.index('[loopif ' + ls + ' False]'):len(diagram)]
                tmp1ine = ''
                for i, ln in enumerate(tmp.splitlines()):
                    if i == 1 or i == 2 or i == 3 or i == 4 or i == 5 or i == 6:
                        tmp1ine += ln + '\n'
                    elif i > 6:
                        break
                listIfExecution[ls + '-false'] = tmp1ine
            elif 'S' in ls or 'J' in ls:
                tmp = diagram[diagram.index('[source ' + ls + ']'):diagram.index('[/source ' + ls + ']')]
                tmp = tmp[tmp.index('\n') + 1:]
                listScriptExecution[ls] = tmp

        start = time.time()
        threadcurrent = False
        threads = []
        listInThread = []

        stop_message = 'Diagram stopped'

        for execution in listBlockExecution:
            if 'E' in execution:
                self.must_stopped = True
                stop_message = "Diagram stopped by {}".format(execution)

            if self.must_stopped:
                print('{}{}\033[0m'.format(error_color, stop_message))
                break

            start_bb = time.time()

            if 'ThreadOn' in execution:
                threadcurrent = True
                threads = []
                listInThread = []

            elif 'ThreadOff' in execution:
                # progress.setLabelText('['+' , '.join(listInThread)+'] running')
                # progress.setValue(i)

                [thread.start() for thread in threads]
                [listDynamicValue.update(thread.join()) for thread in threads]
                threadcurrent = False
                print(">[{}] --- time : {:.2f} sec".format(' , '.join(listInThread), (time.time() - start_bb)))

            if 'U' in execution:
                outUnit = [lsi for lsi in listNodeValue if execution + ':' in lsi]
                category, classes, *rs = listBlock[execution]
                module = importlib.import_module('NodeEditor.modules.' + category)
                MyClass = getattr(module, classes)
                enters = eval(listBlock[execution][2])
                enters_name, enters_val, *rs = enters
                for id, vl in enumerate(enters_val):
                    if type(vl).__name__ == 'str':
                        try:
                            enters_val[id] = listDynamicValue[vl]
                            if vl in listOut:
                                listOut.remove(vl)
                                if vl not in listOut and ':in' not in vl:
                                    del listDynamicValue[vl]
                        except Exception as err:
                            pass
                            # print('error 1 with {}: {}'.format(execution, err))
                args = dict(zip(enters_name, enters_val))
                if threadcurrent:
                    threads.append(ThreadClass(MyClass, args, outUnit))
                    listInThread.append(execution)
                else:
                    try:
                        a = MyClass(**args)
                        for outs in list(set(outUnit)):
                            tmp = outs[outs.index(':') + 1:]
                            value = getattr(a, tmp)
                            try:
                                listDynamicValue[outs] = value()
                            except Exception as err:
                                listDynamicValue[outs] = value
                            # if self.report_pip:
                            #     Data_analyse(execution, listDynamicValue[outs])
                    except Exception as err:
                        # print('error with 2 {}: {}'.format(execution, err))
                        atxt = "{}stopped by an error".format(error_color)
                        btxt = "> error with {} : {}\033[0m".format(execution, err)
                        print("{}{}".format(atxt, btxt))
                        return

            elif 'P' in execution:
                vl = listBlock[execution][2]
                if vl:
                    try:
                        valToPrint = listDynamicValue[vl]
                    except Exception as e:
                        valToPrint = 'unknown'
                    list_info = printProbe(execution,
                               vl,
                               listBlock[execution][0],
                               listBlock[execution][1],
                               valToPrint,
                               False)
                    col, execution, vl, label, val = list_info.getList()
                        
                    print('{}{} ({}) : {} = {}\033[0m'.format(col,
                                                       execution,
                                                       vl,
                                                       label,
                                                       val))
                    print()
                    try:
                        if vl in listOut:
                            listOut.remove(vl)
                        if vl not in listOut:
                            del listDynamicValue[vl]
                    except Exception as err:
                        pass

            elif 'M' in execution:
                Dyn_Enters = {}
                enters = eval(listModul[execution][2])
                enters_name, enters_val, *rs = enters
                for id, vl in enumerate(enters_val):
                    if type(vl).__name__ == 'str':
                        try:
                            enters_val[id] = listDynamicValue[vl]
                        except Exception as err:
                            pass
                        # try:
                        #     if vl in listOut:
                        #         listOut.remove(vl)
                        #     if vl not in listOut:
                        #         del listDynamicValue[vl]
                        # except:
                        #     pass
                args = dict(zip(enters_name, enters_val))
                path_submod = os.path.dirname(os.path.realpath(__file__))
                module = os.path.join(path_submod, '..', 'submodules',  listModul[execution][1], listModul[execution][0] + '.mod')
                print("module:", module)
                f = open(module, 'r')
                txt = f.read()
                f.close()
                txtSubmod = txt[txt.index('[execution]') + 12: len(txt)]
                ConnectIn = eval(txtSubmod.splitlines()[0])

                for j, conn in enumerate(ConnectIn):
                    Dyn_Enters[conn[0:-1]] = enters_val[j]
                if threadcurrent:
                    threads.append(ThreadSubMod(execution, txtSubmod + txt, Dyn_Enters, self.n_cpu))
                    listInThread.append(execution)
                else:
                    a = self.go_execution(txtSubmod + txt, Dyn_Enters, '')
                    for lst_k, lst_v in a.items():
                        tmp_k = execution + lst_k[lst_k.index(':'):]
                        listDynamicValue[tmp_k] = lst_v

            elif 'F' in execution:
                Dyn_Enters, Dyn_outs = {}, {}
                txt = listForExecution[execution]
                ConnectIn, ConnectOut = eval(txt.splitlines()[0]), eval(txt.splitlines()[5])
                ConnectIn.sort(key=self.alphaNumOrder)

                for conn in ConnectIn:
                    st, ed = conn.split("=")
                    if ':' in ed and '\\' not in ed:
                        Dyn_Enters[st] = listDynamicValue[ed]
                    else:
                        try:
                            Dyn_Enters[st] = eval(ed)
                        except Exception as e:
                            Dyn_Enters[st] = ed
                # for tp in ConnectIn:
                #     if ':in0=' in tp:
                #         firstIndex = tp[0:tp.index('=')]
                #         break
                tp = ConnectIn[0]
                firstIndex = tp[0:tp.index('=')]
                try:
                    lengthEnter = range(len(Dyn_Enters[firstIndex]))
                except Exception as err:
                    print(error_color + "> error : " + execution + " loop has no inputs\033[0m")
                    break

                for lstOut in listOutsInter:
                    try:
                        listDynamicValueSub[lstOut] = listDynamicValue[lstOut]
                    except Exception as err:
                        pass
                        # print('{}{}err\033[0m'.format(error_color, err))

                if 'm' not in execution and 't' not in execution:
                    for ind in lengthEnter:
                        for keyDyn, valDyn in Dyn_Enters.items():
                            try:
                                listDynamicValueSub[keyDyn] = valDyn[ind]
                            except Exception as err:
                                print(error_color + "> error : " + execution + " loop inputs seem to be of different dimension\033[0m")
                                break
                        a = self.go_execution(txt + diagram, listDynamicValueSub, '')
                        for lst_k, lst_v in a.items():
                            tmp_k = execution + lst_k[lst_k.index(':'):]
                            if ind == 0:
                                listDynamicValue[tmp_k] = [lst_v]
                            else:
                                listDynamicValue[tmp_k].append(lst_v)
                elif 'm' in execution:
                    super().__init__()
                    process = []
                    sema = Semaphore(self.n_cpu)
                    pool = Pool(processes=self.n_cpu)

                    try:
                        pool.close()
                        pool.join()
                        pool.terminate()
                    except Exception as err:
                        pass

                    # multiprocessing
                    if ConnectOut:
                        pool = Pool(processes=self.n_cpu)
                        list_args = []
                        for ele in lengthEnter:
                            for keyDyn, valDyn in Dyn_Enters.items():
                                listDynamicValueSub[keyDyn] = valDyn[ele]
                            list_args.append((self.n_cpu, txt + diagram, listDynamicValueSub.copy(), ''))
                        with pool:
                            result = pool.starmap(execution2.methodForMultiprocessing, list_args)
                        i = 0
                        for res in result:
                            for lst_k, lst_v in res.items():
                                tmp_k = execution + lst_k[lst_k.index(':'):]
                                if i == 0:
                                    listDynamicValue[tmp_k] = [lst_v]
                                else:
                                    tmp = listDynamicValue[tmp_k].copy()
                                    tmp.append(lst_v)
                                    listDynamicValue[tmp_k] = tmp
                            i += 1
                    else:
                        for ele in lengthEnter:
                            for keyDyn, valDyn in Dyn_Enters.items():
                                listDynamicValueSub[keyDyn] = valDyn[ele]
                            process_name = 'Diagram_process_' + execution + "_" + str(ele)
                            process.append(Process(target=self.go_execution, name=process_name,
                                                   args=(txt + diagram, listDynamicValueSub.copy(), sema)))
                            process[-1].daemon = True
                            process[-1].start()
                            with open(os.path.join(os.path.expanduser('~'), '.skrypy', 'list_process.tmp'), 'a') as f:
                                f.write('{}{}{}\n'.format(process[-1].pid, ' '*10, process_name))
                        if '*' in execution:
                            for p in process:
                                try:
                                    p.join()
                                except Exception as err:
                                    p.terminate()
                            pool.join()
                        else:
                            pool.terminate()

                elif 't' in execution:
                    if ConnectOut:
                        loop_threads = []
                        result = []
                        # list_args = []
                        for ele in lengthEnter:
                            for keyDyn, valDyn in Dyn_Enters.items():
                                listDynamicValueSub[keyDyn] = valDyn[ele]
                            # list_args = (txt + diagram, listDynamicValueSub.copy(), '', False, '', None)
                            loop_threads.append(ThreadLoop(self.n_cpu, txt + diagram, listDynamicValueSub.copy(), ''))
                        [thread.start() for thread in loop_threads]
                        [result.append(thread.join()) for thread in loop_threads]
                        i = 0
                        for res in result:
                            for lst_k, lst_v in res.items():
                                tmp_k = execution + lst_k[lst_k.index(':'):]
                                if i == 0:
                                    listDynamicValue[tmp_k] = [lst_v]
                                else:
                                    tmp = listDynamicValue[tmp_k].copy()
                                    tmp.append(lst_v)
                                    listDynamicValue[tmp_k] = tmp
                            i += 1
                        # for lst_k, lst_v in result.items():
                        #     tmp_k = execution + lst_k[lst_k.index(':'):]
                        #     if ele == 0:
                        #         listDynamicValue[tmp_k] = [lst_v]
                        #     else:
                        #         listDynamicValue[tmp_k].append(lst_v)
                    else:
                        loop_threads = []
                        for ele in lengthEnter:
                            for keyDyn, valDyn in Dyn_Enters.items():
                                listDynamicValueSub[keyDyn] = valDyn[ele]
                            loop_threads.append(threading.Thread(target=self.go_execution, args=(txt+diagram, listDynamicValueSub.copy(), '')))
                            loop_threads[-1].start()
                        if '*' in execution:
                            [thread.join() for thread in loop_threads]

##############################################################################

            elif 'I' in execution:
                Dyn_Enters = {}
                txtIf = listIfExecution[execution + '-true']
                ConnectIn = eval(txtIf.splitlines()[0])
                for indif in ConnectIn:
                    if execution + ':val' in indif:
                        tmpVal = indif[indif.index('=') + 1:]
                        try:
                            tmpVal = eval(tmpVal)
                        except Exception as e:
                            pass
                        ConnectIn.remove(indif)
                for conn in ConnectIn:
                    st, ed = conn.split("=")
                    if ':' in ed and '\\' not in ed:
                        Dyn_Enters[st] = listDynamicValue[ed]
                    else:
                        try:
                            Dyn_Enters[st] = eval(ed)
                        except Exception as e:
                            Dyn_Enters[st] = ed
                try:
                    if not tmpVal:
                        txtIf = listIfExecution[execution + '-false']
                except Exception as e:
                    pass
                try:
                    if not listDynamicValue[tmpVal]:
                        txtIf = listIfExecution[execution + '-false']
                except Exception as e:
                    pass

                a = self.go_execution(txtIf + diagram, Dyn_Enters, '')
                for lst_k, lst_v in a.items():
                    tmp_k = execution + lst_k[lst_k.index(':'):]
                    listDynamicValue[tmp_k] = lst_v

            elif 'S' in execution:
                try:
                    a = executionScript(execution, listScriptExecution[execution], listDynamicValue)
                    outVals = a.getOutValues()
                    for uj in outVals.keys():
                        listDynamicValue[uj] = outVals[uj]
                except Exception as e:
                    print(error_color + "Diagram Execution " +
                                      execution +
                                      " stopped <br>" +
                                      execution + ' : ' +
                                      str(e) + '\033[0m\n')
            elif 'J' in execution:
                a = executionMacro(execution, listScriptExecution[execution], listDynamicValue)
                outValj = a.getOutValues()
                for uj in outValj.keys():
                    listDynamicValue[uj] = outValj[uj]

            if not threadcurrent and 'Thread' not in execution:
                print("{} --- time : {:.2f} sec\n".format(execution, time.time() - start_bb))

        listValueDynamicToReturn = {}
        for ln in listConnctOut:
            st, ed = ln.split("=")
            if ':' in ed and '\\' not in ed:
                listValueDynamicToReturn[st] = listDynamicValue.copy()[ed]
            else:
                try:
                    listValueDynamicToReturn[st] = eval(ed)
                except Exception as e:
                    listValueDynamicToReturn[st] = ed

        print("> finished\n Total time : {:.3f} sec".format(time.time() - start))

        if sema:
            sema.release()

        # pro.kill()
        return listValueDynamicToReturn.copy()


class executionScript:

    def __init__(self, unitName, txt, listDynamicValue):
        current_module = sys.modules[__name__]
        self.listDynamicValueToReturn = {}
        inputsList = eval(txt[0:txt.index('\n')])
        textScript = '\n'.join(txt.split('\n')[1:-2])
        outputsList = eval(txt.splitlines()[-1])
        code = ''
        for lst in inputsList:
            az = lst.split('=')
            if ':' in az[1]:
                setattr(current_module, az[0], listDynamicValue[az[1]])
            else:
                setattr(current_module, az[0], eval(az[1]))
        code += textScript+'\n'
        for lst in outputsList:
            az = lst.split(':')
            # code = az[1] + '=None\n' + code
            code += 'self.listDynamicValueToReturn["' + lst + '"]=' + az[1] + '\n'
        try:
            d = dict(locals(), **globals())
            exec(code, d, d)
        except Exception as e:
            print("> Diagram Execution " +
                    unitName +
                    " stopped <br>" +
                    unitName + ' : ' +
                    str(e))

    def getOutValues(self):
        return self.listDynamicValueToReturn


class executionMacro:
    def __init__(self, unitName, txt, listDynamicValue):
        self.listDynamicValueToReturn = {}
        inputsList = eval(txt[0:txt.index('\n')])
        textScript = '\n'.join(txt.split('\n')[1:-2])
        outputsList = eval(txt.splitlines()[-1])
        code = ''

        for lst in inputsList:
            az = lst.split('=')
            ispath = ':/' in az[1]
            if ':' in az[1] and not ispath:
                if type(listDynamicValue[az[1]]).__name__ in ['tuple', 'list', 'range']:
                    val = listDynamicValue[az[1]]
                    val = 'newArray(' + ','.join(('\'' + x + '\'') for x in val) + ')'
                    code += az[0] + ' = ' + val
                elif type(listDynamicValue[az[1]]).__name__ in 'str':
                    code += az[0] + ' = "' + str(listDynamicValue[az[1]]) + '"'
                elif (type(listDynamicValue[az[1]]).__name__ in ['bool']):
                    val = listDynamicValue[az[1]]
                    val == 1 if val == 'True' else 0
                elif ('float' in type(listDynamicValue[az[1]]).__name__ or
                      'int' in type(listDynamicValue[az[1]]).__name__):
                    code += az[0] + ' = ' + str(listDynamicValue[az[1]])
                elif (type(listDynamicValue[az[1]]).__name__ in ['array']):
                    code += az[0] + ' = ' + str(listDynamicValue[az[1]])
                elif type(listDynamicValue[az[1]]).__name__ in ['memmap']:
                    code += az[0] + ' = ' + str(listDynamicValue[az[1]].tolist())
                elif type(listDynamicValue[az[1]]).__name__ in ['ndarray']:
                    code += az[0] + ' = ' + str(listDynamicValue[az[1]].tolist())
                elif type(listDynamicValue[az[1]]).__name__ in ['NoneType']:
                    code += az[0] + ' = None'
            else:
                code += lst
            code += ';\n'
        code += textScript+'\n'
        self.listDynamicValueToReturn[outputsList[0]] = '""' + code + '""'

    def getOutValues(self):
        return self.listDynamicValueToReturn


class ThreadClass(threading.Thread):

    def __init__(self, classs, inp, outp):
        threading.Thread.__init__(self)
        self.classs = classs
        self.inp = inp
        self.outp = outp

    def run(self):
        self._return = {}
        if self.inp:
            a = self.classs(**self.inp)
        else:
            a = self.classs()
        if self.outp:
            for el in self.outp:
                unit = el[0:el.index(':')]
                val = el[el.index(':') + 1:len(el)]
                value = getattr(a, val)
                try:
                    self._return[el] = value()
                except Exception as e:
                    self._return[el] = value

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return


class ThreadLoop(threading.Thread):

    def __init__(self, n_cpu, *args):
        threading.Thread.__init__(self)
        self.args = args
        self.n_cpu = n_cpu

    def run(self):
        self._return = {}
        a = execution2(self.n_cpu).go_execution(*self.args)
        self._return = a
        # for lst_k, lst_v in a.items():
        #     tmp_k = self.execution + lst_k[lst_k.index(':'):]
        #     self._return[tmp_k] = lst_v

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return


class ThreadSubMod(threading.Thread):

    def __init__(self, execution, txt, Dyn_Enters, n_cpu):
        threading.Thread.__init__(self)
        self.execution = execution
        self.txt = txt
        self.Dyn_Enters = Dyn_Enters
        self.n_cpu = n_cpu

    def run(self):
        self._return = {}
        a = execution2(self.n_cpu).go_execution(self.txt, self.Dyn_Enters, '')
        for lst_k, lst_v in a.items():
            tmp_k = self.execution + lst_k[lst_k.index(':'):]
            self._return[tmp_k] = lst_v

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return
