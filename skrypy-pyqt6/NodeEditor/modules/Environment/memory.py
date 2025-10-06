class clean_RAM():
    def __init__(self, sudo_password=''):
        # from NodeEditor.modules.Environment.authentification import passwd_dialog
        from subprocess import Popen, PIPE

        # sudo_password = passwd_dialog("Enter your sudo password").passwd()
        if not sudo_password or sudo_password == 'None':
            print("RAM cleaning abandoned")
            self.output = ''
        else:
            p1 = Popen(['echo', sudo_password], stdout=PIPE, stderr=PIPE)
            p2 = Popen(['sudo', '-S', 'sysctl', 'vm.drop_caches=3'], stdin=p1.stdout, stdout=PIPE)
            self.output = p2.stdout.read().decode()
            p2.communicate()
            print('RAM cleaning done')

    def stdout(self: 'str'):
        return self.output

##############################################################################


class clean_SWAP():
    def __init__(self, sudo_password=''):
        # from NodeEditor.modules.Environment.authentification import passwd_dialog
        from subprocess import Popen, PIPE

        # sudo_password = passwd_dialog("Enter your sudo password").passwd()
        if not sudo_password or sudo_password == 'None':
            print("SWAP cleaning abandoned")
            self.output = ''
        else:
            p1 = Popen(['echo', sudo_password], stdout=PIPE)
            p2 = Popen(['sudo', '-S', 'swapoff', '-a'], stdin=p1.stdout, stdout=PIPE)
            p2.communicate()
            p3 = Popen(['echo', sudo_password], stdout=PIPE)
            p4 = Popen(['sudo', '-S', 'swapon', '-a'], stdin=p3.stdout, stdout=PIPE)
            self.output = p4.stdout.read().decode()
            p4.communicate()
            print('SWAP cleaning done')

    def stdout(self: 'str'):
        return self.output
