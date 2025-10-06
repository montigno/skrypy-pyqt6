##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

from NodeEditor.python.tools import GetValueInBrackets, ReorderList, eval_type
import ast
import os


class analyze2:

    def __init__(self, txt, mode):

        self.mode = mode
        self.txtInfo = ''
        self.diagram = txt.splitlines()
        self.load_dict()

    def load_dict(self):

        self.textExecution = ''
        ConnectIn, ConnectOut = {}, {}
        listIt, listBlInLoop = [], []
        self.listNd, self.listFo, self.listIf = {}, {}, {}
        self.listCt, self.listBl, self.listSm = {}, {}, {}
        self.listPr, self.listSt, self.list_loop_recursive = {}, {}, {}
        self.interlinks_node = {}
        insource = False
        tmpKeyScript = ''
        tmpValScript = ''

        for line in self.diagram:
            if line[0:5] == 'probe' and 'RectF' in line:
                args = ["probe", "label", "format", "RectF"]
                unit, label, form, pos = GetValueInBrackets(line, args).getValues()
                listIt.append(unit)
                self.listPr[unit] = (form, label, "")

            elif line[0:5] == 'block' and 'RectF' in line:
                args = ["block", "category", "class", "valInputs", "RectF"]
                unit, cat, classs, Vinput, pos = GetValueInBrackets(line, args).getValues()
                listIt.append(unit)
                self.listBl[unit] = (cat, classs, Vinput)

            elif line[0:7] == 'loopFor' and 'RectF' in line:
                args = ["loopFor", "inputs", "outputs", "listItems", "RectF"]
                unit, inp, outp, listItems, pos = GetValueInBrackets(line, args).getValues()
                self.listFo[unit] = (unit, eval(inp), eval(outp), eval(listItems))
                listIt.append(unit)
                listBlInLoop.extend(eval(listItems))

            elif line[0:6] == 'loopIf' and 'RectF' in line:
                args = ["loopIf", "inputs", "outputs", "listItems", "RectF"]
                unit, inp, outp, listItems, pos = GetValueInBrackets(line, args).getValues()
                tmp_listIt = eval(listItems)
                self.listIf[unit] = (unit, eval(inp), eval(outp), tmp_listIt)
                listIt.append(unit)
                listBlInLoop.extend(tmp_listIt[0])
                listBlInLoop.extend(tmp_listIt[1])

            elif line[0:6] == 'submod' and 'RectF' in line:
                args = ["submod", "nameMod", "catMod", "valInputs", "RectF"]
                unit, nameMod, catMod, Vinput, pos = GetValueInBrackets(line, args).getValues()
                listIt.append(unit)
                self.listBl[unit] = (nameMod, catMod, Vinput)
                path_submod = os.path.dirname(os.path.realpath(__file__))
                file = os.path.join(path_submod,
                                    '..',
                                    'submodules',
                                    catMod,
                                    nameMod + '.mod')
                f = open(file, 'r')
                txt = f.read()
                f.close()
                txt = txt[txt.index('[execution]') + 12:len(txt)]
                tmp1 = ''
                for i, ln in enumerate(txt.splitlines()):
                    if i < 6:
                        tmp1 += ln + '\n'
                self.listSm[unit] = tmp1

            elif line[0:6] == 'script' and "RectF" in line:
                args = ["script", "title", "inputs", "outputs", "code", "RectF"]
                unit, tit, inp, outp, code, pos = GetValueInBrackets(line, args).getValues()
                inp, outp = "["+inp+"]", "["+outp+"]"
                listIt.append(unit)

            elif line[0:4] == 'link' and 'node' in line:
                args = ["link", "node"]
                nameNode, line = GetValueInBrackets(line, args).getValues()
                link_cur = line.replace('#Node#', ':').split(':')
                self.listNd[nameNode] = link_cur

            elif line[0:5] == 'connt' and 'RectF' in line:
                args = ["connt", "name", "type", "format", "valOut", "RectF"]
                unit, nameConn, typ, form, Vinput, pos = GetValueInBrackets(line, args).getValues()
                if 'in' in typ:
                    ConnectIn[unit] = (nameConn, eval(pos)[1])
                else:
                    ConnectOut[unit] = (nameConn, eval(pos)[1])

            elif line[0:8] == 'constant' and 'RectF' in line:
                args = ["constant", "value", "format", "label", "RectF"]
                unit, vout, fort, lab, pos = GetValueInBrackets(line, args).getValues()
                if fort == 'list_str':
                    vout = eval(vout)
                    tmp = []
                    for lstVal in vout:
                        if '*' in lstVal[-1]:
                            tmp.append(lstVal[0:-1])
                    vout = tmp
                elif fort == 'list_path':
                    vout = eval(vout)
                    # vout = vout[1:-1].split('\\n')
                else:
                    vout = eval_type(vout, fort).getVout()
                self.listCt[unit] = (vout, fort)

            elif line[0:7] == 'cluster' and 'RectF' in line:
                args = ["cluster", "value", "format", "label", "RectF"]
                unit, vout, fort, lab, pos = GetValueInBrackets(line, args).getValues()
                vout = eval_type(vout, fort).getVout()
                self.listCt[unit] = (vout, fort)

            elif line[0:8] == 'stopexec' and 'RectF' in line:
                args = ["stopexec", "RectF"]
                unit, pos = GetValueInBrackets(line, args).getValues()
                pos = eval(pos)
                listIt.append(unit)

        self.assign_variables()
        connects = self.connection_inputs_ouputs(ConnectIn, ConnectOut)
        self.interlinks, self.interlinks_node = self.get_inter_link()
        # print('self.interlinks_node', self.interlinks, self.interlinks_node)
        self.textExecution += connects[0] + '\n'
        taks_ord = self.tasks_order(self.listNd, listIt, listBlInLoop, self.mode, "main: ")
        self.textExecution += str(taks_ord[0]) + '\n'
        dict_bl_sm = self.dict_block_submod(taks_ord[0])
        self.textExecution += dict_bl_sm[0] + '\n'
        self.textExecution += str(taks_ord[1]) + '\n'
        self.textExecution += dict_bl_sm[1] + '\n'
        self.textExecution += connects[1] + '\n'
        self.analyze_loop(taks_ord[0])
        self.textExecution += self.analyze_submod()
        self.textExecution += '[interlinks]\n'
        self.textExecution += self.interlinks + '\n'

    def assign_variables(self):
        for klan, vlan in self.listNd.items():
            tmp_klan = 'Node('+klan+')'
            if 'U' in vlan[2] or 'M' in vlan[2]:
                if 'A' in vlan[0]:
                    tmp_val = self.listCt[vlan[0]][0]
                else:
                    tmp_val = vlan[0] + ':' + vlan[1]
                a, b, c = self.listBl[vlan[2]]
                x, tmp_vlan, y, z = eval(c)
                vlan_new = []
                for w in tmp_vlan:
                    if w == tmp_klan:
                        vlan_new.append(tmp_val)
                    else:
                        vlan_new.append(w)
                self.listBl[vlan[2]] = (a, b, str((x, vlan_new, y, z)))
            elif 'P' in vlan[2]:
                if 'A' in vlan[0]:
                    tmp_val = self.listCt[vlan[0]][0]
                else:
                    tmp_val = vlan[0] + ':' + vlan[1]
                a, b, c = self.listPr[vlan[2]]
                self.listBl[vlan[2]] = (a, b, tmp_val)

    def connection_inputs_ouputs(self, CnIn, CnOut):

        connect_in, connect_out = "[]", "[]"

        if CnIn:
            connect_in = []
            sorted_by_pos_In = sorted(CnIn.items(),
                                      key=lambda kv: kv[1][1])
            for elem in sorted_by_pos_In:
                connect_in.append(elem[0] + ":" + elem[1][0] + "=")

        if CnOut:
            connect_out = []
            sorted_by_pos_Out = sorted(CnOut.items(),
                                       key=lambda kv: kv[1][1])
            for elem in sorted_by_pos_Out:
                for lan in self.listNd.values():
                    if lan[2] == elem[0]:
                        connect_out.append("{}:{}={}:{}".format(elem[0], elem[1][0], lan[0], lan[1]))

        return str(connect_in), str(connect_out)

    def connection_loopfor(self, unit):

        tunnel_in, tunnel_out = [], []
        for klan, vlan in self.listNd.items():
            if unit == vlan[2]:
                if 'A' in vlan[0]:
                    if 'in' in vlan[3]:
                        tunnel_in.append(vlan[2] + ':' + vlan[3] + '=' + str(self.listCt[vlan[0]][0]))
                    else:
                        tunnel_out.append(vlan[2] + ':' + vlan[3] + '=' + str(self.listCt[vlan[0]][0]))
                else:
                    if 'in' in vlan[3]:
                        tunnel_in.append(vlan[2] + ':' + vlan[3] + '=' + vlan[0] + ':' + vlan[1])
                    else:
                        tunnel_out.append(vlan[2] + ':' + vlan[3] + '=' + vlan[0] + ':' + vlan[1])

        return str(tunnel_in), str(tunnel_out)

    def connection_if(self, unit, list_it):

        tunnel_in, tunnel_out = [], []
        for klan, vlan in self.listNd.items():
            if unit == vlan[2]:
                if 'A' in vlan[0] and vlan[0] in list_it:
                    tunnel_out.append(vlan[2] + ':' + vlan[3] + '=' + str(self.listCt[vlan[0]][0]))
                elif vlan[0] in list_it or klan in list_it:
                    tunnel_out.append(vlan[2] + ':' + vlan[3] + '=' + vlan[0] + ':' + vlan[1])
                elif 'in' in vlan[3] or 'val' in vlan[3]:
                    if 'A' in vlan[0]:
                        tunnel_in.append(vlan[2] + ':' + vlan[3] + '=' + str(self.listCt[vlan[0]][0]))
                    else:
                        tunnel_in.append(vlan[2] + ':' + vlan[3] + '=' + vlan[0] + ':' + vlan[1])
