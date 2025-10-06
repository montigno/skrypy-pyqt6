Requirements
============

Python
------
.. important::
   First of all, you should carefully select the correct Python 3 version (3.6 to 3.12) to install the Skrypy virtual environment. |br|
   If you plan to use `the Matlab engine <https://www.mathworks.com/help/matlab/matlab-engine-for-python.html>`__, you should check `the supported versions <https://fr.mathworks.com/support/requirements/python-compatibility.html>`__. |br|
   Otherwise it is recommended to use at least Python3.12 version.

If you don't have Python3 or not the right version, you can try this method::

	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt-get update
	sudo apt-get install python3.x # x the chosen version between 6 and 12

Miniconda
---------

Some dependencies require miniconda to be installed.

#. To install::

	cd /home/user/Applications
	mkdir miniconda3
	cd miniconda3
	wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
	bash Miniconda3-latest-Linux-x86_64.sh

#. Close your terminal and reopen it

#. To test::

	conda list
	conda init fish

#. To update::

	conda update conda

#. To activate conda::

	conda activate

#. To deactivate conda::

	conda deactivate


SSHPass
-------

SSHPass is an utility which allows to provide the ssh password non-interactivly::

	sudo apt install sshpass



.. # define a hard line break for HTML
.. |br| raw:: html

   <br />

