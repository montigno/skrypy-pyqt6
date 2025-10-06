How to install Skrypy
=====================

Download the installer
----------------------

Download the latest version of the skrypy installer and save in a temporary folder.

`download skrypy install <https://github.com/montigno/skrypy/archive/refs/heads/main.zip>`__

Install
------- 

#. Open a terminal

#. Go to the temporary folder where the installer is located::

	cd /root/of/your/temporary/folder

#. Unzip the installer::

	unzip skrypy-main.zip

#. Go to the unziped folder::

	cd skrypy-main

#. Launch the install::

	python3.12 setup.py /home/user/Applications/skrypy_venv

   .. tip::

	**python3.12**: choose the version of Python (see `requirements chapter <https://montigno.github.io/skrypy/html/installation/requirements.html>`__). |br|
	**setup.py**: contains the installation code. |br|
	**/home/user/Applications/skrypy_venv**: specify the installation path of your virtual environment. |br|

   .. NOTE::

	At the end of this step, 3 aliases are created in your OS's .bashrc file (312 as Python version). |br|
	**skrypy_312** to launch Skrypy. |br|
	**skrypy_312_install** for installing Python packages. |br|
	**skrypy_312_test** to test that skrypy is working properly. |br|

#. Reload .bashrc::

	source ~/.bashrc

#. Install packages::

	skrypy_312_packages

   .. NOTE::

	This installs all packages written in Python (TensorFlow, Numpy, etc...) in your virtual environment.

   .. attention::
	It takes a little time and will take up about 10GB.

Test
----

#. To test if Skrypy is working, type in the terminal::

	skrypy_312_test


.. # define a hard line break for HTML
.. |br| raw:: html

   <br />
