from subprocess import Popen, PIPE
import subprocess


def install(command):
    p = subprocess.Popen(command, shell=True)
    p.wait()


install('pip install --upgrade pip')
install('pip3 install --ignore-installed PyYAML')

# this import must stay here !
from Config import Config

pack = Config().getPathLibraries()

for keypk, valpk in pack.items():
    try:
        print('\033[93m'+'checking ', keypk, end=' : ')
        print('\033[0m')
        install('pip3 install ' + valpk)
        print('\033[0m')
    except Exception as e:
        print('error : ', e)

install('pip3 install --upgrade --force-reinstall pyqt5')
