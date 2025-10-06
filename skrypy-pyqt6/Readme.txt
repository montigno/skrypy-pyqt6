How to install skrypy:
	- download skrypy_install.zip

	In terminal:
	- unzip skrypy_install.zip
	- python3.11 setup.py ~/Applications/skrypy_venv
	- cd
	- source .bashrc
	- skrypy_install

*********************************************************************************************************************

How to install python packages:

	In terminal:
	- cd ~/Applications/skrypy_venv
	- source bin/activate
	- pip3 install <your package>
	
	Or in skrypy:
	- go to the menu 'Configuration' then 'Packages manager'

*********************************************************************************************************************

How to install RS2: (see https://github.com/VitoLin21/Rodent-Skull-Stripping)

	download RS2 : https://github.com/VitoLin21/Rodent-Skull-Stripping/archive/refs/heads/main.zip
	
	In terminal:
	- conda create -n rss python=3.9
	- conda activate rss
	- # CUDA 11.7
	  conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 pytorch-cuda=11.7 -c pytorch -c nvidia
	- # CUDA 11.8
	  conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 pytorch-cuda=11.8 -c pytorch -c nvidia
	- # CPU Only
	  conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 cpuonly -c pytorch
	- cd your_folder_where_'Rodent-Skull-Stripping-main.zip'_was_downloaded/
	- unzip Rodent-Skull-Stripping-main.zip
	- cd Rodent-Skull-Stripping-main
	- pip install -r requirements.txt
	- python setup.py install
	- pip install blosc2
	- copy all the files from "Rodent-Skull-Stripping-main/RS2/jsons" to "your_conda_path/envs/rss/lib/python3.9/site-packages/RS2-1.0-py3.9.egg/RS2/jsons"

*********************************************************************************************************************

How to install matlab_engine: 

	for MATLAB < R2022b:
	- cd ~/Applications/skrypy_venv
	- source bin/activate
	- cd <matlabroot>/MATLAB/R2021a/extern/engines/python
	- python3 setup.py build --build-base ~/Applications/skrypy_venv/build install
	- exit

	for MATLAB >= R2022b:
	- cd ~/Applications/skrypy_venv
	- source bin/activate
	- export LD_LIBRARY_PATH=<matlabroot>/MATLAB/R2024b/bin/glnxa64/
	- python3 -m pip install matlabengine==24.2.2
	- exit

*********************************************************************************************************************

Codecov:
	- cd ~/Applications/skrypy_venv
	- source bin/activate
	- pip3 install coverage (if not yet done)
	- cd skrypy
	- coverage run testunit.py
	- coverage report -m

*********************************************************************************************************************

Error messages:

	"ModuleNotFoundError: No module named 'pip._vendor.pyproject_hooks'"
			- cd ~/Applications/skrypy_venv
			- source bin/activate
			- curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
			- python get-pip.py --force-reinstall
			
	if error with a module (eg "cannot import name 'projections' from 'matplotlib'")
			- cd ~/Applications/skrypy_venv
			- source bin/activate
			- pip3 uninstall module_name (eg matplotlib)
			- pip3 install module_name (eg matplotlib)