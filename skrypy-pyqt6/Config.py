##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################

'''
Created on 2023/12/26
@author: omontigon
'''

import os
import yaml


class Config():

    EMPTY_FIELDS = {'template': {'host_name': 'user@host_name',
                                 'skrypy_server_directory': '/home/user_name/Applications/Skrypy_venv_directory',
                                 'server_workspace_directory': '/home/user_name/tmp',
                                 'cpu_number': '4',
                                 'X11_forwarding': False,
                                 'pre_execution_command': 'conda activate foo',
                                 'fd_command': '',
                                 'fk_command': ''
                                 }}

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.config_path = os.path.join(dir_path, 'config.yml')
        self.config = self.loadConfig()
        self.path_home = os.path.expanduser('~')
        self.config_path_user = os.path.join(self.path_home, '.skrypy', 'config_user.yml')
        self.config_user = self.loadConfigUser()
        self.env_param_path = os.path.join(self.path_home, '.skrypy', 'env_parameters.txt')
        self.loadEnvDiagram()
        self.servers_list = os.path.join(self.path_home, '.skrypy', 'list_servers.yml')
        self.loadServerFile()

    def loadConfig(self):
        with open(self.config_path, 'r') as stream:
            try:
                return yaml.load(stream, yaml.FullLoader)
            except yaml.YAMLError as exc:
                print(exc)

    def saveConfig(self):
        with open(self.config_path, 'w', encoding='utf8') as configfile:
            yaml.dump(self.config,
                      configfile,
                      default_flow_style=False,
                      allow_unicode=True)

    def loadConfigUser(self):
        if not os.path.exists(self.config_path_user):
            os.makedirs(os.path.dirname(self.config_path_user), exist_ok=True)
            data = dict(diagram_report=False, paths=dict(diagrams='', histories='', run_at_start=''))
            with open(self.config_path_user, 'w') as outfile:
                yaml.dump(data, outfile, default_flow_style=False)
        with open(self.config_path_user, 'r') as stream:
            try:
                return yaml.load(stream, yaml.FullLoader)
            except yaml.YAMLError as exc:
                print(exc)

    def saveConfigUser(self):
        with open(self.config_path_user, 'w', encoding='utf8') as configfile:
            yaml.dump(self.config_user,
                      configfile,
                      default_flow_style=False,
                      allow_unicode=True)

    def loadEnvDiagram(self):
        if not os.path.exists(self.env_param_path):
            f = open(self.env_param_path, 'w+')

    def loadServerFile(self):
        empty_fields = {}
        if not os.path.exists(self.servers_list):
            self.loadEmptyFields()
        else:
            with open(self.servers_list, 'r', encoding='utf8') as stream:
                dicts = yaml.load(stream, yaml.FullLoader)
                if not bool(dicts):
                    self.loadEmptyFields()

    def loadEmptyFields(self):
        with open(self.servers_list, 'w') as stream:
            yaml.dump(self.EMPTY_FIELDS, stream, default_flow_style=False)

    def getEnvDiagram(self):
        return self.env_param_path

    def getServersList(self):
        return self.servers_list

    def getVersion(self):
        return self.config['version']

    def getPathLibraries(self):
        return self.config['packages']

    def getCpuCount(self):
        return self.config["cpu_count"]

    def setCpuCount(self, count):
        self.config["cpu_count"] = count
        self.saveConfig()

    def getPathDiagrams(self):
        diag = self.config_user["paths"]["diagrams"]
        newDiag = []
        if diag:
            for d in diag:
                if os.path.exists(d):
                    newDiag.append(d)
        self.setPathDiagrams(newDiag)
        return newDiag

    def setPathDiagrams(self, diag):
        self.config_user["paths"]["diagrams"] = diag
        self.saveConfigUser()

    def getPathHistories(self):
        hist = self.config_user["paths"]["histories"]
        newHist = []
        if hist:
            for h in hist:
                if os.path.exists(h):
                    newHist.append(h)
        self.setPathHistories(newHist)
        return newHist

    def setPathHistories(self, hist):
        self.config_user["paths"]["histories"] = hist
        self.saveConfigUser()

    def getDiagramReport(self):
        return self.config_user["diagram_report"]

    def setDiagramReport(self, state):
        self.config_user["diagram_report"] = state
        self.saveConfigUser()

    def getRunStart(self):
        start_run = self.config_user["paths"]["run_at_start"]
        newStart = []
        if start_run:
            for s in start_run:
                if os.path.exists(s):
                    newStart.append(s)
        return newStart

    def setRunStart(self, start_run):
        self.config_user["paths"]["run_at_start:"] = start_run
        self.saveConfigUser()

    # def getShowGrid(self):
    #     return self.config_user["show_grid"]
    #
    # def setShowGrid(self, state):
    #     self.config_user["show_grid"] = state
    #     self.saveConfigUser()
