from NodeEditor.ssh.Diagram_Execution_dep import execution2

import os
import sys
import gc
import yaml
import subprocess

from threading import Thread


class execution_ssh():

    def __init__(self, workspace, files_dgr, n_cpu, mode, cluster, parent=None):
        files_dgr = files_dgr[1:-1].split(',')
        self.n_cpu = int(n_cpu)
        self.Start_environment()
        col = '\x1b[38;2;0;100;255m'
        for dgr in files_dgr:
            print("\n{} Excution {} ({}) in progress ... \033[0m".format(col, dgr, cluster))
            self.execute_Diagram(dgr, mode)

    def Start_environment(self):
        env_file = os.path.join(os.path.expanduser('~'), '.skrypy', 'env_parameters.txt')
        list_env = {}
        if os.path.exists(env_file):
            with open(env_file, 'r') as stream:
                for line in stream:
                    line_str = line.rstrip()
                    if line_str:
                        if '#' not in line and ('export' in line or 'sh ' in line):
                            if 'export PATH=' in line:
                                line_mod = line.replace('export', '').replace('$PATH:', '').replace('PATH=', '').strip()
                                if 'PATH' not in list_env.keys():
                                    list_env['PATH'] = line_mod
                                else:
                                    list_env['PATH'] += os.pathsep + line_mod
                            elif 'sh ' in line[0:3]:
                                line_mod = line[2:].strip()
                                list_env['sh'] = line_mod
                            elif '=' in line:
                                line_mode = line.split('=')
                                line_mode[0] = line_mode[0].replace('export', '').strip()
                                list_env[line_mode[0]] = line_mode[1]

            for kenv, venv in list_env.items():
                if kenv == 'sh':
                    try:
                        os.popen('sh ' + venv.replace('\n', ''))
                    except Exception as err:
                        print(err)
                elif kenv == 'PATH':
                    os.environ['PATH'] += os.pathsep + venv.replace('\n', '')
                else:
                    os.environ[kenv] = venv.replace('\n', '')

            # if 'CONDASOURCE' in list_env.keys():
            #     print('CONDASOURCE found')
            #     path_src_conda = list_env['CONDASOURCE']
            #     subprocess.check_output("source {}".format(path_src_conda), shell=True, executable="/bin/bash")

            print("Environment variables:")
            print(os.environ)

    def execute_Diagram(self, file_dgr, mode):
        SharedMemoryManager(False)
        gc.collect()
        title_dgr = os.path.basename(file_dgr)

        # with open(file_dgr) as f:
        #     txt_code = f.read()
        file_head = ''
        file_end = ''

        with open(file_dgr) as f:
            i = 0
            move = False
            for line in f:
                if '[execution]' in line:
                    move = True
                if move:
                    i += 1
                if 1 < i < 8:
                    file_head += line
                else:
                    if '[execution]' not in line:
                        file_end += line
                if i == 8:
                    move = False

        txt_code = file_head + file_end
        # col = col = '\x1b[38;2;0;100;255m'
        # print('\n' * 2)
        # print("{}execution: {}\033[0m".format(col, title_dgr))
        # if mode_th:
        #     mode = 'Multi-threading'
        # else:
        #     mode = 'Sequential'

        if self.check_script_code(txt_code):
            print("Warning: some scripts contain the terms 'QApplication' or 'syst.exit', remove them !")
            return

        print("> started in {} mode".format(mode))

        args = (txt_code, {}, '')

        # current_dir_path = os.path.dirname(os.path.realpath(__file__))
        # source_disp = os.path.join(current_dir_path, 'tasks_progress.py')
        # subprocess.Popen([sys.executable, source_disp, 'start diagram'])
        self.runner = ThreadDiagram(title_dgr, self.n_cpu, args)
        try:
            sr = self.runner.run()
        except Exception as err:
            print("\n\33[31mThis diagram contains errors : {}\33[0m".format(str(err)))
        # self.runner.sysctrl.kill()
        # for proc in psutil.process_iter():
        #     print("pid:", proc.name())

        # self.runner = Window_progressbar(title_dgr, args, editor)
        # self.runner.close()

    def check_script_code(self, txt):
        if 'QApplication(' in txt:
            return True
        return False


class SharedMemoryManager():

    def __init__(self, empt):
        super(SharedMemoryManager, self).__init__()
        self.file_shm = os.path.join(os.path.expanduser('~'), '.skrypy', 'list_shm.yml')
        if empt:
            self.toempty()
        else:
            self.readList()

    def readList(self):
        data = {}
        if os.path.exists(self.file_shm):
            with open(self.file_shm, 'r') as file_yml:
                try:
                    data = yaml.load(file_yml, Loader=yaml.SafeLoader)
                except Exception as err:
                    print("error to read data from list_shm.yml:", err)
                    os.remove(self.file_shm)
                    return
            if not bool(data):
                os.remove(self.file_shm)

    def toempty(self):
        if os.path.exists(self.file_shm):
            os.remove(self.file_shm)


class ThreadDiagram(Thread):

    def __init__(self, name, n_cpu, args, parent=None):
        super(ThreadDiagram, self).__init__()
        self.name = name
        self.args = args
        self.pipe_exec = execution2(n_cpu)
        with open(os.path.join(os.path.expanduser('~'), '.skrypy', 'list_process.tmp'), 'w') as f:
            # list_proc = f.readlines()
            f.write('{}{}{}\n'.format('Process Name', ' '*10, 'ID'))

    def run(self):
        self.pipe_exec.go_execution(*self.args)


if __name__ == '__main__':
    self_dir_path = os.path.dirname(os.path.realpath(__file__))
    wrksp, diags, cpu, mode = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    if len(sys.argv) == 7:
        clust = sys.argv[6]
    else:
        clust = sys.argv[5]
    run_ssh = execution_ssh(wrksp, diags, cpu, mode, clust)
    os.chdir(os.path.expanduser('~'))