#                 elif vlan[0] == vlan[2]:
#                     tunnel_out.append(vlan[2] + ':' + vlan[3] + '=' + vlan[0] + ':' + vlan[1])

        return str(tunnel_in), str(tunnel_out)

    def tasks_order(self, listNd, listIt, listBlInLoop, thrd, part):
        tasks_list = []

        if listIt:
            listBlInLoop = [i for i in listBlInLoop if 'A' not in i]
            listIt = [i for i in listIt if 'A' not in i]

            startBlocks, endBlocks, centralBlocks = [], [], []

            for key_Nd, val_Nd in listNd.items():
                if 'A' in val_Nd[0] or 'C' in val_Nd[0]:
                    pass
                elif 'C' in val_Nd[2]:
                    pass
                elif 'F' in val_Nd[2] or 'I' in val_Nd[2]:
                    if 'out' not in val_Nd[3]:
                        startBlocks.append(val_Nd[0])
                        endBlocks.append(val_Nd[2])
                        ################################################
                elif 'F' in val_Nd[0] or 'I' in val_Nd[0]:
                    if 'in' not in val_Nd[1]:
                        startBlocks.append(val_Nd[0])
                        endBlocks.append(val_Nd[2])
                else:
                    startBlocks.append(val_Nd[0])
                    endBlocks.append(val_Nd[2])

            startBlocks = list(set(startBlocks))  # delete doublons
            endBlocks = list(set(endBlocks))  # delete doublons
            listIt = (list(set(listIt) - set(startBlocks)))
            listIt = (list(set(listIt) - set(endBlocks)))
            listIt = (list(set(listIt) - set(listBlInLoop)))
            startBlocks = (list(set(startBlocks) - set(listBlInLoop)))
            endBlocks = (list(set(endBlocks) - set(listBlInLoop)))
            startBlocks.extend(listIt)  # if listIt not empty

            tmp = startBlocks
            startBlocks = (list(set(startBlocks) - set(endBlocks)))
            endBlocks = (list(set(endBlocks) - set(tmp)))
            centralBlocks = (list(set(tmp) - set(startBlocks)))

            startBlocks = ReorderList(startBlocks).getNewList()
            endBlocks = ReorderList(endBlocks).getNewList()

