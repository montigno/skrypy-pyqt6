class path_export():
    def __init__(self, file_path='path'):
        import os
        if file_path not in os.environ["PATH"]:
            os.environ["PATH"] += os.pathsep + file_path
        print('PATH =', os.environ["PATH"])
        print()

##############################################################################


class param_export():
    def __init__(self, param_name='', file_path='path'):
        import os
        # if file_path not in os.environ[param_name]:
        os.environ[param_name] = file_path
        print(param_name, ' =', os.environ[param_name])
        print()

##############################################################################


class system_cmd_dyn():
    def __init__(self, cmd='', **dynamicsInputs):
        import subprocess
        command = cmd
        if dynamicsInputs:
            command = [cmd]
            for di in dynamicsInputs:
                command.append(dynamicsInputs[di])
        subprocess.call(command)

##############################################################################


class sh_command():
    def __init__(self, sh_file='path'):
        import os
        os.popen('sh ' + sh_file)

##############################################################################


class system_activate_conda():
    def __init__(self, source_conda='path', env='', **dynamicsInputs):
        import subprocess
        command = '. {} && conda activate {}'.format(source_conda, env)
        print(command)
        subprocess.run(command, shell=True, check=True)
