class scp_transfert():
    """
    Allows to copy data between computers in a network. Needs ssh pass

    Args:
        data_type: (str) type of data, 'file' or 'directory'
        direction: (str) 'local_to_host' or 'host_to_local'
        host_name: (string) address of the host (user@host_name)
        host_password: (string) the host password
        host_path: (path or list of path) file path relative to host
        local_path: (path or list of path) local file path

    Returns:
        out_path: (path or list of path) path where the files were transferred
        stdout: (str)

    Note:
        GUI: no
    """
    def __init__(self, data_type="enumerate(('file', 'directory'))", direction="enumerate(('local_to_host', 'host_to_local'))",
                 host_name='', host_password='', host_path='path', local_path='path'):
        from subprocess import Popen, PIPE
        import os

        self.out_pt, self.output = [], ''

        if not host_password or host_password == 'None':
            print("connection abandoned")
        else:
            if direction == 'host_to_local':
                if not isinstance(host_path, list):
                    host_path = [host_path]
                    # host_path = ','.join(host_path)
                    # host_path = '"\\"{' + host_path + '"\\"}'
                source = ["{}:{}".format(host_name, hp) for hp in host_path]
                dest = local_path
                for src in source:
                    self.out_pt.append(os.path.join(os.path.basename(local_path), os.path.basename(src)))
            else:
                if not isinstance(local_path, list):
                    local_path = [local_path]
                    # local_path = ','.join(local_path)
                    # local_path = '"\\{"' + local_path + '"\\}"'
                source = local_path
                dest = "{}:{}".format(host_name, host_path)
                for src in source:
                    self.out_pt.append(os.path.join(host_path, os.path.basename(src)))
            p1 = Popen(['echo', host_password], stdout=PIPE, stderr=PIPE)
            if data_type == 'directory':
                cmd = ['sshpass', '-p', host_password, 'scp', '-r']
                # cmd = ['sshpass', '-p', host_password, 'scp', '-r', source, dest]
            else:
                cmd = ['sshpass', '-p', host_password, 'scp']
                # cmd = ['sshpass', '-p', host_password, 'scp', source, dest]
            cmd_comp = cmd.copy()
            cmd_comp.extend(source)
            cmd_comp.append(dest)
            print(" ".join(cmd_comp[3:]))
            p2 = Popen(cmd_comp, stdin=p1.stdout, stdout=PIPE, stderr=PIPE)
            self.output = p2.stdout.read().decode()
            p2.communicate()
            p2.wait()
            if p2.returncode == 0:
                print('transfert done')
            else:
                self.out_pt = []
                print('transfert error !!, code ' + str(p2.returncode))
            if len(self.out_pt) == 1:
                self.out_pt = self.out_pt[0]

    def out_path(self: 'list_path'):
        return self.out_pt

    def stdout(self: 'str'):
        return self.output

##############################################################################


class scp_transfert_via_bastion():
    """
    Allows to copy data between computers in a network. Needs sshpass

    Args:
        type: (str) type of data, 'file' or 'directory'
        host_name: (string) address of the host (user@host_name)
        host_password: (string) the host password
        source: (path) path of the source
        dest: (path) path of the destination

    Returns:
        stdout: (str)

    Note:
        GUI: no
    """
    def __init__(self, data_type="enumerate(('file', 'directory'))", direction="enumerate(('local_to_host', 'host_to_local'))",
                 host_bastion_name='', host_name='', host_password='', host_path='path', local_path='path'):
        from subprocess import Popen, PIPE
        import os

        if not host_password or host_password == 'None':
            print("connection abandoned")
            self.out_pt, self.output = 'path', ''
        else:
            host_password = host_password.replace('\n', '')
            if direction == 'host_to_local':
                if isinstance(host_path, list):
                    host_path = ' '.join(host_path)
                    # host_path = ','.join(host_path)
                    # host_path = '"\\"{' + host_path + '"\\"}'
                source = "{}:{}".format(host_name, host_path)
                dest = local_path
                self.out_pt = os.path.join(local_path, os.path.basename(host_path))
            else:
                if isinstance(local_path, list):
                    local_path = ' '.join(local_path)
                    # local_path = ','.join(local_path)
                    # local_path = '"\\{"' + local_path + '"\\}"'
                source = local_path
                dest = "{}:{}".format(host_name, host_path)
                self.out_pt = os.path.join(host_path, os.path.basename(local_path))
            p1 = Popen(['echo', host_password], stdout=PIPE, stderr=PIPE)
            
            if data_type == 'directory':
                # cmd = ['sshpass', '-p', host_password, 'scp', '-r', source, dest]
                cmd_base = ['sshpass', '-p', host_password.strip(), 'scp', '-r']
            else:
                # cmd = ['sshpass', '-p', host_password, 'scp', source, dest]
                cmd_base = ['sshpass', '-p', host_password.strip(), 'scp']
            cmd_comp = cmd_base.copy()
            cmd_comp.extend(['-o', 'ProxyCommand={}'.format('sshpass -p {} ssh -W %h:%p {}'.format(host_password, host_bastion_name.strip()))])
            cmd_comp.extend([source, dest])
            print(cmd_comp[3:])
            p2 = Popen(cmd_comp, stdin=p1.stdout, stdout=PIPE, stderr=PIPE)
            self.output = p2.stdout.read().decode()
            p2.communicate()
            p2.wait()
            if p2.returncode == 0:
                print('transfert done')
            else:
                print('transfert error !!, code ' + str(p2.returncode))

    def out_path(self: 'path'):
        return self.out_pt

    def stdout(self: 'str'):
        return self.output

