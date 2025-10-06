##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

from glob import glob
import os
import re


class getlistSubModules:

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = os.path.dirname(dir_path)
        submodules = os.path.join(dir_path, 'submodules')

        self.category = []
        list_dir = []
        self.listSubMod = {}
        self.lstdir = {}

        list_dir = [f for f in glob(submodules + "/*") if os.path.isdir(f)]
        for namedir in list_dir:
            dir_alone = os.path.basename(os.path.normpath(namedir))
            self.lstdir[dir_alone] = []
            tmpv = []
            for namefile in os.listdir(namedir):
                if namefile.endswith(".mod"):
                    file = os.path.join(namedir, namefile)
                    submod_name = os.path.basename(file[0:file.index('.mod')])
                    self.listSubMod[submod_name] = self.readFile(file, dir_alone)
                    tmpv.append(submod_name)
            self.lstdir[dir_alone] = tmpv

    def readFile(self, file, dir):

        f = open(file, 'r')
        txt = f.readlines()
        f.close()

        txt.reverse()
        self.inputs, self.outputs = [], []

        listlabelIn, listlabelOut = [], []
        listVal, listForm = [], []

        listConnectInPos, listConnectOutPos = {}, {}
        tmpIn, tmpOut = {}, {}
        tmpVal, tmpForm = {}, {}

        for line in txt:
            if line[0:5] == 'connt':
                nameConn = re.search(r"\[([A-Za-z0-9_]+)\]", line).group(1)
                line = line[line.index('name=') + 6:len(line)]
                label = line[0:line.index(']')]
                line = line[line.index('type=') + 6:len(line)]
                typ = line[0:line.index(']')]
                line = line[line.index('format=') + 8:len(line)]
                form = line[0:line.index(']')]
                try:
                    line = line[line.index('valOut=') + 8:len(line)]
                    Vinput = line[0:line.index('] ')]
                except Exception as e:
                    Vinput = ''
                line = line[line.index('RectF=') + 7:len(line)]
                line = line[line.index(',') + 2:len(line)]
                posY = line[0:line.index(',')]

                if typ == 'in':
                    tmpIn[nameConn] = label
                    tmpVal[nameConn] = Vinput
                    listConnectInPos[nameConn] = posY
                else:
                    tmpOut[nameConn] = label
                    tmpForm[nameConn] = form
                    listConnectOutPos[nameConn] = posY

        if tmpIn:
            sorted_by_pos_In = sorted(listConnectInPos.items(),
                                      key=lambda kv: eval(kv[1]))
            for elem in sorted_by_pos_In:
                listlabelIn.append(tmpIn[elem[0]])
                if 'enumerate' in tmpVal[elem[0]]:
                    listVal.append(tmpVal[elem[0]])
                else:
                    try:
                        listVal.append(eval(tmpVal[elem[0]]))
                    except Exception as e:
                        listVal.append(tmpVal[elem[0]])

        if tmpOut:
            sorted_by_pos_Out = sorted(listConnectOutPos.items(),
                                       key=lambda kv: eval(kv[1]))
            for elem in sorted_by_pos_Out:
                listlabelOut.append(tmpOut[elem[0]])
                listForm.append(tmpForm[elem[0]])

        listg = (listlabelIn, listVal, listlabelOut, listForm, dir)
        return listg

    def listSubModules(self):
        return self.listSubMod

    def listDir(self):
        return self.lstdir
