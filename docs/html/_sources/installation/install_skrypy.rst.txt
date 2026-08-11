How to install Skrypy
=====================

Download the installer
----------------------

Download the latest version of the skrypy installer and save in a temporary folder.

`download skrypy (PyQt5) install <https://github.com/montigno/skrypy-pyqt5/archive/refs/heads/main.zip>`__ |br|

..
   `download skrypy (PyQt6) install <https://github.com/montigno/skrypy-pyqt6/archive/refs/heads/main.zip>`__

Install
------- 

#. Open a terminal

#. Go to the temporary folder where the installer is located::

	cd /root/of/your/temporary/folder

#. Unzip the installer::

	unzip skrypy-main.zip

#. Go to the unziped folder::

	cd skrypy-main

#. Make the installer file executable::

	chmod +x install_skrypy_Linux.sh

#. Launch the install::

	./install_skrypy_Linux.sh

   .. tip::

	**Do not do** 'sh install_skrypy_Linux.sh'. |br|
	**Installation folder [/home/user_name/Applications]** : press Enter to select the default folder or type your installation folder path. |br|

   .. NOTE::

	This installs your virtual environment with some Python packages (Numpy, Matplotlib, ...).

#. To launch Skrypy:

	- type skrypy on Terminal.
	- or use the Skrypy launcher in the Applications menu.

.. # define a hard line break for HTML
.. |br| raw:: html

   <br />