#             print('startBlocks 1 :', startBlocks)
#             print('centralBlocks 1 :', centralBlocks)
#             print('endBlocks 1 :', endBlocks)

            tmpNeed = {}
            # check for inter link between block and forloop
            threadOk = True
            tmp_startBlocks = startBlocks.copy()
            tmp_endblocks = endBlocks.copy()
            for it in startBlocks:
                if it in self.interlinks_node.keys():
                    tmpblc = self.interlinks_node[it]
                    tmpblc = [x for x in tmpblc if 'C' not in x and x in startBlocks or x in endBlocks or x in centralBlocks]
                    # if tmpblc not in tmp_startBlocks:
                    if not all(x in tmp_startBlocks for x in tmpblc):
                        tmp_startBlocks.remove(it)
                        centralBlocks.append(it)
                        tmpNeed[it] = tmpblc
                        for tmpls in tmpblc:
                            if tmpls in endBlocks and tmpls in tmp_endblocks:
                                tmp_endblocks.remove(tmpls)
                                centralBlocks.append(tmpls)
                    else:
                        tmp_startBlocks.append(tmp_startBlocks.pop(tmp_startBlocks.index(it)))
                        threadOk = False

            # if value list same as the key, delete it
            for k_t, v_t in tmpNeed.items():
                if k_t in v_t:
                    tmpu = v_t
                    tmpu.remove(k_t)
                    tmpNeed[k_t] = tmpu

            startBlocks = tmp_startBlocks.copy()
            endBlocks = tmp_endblocks.copy()

            if thrd[0]:
                if len(startBlocks) > 1 and threadOk:
                    startBlocks.insert(0, 'ThreadOn')
                    startBlocks.append('ThreadOff')
                if len(endBlocks) > 1:
                    endBlocks.insert(0, 'ThreadOn')
                    endBlocks.append('ThreadOff')

            # print('tmpNeed 1 :', tmpNeed)
            # print('startBlocks 2 :', startBlocks)
            # print('centralBlocks 2 :', centralBlocks)
            # print('endBlocks 2 :', endBlocks)

            tasks_list.extend(startBlocks)

            if len(centralBlocks) > 1:
                for key_Nd, val_Nd in listNd.items():
                    if 'A' not in val_Nd[0] and 'C' not in val_Nd[0] and val_Nd[0] != val_Nd[2]:
                        if val_Nd[0] in startBlocks or val_Nd[0] in centralBlocks:
                            if val_Nd[2] in centralBlocks:
                                tmpVal = []
                                tmpVal.append(val_Nd[0])
                                if val_Nd[2] in tmpNeed.keys():
                                    tmpVal.extend(tmpNeed[val_Nd[2]])
                                tmpVal = list(set(tmpVal))
                                tmpNeed[val_Nd[2]] = tmpVal
