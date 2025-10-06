import os
import yaml
import subprocess
import inspect
from threading import Timer

from . import Config
from . import set_dph
from . import get_dph

from PyQt6.QtWidgets import QComboBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, \
    QLineEdit, QTextEdit, QPushButton, QDialogButtonBox, QCheckBox, QMessageBox
from PyQt6.QtCore import Qt


class servers_window(QDialog):

    def __init__(self, config, clust, parent=None):
        super(servers_window, self).__init__(parent)
        self.config = config
        self.clust = clust
        self.server_yml = Config().getServersList()
        self.getServersInfo()

    def field_changed(self):
        self.setWindowTitle('Clusters configuration*')

    def getServersInfo(self):

        self.server_param = []
        dicts = {}

        with open(self.server_yml, 'r', encoding='utf8') as stream:
            dicts = yaml.load(stream, yaml.FullLoader)
            if not self.clust:
                self.mainWindow(dicts)
            else:
                self.getClusterParam(dicts[self.clust])

    def getClusterParam(self, clust):
        try:
            tmpA = clust['fd_command']
            tmpB = clust['fk_command']
            tmppd = get_dph(tmpA, tmpB).get_ushn()
        except Exception as err:
            print('error to open cluster config:', err)
            tmppd = ''
        self.server_param = [clust['host_name'],
                             clust['skrypy_server_directory'],
                             clust['server_workspace_directory'],
                             str(clust['cpu_number']),
                             bool(clust['X11_forwarding']),
                             clust['pre_execution_command'],
                             tmppd,
                             self.clust]

    def mainWindow(self, list_config):

        self.list_config = list_config

        # self.setWindowTitle('Clusters configuration')
        # self.setWindowFlags(self.windowFlags() &
        #                     Qt.WindowType.WindowCloseButtonHint)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowTitleHint | Qt.WindowType.CustomizeWindowHint)

        self.setMinimumWidth(600)

        self.vbox = QVBoxLayout(self)

        hbox1 = QHBoxLayout()
        label = QLabel("Cluster Name :")
        self.server_name = QComboBox()
        if bool(list_config):
            self.server_name.addItems(list_config.keys())
        self.server_name.setMinimumWidth(int(self.size().width() / 4))
        self.server_name.currentIndexChanged.connect(self.actionCombobox)
        hbox1.addWidget(label)
        hbox1.addWidget(self.server_name)

        hbox2 = QHBoxLayout()
        host_name = QLabel("Host name :")
        self.area_name = QLineEdit()
        self.area_name.textChanged.connect(self.field_changed)
        hbox2.addWidget(host_name)
        hbox2.addWidget(self.area_name)

        hbox2a = QHBoxLayout()
        labwd = QLabel("Password :")
        self.wd_field = QLineEdit()
        self.wd_field.textChanged.connect(self.field_changed)
        self.wd_field.setEchoMode(QLineEdit.EchoMode.Password)
        hbox2a.addWidget(labwd)
        hbox2a.addWidget(self.wd_field)

        hbox3 = QHBoxLayout()
        skrypy_dir = QLabel("Skrypy directory on this cluster :")
        self.skry_dir = QLineEdit()
        self.skry_dir.textChanged.connect(self.field_changed)
        hbox3.addWidget(skrypy_dir)
        hbox3.addWidget(self.skry_dir)

        hbox4 = QHBoxLayout()
        wrk_space = QLabel("Workspace directory on this cluster :")
        self.wrkspace_dir = QLineEdit()
        self.wrkspace_dir.textChanged.connect(self.field_changed)
        hbox4.addWidget(wrk_space)
        hbox4.addWidget(self.wrkspace_dir)

        hbox5 = QHBoxLayout()
        cpu_nbr = QLabel("Mx number of cpus to use :")
        self.cpu_to_use = QLineEdit()
        self.cpu_to_use.textChanged.connect(self.field_changed)
        hbox5.addWidget(cpu_nbr)
        hbox5.addWidget(self.cpu_to_use)

        hbox6 = QHBoxLayout()
        self.use_x11_bool = QCheckBox("X11 forwarding")
        self.use_x11_bool.stateChanged.connect(self.field_changed)
        hbox6.addWidget(self.use_x11_bool)

        vbox7 = QVBoxLayout()
        pre_exec = QLabel("Pre-execution command :")
        self.exec_cmd = QTextEdit()
        self.exec_cmd.textChanged.connect(self.field_changed)
        vbox7.addWidget(pre_exec)
        vbox7.addWidget(self.exec_cmd)

        buttonGo = QPushButton('Go', self)
        buttonQuit = QPushButton('Quit', self)
        self.buttonSave = QPushButton('Save', self)
        buttonSaveAs = QPushButton('Save As ...', self)
        self.buttonDelete = QPushButton('Delete from list', self)
        self.buttonTest = QPushButton('Test', self)

        hbox8 = QHBoxLayout()
        hbox8.addWidget(buttonGo)
        hbox8.addWidget(buttonQuit)
        hbox8.addWidget(self.buttonSave)
        hbox8.addWidget(buttonSaveAs)
        hbox8.addWidget(self.buttonDelete)
        hbox8.addWidget(self.buttonTest)

        if self.config == 'config':
            buttonGo.setEnabled(False)

        buttonGo.clicked.connect(self.go)
        buttonQuit.clicked.connect(self.QUIT)
        self.buttonSave.clicked.connect(self.save)
        buttonSaveAs.clicked.connect(self.saveas)
        self.buttonDelete.clicked.connect(lambda: self.deleteServer(self.server_name.currentText()))
        self.buttonTest.clicked.connect(self.test_cluster)

        self.info1 = QLabel()
        self.info2 = QLabel()
        self.info3 = QLabel()
        self.memory_info = QTextEdit()
        self.memory_info.setStyleSheet("background: rgba(100,100,100,20%)")

        self.vbox.addLayout(hbox1)
        self.vbox.addLayout(hbox2)
        self.vbox.addLayout(hbox2a)
        self.vbox.addLayout(hbox3)
        self.vbox.addLayout(hbox4)
        self.vbox.addLayout(hbox5)
        self.vbox.addLayout(hbox6)
        self.vbox.addLayout(vbox7)
        self.vbox.addLayout(hbox8)
        self.vbox.addWidget(self.info1)
        self.vbox.addWidget(self.info2)
        self.vbox.addWidget(self.info3)
        self.vbox.addWidget(self.memory_info)

        self.setLayout(self.vbox)

        self.actionCombobox()
        self.setWindowTitle('Clusters configuration')

    def actionCombobox(self):
        current_server = self.server_name.currentText()

        if self.server_name.currentText() == 'template':
            self.buttonDelete.setEnabled(False)
            self.buttonSave.setEnabled(False)
            self.buttonTest.setEnabled(False)
        else:
            self.buttonDelete.setEnabled(True)
            self.buttonSave.setEnabled(True)
            self.buttonTest.setEnabled(True)

        self.area_name.setText(self.list_config[current_server]['host_name'])
        self.skry_dir.setText(self.list_config[current_server]['skrypy_server_directory'])
        self.wrkspace_dir.setText(self.list_config[current_server]['server_workspace_directory'])
        self.cpu_to_use.setText(str(self.list_config[current_server]['cpu_number']))
        self.use_x11_bool.setChecked(bool(self.list_config[current_server]['X11_forwarding']))
        self.exec_cmd.setText(self.list_config[current_server]['pre_execution_command'])
        try:
            tmpA = self.list_config[current_server]['fd_command']
            tmpB = self.list_config[current_server]['fk_command']
            tmppd = get_dph(tmpA, tmpB).get_ushn()
        except Exception as err:
            print('error to open cluster config:', err)
            tmppd = ''
        self.wd_field.setText(tmppd)
        self.info1.clear()
        self.info2.clear()
        self.info3.clear()
        self.memory_info.clear()
        self.setWindowTitle('Clusters configuration')

    def go(self):
        self.server_param = [self.area_name.text(),
                             self.skry_dir.text(),
                             self.wrkspace_dir.text(),
                             self.cpu_to_use.text(),
                             self.use_x11_bool.isChecked(),
                             self.exec_cmd.toPlainText(),
                             self.wd_field.text(),
                             self.server_name.currentText()]
        self.close()

    def QUIT(self):
        if "*" in self.windowTitle():
            msg = QMessageBox()
            msg.setWindowTitle("Config modified...")
            msg.setText("Save the modifications ?)")
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg.setDefaultButton(QMessageBox.StandardButton.Yes)
            x = msg.exec()
            if x == QMessageBox.StandardButton.Yes:
                self.save()
                # event.accept()
        self.server_param = []
        self.close()

    def save(self):
        tmp = set_dph(self.wd_field.text())
        tmppd = tmp.get_shn()
        tmppk = tmp.get_fk()

        self.list_config[self.server_name.currentText()] = {'host_name': self.area_name.text().strip(),
                                                            'skrypy_server_directory': self.skry_dir.text().strip(),
                                                            'server_workspace_directory': self.wrkspace_dir.text().strip(),
                                                            'cpu_number': self.cpu_to_use.text().strip(),
                                                            'X11_forwarding': self.use_x11_bool.isChecked(),
                                                            'pre_execution_command': self.exec_cmd.toPlainText(),
                                                            'fd_command': tmppd, 'fk_command': tmppk}
        with open(self.server_yml, 'w', encoding='utf8') as stream:
            yaml.dump(self.list_config, stream, default_flow_style=False)
        self.setWindowTitle('Clusters configuration')

    class _NewServerName(QDialog):

        def __init__(self, list_server, parent=None):
            super(servers_window._NewServerName, self).__init__(parent)
            self.list_server = list_server
            layout = QVBoxLayout(self)
            hlay1 = QHBoxLayout()
            layout.addLayout(hlay1)
            hlay1.addWidget(QLabel('new name:'))
            self.name_line = QLineEdit()
            hlay1.addWidget(self.name_line)
            hlay2 = QHBoxLayout()
            layout.addLayout(hlay2)
            ok = QPushButton('OK')
            hlay2.addWidget(ok)
            cancel = QPushButton('Cancel')
            hlay2.addWidget(cancel)
            ok.clicked.connect(self.ok_clicked)
            cancel.clicked.connect(self.reject)
            self.info = QLabel()
            layout.addWidget(self.info)

        def ok_clicked(self):
            if self.name_line.text() not in self.list_server:
                self.accept()
            else:
                self.info.setText("<span style=\" \
                                  font-size:10pt; \
                                  color:#cc0000;\" > error : " + self.name_line.text() + " already exists ! </span>")
                return

    def saveas(self):
        dial = self._NewServerName(self.list_config.keys())
        # dial.name_line.setText(dial.name_line.text())
        res = dial.exec()
        if res:
            tmp = set_dph(self.wd_field.text())
            tmppd = tmp.get_shn()
            tmppk = tmp.get_fk()
            self.list_config[dial.name_line.text()] = {'host_name': self.area_name.text().strip(),
                                                       'skrypy_server_directory': self.skry_dir.text().strip(),
                                                       'server_workspace_directory': self.wrkspace_dir.text().strip(),
                                                       'cpu_number': self.cpu_to_use.text().strip(),
                                                       'X11_forwarding': self.use_x11_bool.isChecked(),
                                                       'pre_execution_command': self.exec_cmd.toPlainText().strip(),
                                                       'fd_command': tmppd, 'fk_command': tmppk}
            with open(self.server_yml, 'w', encoding='utf8') as stream:
                yaml.dump(self.list_config, stream, default_flow_style=False)

            self.server_name.addItem(dial.name_line.text())
            # self.server_name.update()
            index = self.server_name.findText(dial.name_line.text(), Qt.MatchFlag.MatchFixedString)
            self.server_name.setCurrentIndex(index)
            self.setWindowTitle('Clusters configuration')

    class _ConfirmationDialog(QDialog):

        def __init__(self, cur_serv, parent=None):
            super().__init__(parent)

            self.setWindowTitle("Confirmation")

            QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

            self.buttonBox = QDialogButtonBox(QBtn)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)

            layout = QVBoxLayout()
            message = QLabel("delete {}?".format(cur_serv))
            layout.addWidget(message)
            layout.addWidget(self.buttonBox)
            self.setLayout(layout)

    def deleteServer(self, currentServer):
        dial = self._ConfirmationDialog(currentServer)
        res = dial.exec()
        if res:
            del self.list_config[currentServer]
            with open(self.server_yml, 'w', encoding='utf8') as stream:
                yaml.dump(self.list_config, stream, default_flow_style=False)
            index = self.server_name.findText(currentServer, Qt.MatchFlag.MatchFixedString)
            self.server_name.removeItem(index)

    def clear_infos(self):
        self.info1.clear()
        self.info2.clear()
        self.info3.clear()
        self.memory_info.clear()
        self.info1.repaint()

    def test_cluster(self):

        self.clear_infos()

        host = self.area_name.text()
        host_name = self.area_name.text()

        if '@' in host_name:
            host_name = host_name[host_name.index('@') + 1:]
        else:
            msg = 'the host has not user name'
            msg = self.styleErrorMessage(msg)
            self.info1.setText(msg)
            return

        # host_name_m = host_name.split()
        # if len(host_name) == 2:

        cmd_base = ['sshpass', '-p', self.wd_field.text(), 'ssh']
        hnm = host.split()
        if len(hnm) == 2:
            cmd_base.extend(['-o', 'ProxyCommand={}'.format('sshpass -p {} ssh -W %h:%p {}'.format(self.wd_field.text(), hnm[0].strip())), hnm[1].strip()])
        else:
            cmd_base.append(host)

        # connection test
        cmd_comp = cmd_base.copy()
        cmd_comp.append('test -e {}; echo $?'.format(self.skry_dir.text().strip()))
        cmd_comp.append('&&')
        cmd_comp.append('test -e {}; echo $?'.format(self.wrkspace_dir.text().strip()))
        proc = subprocess.Popen(cmd_comp, stdout=subprocess.PIPE, shell=False)
        timer = Timer(2, proc.kill)
        try:
            timer.start()
            stdout, stderr = proc.communicate()
        except Exception as err:
            msg = '{} connection problem'.format(host_name)
            msg = self.styleErrorMessage(msg)
            self.info1.setText(msg)
            return
        finally:
            timer.cancel()
        # print('stdout', stdout, stderr)
        if stdout.decode('UTF-8'):
            answs = stdout.decode('UTF-8').split('\n')
            msg = '{} connection ok'.format(host_name)
            msg = self.styleGoodMessage(msg)
            self.info1.setText(msg)
            if not bool(int(answs[0])):
                msg = self.styleGoodMessage('Skrypy directory exists')
            else:
                msg = self.styleErrorMessage('Skrypy directory doesn\'t exist !')
            self.info2.setText(msg)
            if not bool(int(answs[1])):
                msg = self.styleGoodMessage('Workspace directory exists')
            else:
                msg = self.styleErrorMessage('Workspace directory doesn\'t exist !')
            self.info3.setText(msg)
        else:
            msg = '{} connection problem'.format(host_name)
            msg = self.styleErrorMessage(msg)
            self.info1.setText(msg)
            msg = self.styleErrorMessage('problem with login or password or network  (try on a terminal if this problem persists)')
            self.info2.setText(msg)
            return

        cmd_comp = cmd_base.copy()
        cmd_comp.append('echo "GPU:"; nvidia-smi --query-gpu=memory.used --format=csv && echo "RAM:"; free -m --human')
        stdout, stderr = subprocess.Popen(cmd_comp, stdout=subprocess.PIPE).communicate()
        msg = self.server_name.currentText() + '\n'
        msg += stdout.decode('UTF-8')
        # self.memory_info.setText(msg)
        self.memory_info.setText(msg)

    def styleErrorMessage(self, msg):
        style = "<span style=\" \
                              font-size:10pt; \
                              color:#cc0000;\" >" \
                              + msg + "</span>"
        return style

    def styleGoodMessage(self, msg):
        style = "<span style=\" \
                              font-size:10pt; \
                              color:#007700;\" >" \
                              + msg + "</span>"
        return style

    def get_params(self):
        return self.server_param
