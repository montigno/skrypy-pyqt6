class ssh_file_dir_exists():
    def __init__(self, path='path', host_name='', host_password=''):
        from subprocess import Popen, PIPE

        stdout, stderr = Popen(['sshpass', '-p', host_password, 'ssh', host_name,
                                'test -e ' + path + '; echo $?'], stdout=PIPE).communicate()
        self.answ = not bool(int(stdout[:-1]))

    def exists(self: 'bool'):
        return self.answ

######################################################################################################################


class ssh_list_files_in_directory():
    def __init__(self, dir='path', host_name='', host_password=''):
        from subprocess import Popen, PIPE

        stdout, stderr = Popen(['sshpass', '-p', host_password, 'ssh', host_name,
                                'ls -l ' + dir], stdout=PIPE).communicate()
        self.answ = stdout.decode()

    def exists(self: 'str'):
        return self.answ

######################################################################################################################


class ssh_get_size():
    def __init__(self, dir_or_file='path', host_name='', host_password=''):
        from subprocess import Popen, PIPE

        stdout, stderr = Popen(['sshpass', '-p', host_password, 'ssh', host_name,
                                'du -msh ' + dir_or_file], stdout=PIPE).communicate()
        self.answ = stdout.decode()

    def size(self: 'str'):
        return self.answ

######################################################################################################################


# class ssh_remove_files_directory():
#     def __init__(self, path_type="enumerate(('file', 'directory'))", paths='path', host_name='', host_password=''):
#         from subprocess import Popen, PIPE
#
#         if not isinstance(paths, list):
#             source = [paths]
#         else:
#             source = paths
#
#         for src in source:
#             if path_type == 'directory':
#                 exec_cli = "rm -r {}".format(src)
#             else:
#                 exec_cli = "rm {}".format(src)
#             cmd = ['sshpass', '-p', host_password, 'ssh', host_name, exec_cli]
#             print(" ".join(cmd[3:]))
#             p = Popen(cmd, stdin=p1.stdout, stdout=PIPE, stderr=PIPE)
#             # self.output = p.stdout.read().decode()
#             p.communicate()
#             p.wait()
#             if p.returncode == 0:
#                 print('{} deleted'.format(src))
#             else:
#                 print('deletion error for {}'.format(src))