#                 print('tmpNeed 2 :', tmpNeed)
                tmpNeedIter = tmpNeed.copy()
                while len(tmpNeedIter) != 0:
                    tmpIt = []
                    for key_need, val_need in tmpNeed.items():
                        if key_need in tmpNeedIter.keys():
                            if all(x in tasks_list for x in val_need):
                                tmpIt.append(key_need)
                                del tmpNeedIter[key_need]

                    # print('tmpIt :', tmpIt, tmpNeedIter)

                    # check interlinks bloc #############
                    tmpIttmp = tmpIt.copy()
                    for it in tmpIt:
                        if it in self.interlinks_node.keys():
                            for lsbl in self.interlinks_node[it]:
                                if lsbl in tmpIt:
                                    tasks_list.append(lsbl)
                                    tmpIttmp.remove(lsbl)
                    tmpIt = tmpIttmp
                    #####################################
                    if len(tmpIt) > 1 and thrd[1]:
                        tasks_list.append("ThreadOn")
                        tasks_list.extend(tmpIt)
                        tasks_list.append("ThreadOff")
                    else:
                        tasks_list.extend(tmpIt)
            else:
                tasks_list.extend(centralBlocks)
            tasks_list.extend(endBlocks)

        tasks_list = [x for x in tasks_list if "N" not in x]

        outs_list = []
        for klan, vlan in self.listNd.items():
            if 'F' not in vlan[0] and 'I' not in vlan[0]:
                if vlan[0] in tasks_list:
                    outs_list.append(vlan[0] + ':' + vlan[1])
            elif 'out' in vlan[1] and vlan[0] in tasks_list:
                outs_list.append(vlan[0] + ':' + vlan[1])
            elif 'in' in vlan[1] and vlan[2] in tasks_list:
                outs_list.append(vlan[0] + ':' + vlan[1])
            elif vlan[0] == vlan[2] and vlan[0] not in tasks_list:
                outs_list.append(vlan[0] + ':' + vlan[1])

        self.txtInfo += part + str(tasks_list) + "<br>"
        self.txtInfo = self.txtInfo.replace("'", "")

        return tasks_list, outs_list

    def dict_block_submod(self, tasks):
        dict_bl, dict_sm = {}, {}

        for lst in tasks:
            if 'U' in lst or 'P' in lst:
                try:
                    dict_bl[lst] = self.listBl[lst]
                except Exception as err:
                    dict_bl[lst] = self.listPr[lst]
            if 'M' in lst:
                dict_sm[lst] = self.listBl[lst]

        return str(dict_bl), str(dict_sm)

    def analyze_loop(self, tmpGen):

        for lst_bl in tmpGen:
            tmp_it = []
            if 'F' in lst_bl:
                tmp_Nd = {}
                tmp_it = self.listFo[lst_bl][3]
                for key_Nd, val_Nd in self.listNd.items():
                    if 'A' not in val_Nd[0]:
                        if val_Nd[0] in tmp_it and val_Nd[2] in tmp_it:
                            tmp_Nd[key_Nd] = val_Nd
                self.textExecution += ('[loopfor {}]'.format(lst_bl)) + '\n'
                conn_loop = self.connection_loopfor(lst_bl)
                self.textExecution += conn_loop[0] + '\n'
                taks_ord = self.tasks_order(tmp_Nd, tmp_it, [], [True, True], lst_bl+": ")
                self.textExecution += str(taks_ord[0]) + '\n'
                dict_bl_sm = self.dict_block_submod(taks_ord[0])
                self.textExecution += dict_bl_sm[0] + '\n'
                self.textExecution += str(taks_ord[1]) + '\n'
                self.textExecution += dict_bl_sm[1] + '\n'
                self.textExecution += conn_loop[1] + '\n'
                self.analyze_loop(taks_ord[0])
            elif 'I' in lst_bl:
                tmp_Nd = {}
                tmp_it = self.listIf[lst_bl][3][0]
