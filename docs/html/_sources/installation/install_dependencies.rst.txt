How to install dependencies
===========================

Environment variables
---------------------
.. important::
   Skrypy needs to point programs to specific versions of dependencies. |br|
   The .bashrc file is in principle sufficient, but it has been found that when processing on a cluster, it does not always load. |br|
   The best solution is to edit the file **'env_parameters.txt'** which is located in the hidden folder **/home/username/.skrypy/**. |br|
   Skrypy takes care of concatenating the 'PATH' variable.

`ANTs <https://github.com/ANTsX/ANTs>`__
----------------------------------------

#. Download from the `site <https://github.com/ANTsX/ANTs/releases>`__ (choose according to your OS version)

#. Decompress in a folder (e.g /home/user/Applications/)

#. Edit **'env_parameters.txt'** and add::
	
	#ANTs
	export PATH=ants_root/ants-2.5.0/bin
	export ANTSPATH=ants_root/ants-2.5.0/bin

________________________________________________________________

`AFNI <https://afni.nimh.nih.gov/>`__
-------------------------------------

#. See `install <https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/background_install/install_instructs/index.html>`__

#. Edit **'env_parameters.txt'** and add::

	#fsl
	export PATH=afni_root/abin

________________________________________________________________

`FSL <https://fsl.fmrib.ox.ac.uk/fsl/docs/#/>`__
------------------------------------------------

#. See `install <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation>`__

#. Edit **'env_parameters.txt'** and add::

	#FSL
	export PATH=fsl_root/fsl/bin
	sh fsl_root/fsl/etc/fslconf/fsl.sh

________________________________________________________________

`ImageJ <https://imagej.net/ij/>`__
-----------------------------------

#. Download ImageJ `here <https://imagej.net/ij/download.html>`__ 

#. Unzip and put in a directory (eg /home/user/Applications)

#. Edit **'env_parameters.txt'** and add::

	#ImageJ
	export PATH=imagej_root/ImageJ/

________________________________________________________________

`Matlab <https://www.mathworks.com/products/matlab.html>`__
-----------------------------------------------------------

#. Edit **'env_parameters.txt'** and add::

	export PATH=matlabroot/MATLAB/R2024b/bin
	export MATLABCMD=matlabroot/MATLAB/R2024b/bin/glnxa64/MATLAB
	export MATLABPATH=/home/username/MATLAB/ *

	* directory where your pathdef.m (user-specific) is located 

________________________________________________________________


`Matlab engine <https://www.mathworks.com/help/matlab/matlab-engine-for-python.html>`__
---------------------------------------------------------------------------------------

#. For MATLAB < R2022b::

	source skrypy_root/skrypy_venv/bin/activate
	cd matlabroot/MATLAB/R2021a/extern/engines/python
	python3 setup.py build --build-base ~/Applications/skrypy_venv/build install
	exit

#. For MATLAB >= R2022b::

        source skrypy_root/skrypy_venv/bin/activate
	export LD_LIBRARY_PATH=<matlabroot>/MATLAB/R2024b/bin/glnxa64/
	python3 -m pip install matlabengine==24.2.2
	exit	

________________________________________________________________

`MRTrix3 <https://mrtrix.readthedocs.io/en/latest/installation/build_from_source.html>`__
-----------------------------------------------------------------------------------------

#. Required dependencies::

	sudo apt-get install git g++ python libeigen3-dev zlib1g-dev libqt5opengl5-dev libqt5svg5-dev libgl1-mesa-dev libfftw3-dev libtiff5-dev libpng-dev

#. Choose or create a directory where MRTrix3 will be installed (eg /home/user/Applications):

#. In this directory, type::

	git clone https://github.com/MRtrix3/mrtrix3.git
	cd mrtrix3
	./configure
	./build
	./set_path
	
#. Close the terminal and start another one::

	mrview

#. Edit **'env_parameters.txt'** and add::

	# MRtrix3
	export PATH=mrtrix_root/mrtrix3/bin
	export PATH=mrtrix_root/mrtrix3/mrdegibbs3D/bin

________________________________________________________________

`RS2 <https://github.com/VitoLin21/Rodent-Skull-Stripping>`__
-------------------------------------------------------------

#. Download RS2 `here <https://github.com/VitoLin21/Rodent-Skull-Stripping/archive/refs/heads/main.zip>`__
#. Save it in a temporary folder
#. In terminal::

	conda create -n rss python=3.9
	conda activate rss
	# CUDA 11.7
	conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 pytorch-cuda=11.7 -c pytorch -c nvidia
	# CUDA 11.8
	conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 pytorch-cuda=11.8 -c pytorch -c nvidia
	# CPU Only
	conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 cpuonly -c pytorch
	cd <your_temporary_folder>
	unzip Rodent-Skull-Stripping-main.zip
	cd Rodent-Skull-Stripping-main
	pip install -r requirements.txt
	python setup.py install
	pip install blosc2

#.  copy all the files from "Rodent-Skull-Stripping-main/RS2/jsons" to "your_conda_path/envs/rss/lib/python3.9/site-packages/RS2-1.0-py3.9.egg/RS2/jsons"

________________________________________________________________

`SPM (requires MATLAB) <https://www.fil.ion.ucl.ac.uk/spm/>`__
--------------------------------------------------------------

#. Download SPM12 `here <https://www.fil.ion.ucl.ac.uk/spm/docs/installation/>`__

#. Uncompress the zip file and put the directory 'SPM12' in the 'toolbox' folder of your Matlab (eg /usr/local/MATLAB/R2024b/toolbox/)

#. In terminal::

	cd matlab_root/MATLAB/R2024b/toolbox/local/
	sudo nano pathdef.m

#. find the line %%% BEGIN ENTRIES %%% and add to the line below: matlabroot,'/toolbox/spm12:', ...::

	%%% BEGIN ENTRIES %%%
	matlabroot,'/toolbox/spm12:', ...

#. Save it

#. Edit **'env_parameters.txt'** and add::

	#SPM12
	export SPM_PATH=matlab_root/MATLAB/R2024b/toolbox/spm12/

Configuration example
------------------------

To give an idea, here is a configuration of **env_parameters.txt** file::

	#ImageJ
	export PATH=/home/olivier/Applications/ImageJ/

	#Matlab
	export PATH=/home/Apps/MATLAB/R2024b/bin
	export MATLABCMD=/home/Apps/MATLAB/R2024b/bin/glnxa64/MATLAB
	export MATLABPATH=/home/olivier/Documents/MATLAB/

	#FSL
	export PATH=/home/olivier/Applications/fsl/bin
	sh /home/olivier/Applications/fsl/etc/fslconf/fsl.sh

	#ANTs
	export PATH=/home/olivier/Applications/ants-2.5.0
	export ANTSPATH=/home/olivier/Applications/ants-2.5.0

	#MRTrix3
	export PATH=/home/olivier/Applications/mrtrix3/bin

	#FreeSurfer
	export FREESURFER_HOME=/usr/local/freesurfer

	#AFNI
	export PATH=/home/olivier/abin

	#SPM
	export PATH=/usr/local/MATLAB/R2020a/toolbox/spm12

	#mri_conv
	export MRIFilePATH=/home/olivier/Applications/Java/mri_conv/MRIFileManager/MRIManager.jar


.. # define a hard line break for HTML
.. |br| raw:: html

   <br />

