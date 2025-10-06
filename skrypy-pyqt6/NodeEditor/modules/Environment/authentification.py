class login_passwd_dialog():
    def __init__(self, message=''):
        import os
        import sys
        from subprocess import run
        if not message:
            message = "Enter your login and password"
        current_dir_path = os.path.abspath(os.path.join(__file__, "../../.."))
        source_disp = os.path.join(current_dir_path, 'api', 'dialog_login_pwd.py')
        p = run([sys.executable, source_disp, message], check=False, capture_output=True, text=True)
        aws = p.stdout.split(' ')
        self.log, self.pwd = aws[0].strip(), aws[1].strip()

    def login(self: 'str'):
        return self.log

    def passwd(self: 'str'):
        return self.pwd

##############################################################################


class passwd_dialog():
    def __init__(self, message=''):
        import os
        import sys
        from subprocess import run
        if not message:
            message = "Enter your password"
        current_dir_path = os.path.abspath(os.path.join(__file__, "../../.."))
        source_disp = os.path.join(current_dir_path, 'api', 'dialog_pwd.py')
        p = run([sys.executable, source_disp, message], check=False, capture_output=True, text=True)
        self.pwd = p.stdout.strip()

    def passwd(self: 'str'):
        return self.pwd