#                 tmp_it = [x for x in tmp_it if "N" not in x]
                for key_Nd, val_Nd in self.listNd.items():
                    if 'A' not in val_Nd[0]:
                        if val_Nd[0] in tmp_it and val_Nd[2] in tmp_it:
                            tmp_Nd[key_Nd] = val_Nd
                self.textExecution += ('[loopif {} True]'.format(lst_bl)) + '\n'
                conn_loop = self.connection_if(lst_bl, tmp_it)
                self.textExecution += conn_loop[0] + '\n'
                taks_ord = self.tasks_order(tmp_Nd, tmp_it, [], [True, True], lst_bl+" True: ")
                self.textExecution += str(taks_ord[0]) + '\n'
                dict_bl_sm = self.dict_block_submod(taks_ord[0])
                self.textExecution += dict_bl_sm[0] + '\n'
                self.textExecution += str(taks_ord[1]) + '\n'
                self.textExecution += dict_bl_sm[1] + '\n'
                self.textExecution += conn_loop[1] + '\n'
                self.analyze_loop(taks_ord[0])

                tmp_Nd = {}
                tmp_it = self.listIf[lst_bl][3][1]
#                 tmp_it = [x for x in tmp_it if "N" not in x]
                for key_Nd, val_Nd in self.listNd.items():
                    if 'A' not in val_Nd[0]:
                        if val_Nd[0] in tmp_it and val_Nd[2] in tmp_it:
                            tmp_Nd[key_Nd] = val_Nd
                self.textExecution += ('[loopif {} False]'.format(lst_bl)) + '\n'
                conn_loop = self.connection_if(lst_bl, tmp_it)
                self.textExecution += conn_loop[0] + '\n'
                taks_ord = self.tasks_order(tmp_Nd, tmp_it, [], [True, True], lst_bl+" False: ")
                self.textExecution += str(taks_ord[0]) + '\n'
                dict_bl_sm = self.dict_block_submod(taks_ord[0])
                self.textExecution += dict_bl_sm[0] + '\n'
                self.textExecution += str(taks_ord[1]) + '\n'
                self.textExecution += dict_bl_sm[1] + '\n'
                self.textExecution += conn_loop[1] + '\n'
                self.analyze_loop(taks_ord[0])

    def analyze_submod(self):
        txt_submod = ''
        for k_Sm, v_Sm in self.listSm.items():
            listConnctIn, listConnctOut = [], []
            txt_splitline = v_Sm.splitlines()
            listConnctIn = ast.literal_eval(txt_splitline[0])
            listConnctOut = ast.literal_eval(txt_splitline[5])
            list_in_out = eval(self.listBl[k_Sm][2])
            for input in list_in_out[0]:
                idx = [listConnctIn.index(x) for x in listConnctIn if input in x][0]
                listConnctIn[idx] = listConnctIn[idx] + str(list_in_out[1][idx])
            for i, ouput in enumerate(listConnctOut):
                listConnctOut[i] = k_Sm + listConnctOut[i][listConnctOut[i].index(':'):]
            txt_submod += '[submod {}]\n'.format(k_Sm)
            txt_submod += str(listConnctIn) + '\n'
            txt_submod += '\n'.join(txt_splitline[1:5]) + '\n'
            txt_submod += str(listConnctOut) + '\n'
        return txt_submod

    def get_inter_link(self):
        list_outs_inter = []
        list_blocks_loop_interconnected = {}
        for klan, vlan in self.listNd.items():
            # print('klan, vlan : ', klan, vlan)
            # if ('A' not in vlan[0] and
            #     'F' not in vlan[0] and
            #     'F' not in vlan[2]):
            if ('A' not in vlan[0] and
                    'F' not in vlan[0]):
                for kfor, vfor in self.listFo.items():
                    # print('    kfor, vfor 1: ', kfor, vfor)
                    for elem in vfor[3]:
                        if 'F' in elem:
                            try:
                                if elem not in self.list_loop_recursive[kfor]:
                                    self.list_loop_recursive[kfor].append(elem)
                            except Exception as err:
                                self.list_loop_recursive[kfor] = [elem]
                    if vlan[0] in vfor[3] and vlan[2] in vfor[3]:
                        pass
                    elif vlan[2] in vfor[3]:
                        list_outs_inter.append(vlan[0] + ':' + vlan[1])
                        nl = self.search_inter_blocks_through_loop(kfor, vlan[0])
                        if nl in list_blocks_loop_interconnected:
                            tmp = list_blocks_loop_interconnected[nl]
                            tmp.append(vlan[0])
                            list_blocks_loop_interconnected[nl]
                        else:
                            list_blocks_loop_interconnected[nl] = [vlan[0]]
            if 'F' in vlan[0] and 'in' in vlan[1]:
                for kfor, vfor in self.listFo.items():
                    # print('    kfor, vfor 2: ', kfor, vfor)
                    for elem in vfor[3]:
                        if 'F' in elem:
                            try:
                                if elem not in self.list_loop_recursive[kfor]:
                                    self.list_loop_recursive[kfor].append(elem)
                            except Exception as err:
                                self.list_loop_recursive[kfor] = [elem]
                    if vlan[0] in vfor[0] and vlan[2] not in vfor[3]:
                        list_outs_inter.append(vlan[0] + ':' + vlan[1])
                        nl = self.search_inter_blocks_through_loop(kfor, vlan[0])
                        if nl in list_blocks_loop_interconnected:
                            tmp = list_blocks_loop_interconnected[nl]
                            tmp.append(vlan[0])
                            list_blocks_loop_interconnected[nl]
                        else:
                            list_blocks_loop_interconnected[nl] = [vlan[0]]

        return str(list(set(list_outs_inter))), list_blocks_loop_interconnected

    def search_inter_blocks_through_loop(self, loopItem, block1):
        main = False
        newloop = loopItem
        while not main:
            find = False
            for kfor, vfor in self.listFo.items():
                if newloop in vfor[3] and block1 not in vfor[3]:
                    newloop = kfor
                    find = True
            if not find:
                main = True
        return newloop

    def get_analyze(self, textEditor):
        textEditor.addTxt("<span style=\" \
                           font-size:12pt; \
                           font-weight:600; \
                           color:#000000;\" >Sequence of tasks :</span>")
        textEditor.addTxt("<span style=\" \
                           font-size:10pt; \
                           font-weight:600; \
                           color:#000000;\" >" + self.txtInfo + "</span>")
        return self.textExecution
