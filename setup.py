##########################################################################
# mriWorks - Copyright (C) IRMAGE/INSERM, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# https://cecill.info/licences/Licence_CeCILL_V2-en.html
# for details.
##########################################################################
'''
Skrypy 25.10.06b   setup   Oct. 06 2025

SYNOPSIS
    Install Skrypy in a virtual python environment (administration rights required).

USAGE (in the terminal)
    1 - conda activate (optional, necessary if your Python is in conda)
    2 - cd <path/where/setup.py/is/located>
    3 - python3.x setup.py dest
            python3.x : you can choose the version of python installed on your system (ex python3.11)
            dest : full path of your virtual environment 
                   (ex /home/mosfet/Apps/skrypy_venv_3x, the last directory will be created)
            aliases will be created in the .bashrc file: 'skrypy_3x', 'skrypy_3x_install and skrypy_3x_test
    4 - source ~/.bashrc (to initialize aliases)
    5 - skrypy_3x_install (to install librairies in your virtual environment, may take a few minutes)
    6 - skrypy_3x_test (optional, for the test, it will last about 20s)
    7 - skrypy_3x (to launch)

EXAMPLES
    conda activate (if necessary)
    cd <path/where/setup.py/is/located>
    python3.8 setup.py /home/mosfet/Apps/skrypy_venv_38
    source ~/.bashrc
    skrypy_38_install
    skrypy_38_test (optional)
    skrypy_38

    conda activate (if necessary)
    cd <path/where/setup.py/is/located>
    python3.11 setup.py /home/username/Applications/skrypy_venv_311
    source ~/.bashrc
    skrypy_311_install
    skrypy_311_test (optional)
    skrypy_311
'''

from subprocess import Popen
import sys
import os
import platform


# Basic color codes
RED = '\033[91m'
GREEN = '\033[92m'
ORANGE = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'  # This resets the color back to default

def install(command):
    p = Popen(command, shell=True)
    p.wait()

def install_linux(pyth, base_dir):
    try:
        install('pip3 install --upgrade pip')
    except Exception as err:
        print("warning with pip update:", err)
    try:
        install('pip3 install tk')
    except Exception as err:
        print("warning with tk installation:", err)
    try:
        install('pip3 install virtualenv')
    except Exception as err:
        print("Warning with Virtualenv installation:", err)
    install(pyth + ' -m venv ' + base_dir)
    install('cp -r skrypy/ ' + base_dir)
    print("{}{} is created!{}".format(GREEN, base_dir, RESET))

    src_bash = os.path.join(os.path.expanduser('~'), '.bashrc')
    ext_py = pyth.split(".")
    ext_py = "_{}{}".format(ext_py[0][-1], ext_py[1])

    with open(src_bash, 'r') as fp:
        lines = fp.readlines()
    start_here = False
    if '#skrypy {}\n'.format(pyth) in lines:
        print("{}aliases for skrypy version {} already exist! Manually update .bashrc !{}".format(RED, pyth, RESET))
        exit()

    fp = open(src_bash)

    os.system("echo '\n#skrypy {}' >> ~/.bashrc".format(pyth))
    os.system("echo 'cmd_sk{}=\"source ".format(ext_py) + os.path.join(base_dir, "bin", "activate") +
              "; cd " + os.path.join(base_dir, "skrypy") +
              "; " + pyth + " main.py; deactivate\"' >> ~/.bashrc")
    os.system("echo 'cmd_sk{}_packages=\"source ".format(ext_py) + os.path.join(base_dir, "bin", "activate") +
              "; cd " + os.path.join(base_dir, "skrypy") +
              "; " + pyth + " install_modules.py; deactivate\"' >> ~/.bashrc")
    os.system("echo 'cmd_sk{}_test=\"source ".format(ext_py) + os.path.join(base_dir, "bin", "activate") +
              "; cd " + os.path.join(base_dir, "skrypy") +
              "; " + pyth + " testunit.py; deactivate\"' >> ~/.bashrc")
    os.system("echo 'alias skrypy{}=$cmd_sk{}".format(ext_py, ext_py) + "'>> ~/.bashrc")
    os.system("echo 'alias skrypy{}_packages=$cmd_sk{}_packages".format(ext_py, ext_py) + "'>> ~/.bashrc")
    os.system("echo 'alias skrypy{}_test=$cmd_sk{}_test".format(ext_py, ext_py) + " '>> ~/.bashrc")
    os.system("echo '\n' >> ~/.bashrc")
    print("{}.bashrc modified, tape source ~/.bashrc{}".format(ORANGE, RESET))
    #p1 = Popen('chmod +x run_bg.sh', shell=True)
    #p1.wait()
    #p2 = Popen('./run_bg.sh', shell=True)
    #p2.wait()

if __name__ == '__main__':
    ind_v = '{}.{}'.format(str(sys.version_info[0]), str(sys.version_info[1]))
    pyth_v = 'python{}'.format(ind_v)
    if len(sys.argv) == 1:
        print(__doc__)
        exit()
    elif len(sys.argv) == 2:
        if '--help' in sys.argv[1]:
            print(__doc__)
            exit()
        else:
            base_dir = sys.argv[1]
    if os.path.exists(base_dir):
        print("this directory already exists ! Remove it or choose another name")
        exit()
    os_current = platform.system()
    if os_current == 'Linux':
        install_linux(pyth_v, base_dir)
    elif os_current == 'Windows':
        print("Windows version not yet avalaible")
    elif os_current == 'Darwin':
        print("MacOS version not yet avalaible")