##############################################################################


class scp_transfert_multifiles():
    """
    Allows to copy data between computers in a network. Needs ssh pass

    Args:
        type: (str) type of data, 'file' or 'directory'
        host_name: (string) address of the host (user@host_name)
        host_password: (string) the host password
        source: (path) path of the source
        dest: (path) path of the destination

    Returns:
        stdout: (str)

    Note:
        GUI: no
    """
    def __init__(self, data_type="enumerate(('file', 'directory'))", direction="enumerate(('local_to_host', 'host_to_local'))",
                 host_name='', host_password='', host_path='path', local_path='path'):
        from subprocess import Popen, PIPE
        import os

        if not host_password or host_password == 'None':
            print("connection abandoned")
            self.out_pt, self.output = 'path', ''
        else:
            self.out_pt = []
            if direction == 'host_to_local':
                dest = local_path
                if isinstance(host_path, list):
                    source = []
                    for src in host_path:
                        source.append("{}:{}".format(host_name, src))
                        self.out_pt.append(os.path.join(local_path, os.path.basename(src)))
                else:
                    source = ["{}:{}".format(host_name, host_path)]
                    self.out_pt = os.path.join(local_path, os.path.basename(host_path))
            else:
                dest = "{}:{}".format(host_name, host_path)
                if isinstance(local_path, list):
                    source = local_path
                    for src in source:
                        self.out_pt.append(os.path.join(host_path, os.path.basename(src)))
                else:
                    source = [local_path]
                    self.out_pt = os.path.join(host_path, os.path.basename(local_path))
            p1 = Popen(['echo', host_password], stdout=PIPE, stderr=PIPE)
            for src in source:
                if data_type == 'directory':
                    cmd = ['sshpass', '-p', host_password, 'scp', '-r', src, dest]
                else:
                    cmd = ['sshpass', '-p', host_password, 'scp', src, dest]
                print(" ".join(cmd[3:]))
                p2 = Popen(cmd, stdin=p1.stdout, stdout=PIPE, stderr=PIPE)
                self.output = p2.stdout.read().decode()
                p2.communicate()
                p2.wait()
                if p2.returncode == 0:
                    print('transfert done')
                else:
                    print('transfert error !!, code ' + str(p2.returncode))

    def out_path(self: 'path'):
        return self.out_pt

    def stdout(self: 'str'):
        return self.output

##############################################################################


class rsync_network():
    def __init__(self, direction="enumerate(('local_to_host', 'host_to_local'))",
                 host_name='', host_password='', host_path='path', local_path='path'):
        from subprocess import Popen, PIPE

        if not host_password or host_password == 'None':
            print("connection abandoned")
            self.out_pt, self.output = 'path', ''
        else:
            if direction == 'host_to_local':
                source = "{}:{}".format(host_name, host_path)
                dest = local_path
            else:
                source = local_path
                dest = "{}:{}".format(host_name, host_path)
            p1 = Popen(['echo', host_password], stdout=PIPE, stderr=PIPE)
            cmd = ['sshpass', '-p', host_password, 'rsync', '-va', source, dest]
            print(" ".join(cmd[3:]))
            p2 = Popen(cmd, stdin=p1.stdout, stdout=PIPE)
            self.output = p2.stdout.read().decode()
            p2.communicate()
            p2.wait()
            print('synchronization done')

    def stdout(self: 'str'):
        return self.output

##############################################################################


class rsync_local():
    def __init__(self, source='path', dest='path'):
        from subprocess import Popen, PIPE

        cmd = ['rsync', '-av', source, dest]
        print(" ".join(cmd))
        p2 = Popen(cmd, stdin=PIPE, stdout=PIPE)
        self.output = p2.stdout.read().decode()
        p2.communicate()
        p2.wait()
        print('synchronization done')

    def stdout(self: 'str'):
        return self.output
