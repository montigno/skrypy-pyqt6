Troubleshooting
===============


Bugs with Qt
------------

1. Error with "xcb":

   .. |pic1| image:: ../ressources/Bug_Qt5.png
      :width: 100%
      :alt: (bug Qt5)

|pic1|

   Solution::

	sudo apt install \
		libxcb-cursor0 \
		libxcb-xinerama0 \
		libxcb-render0 \
		libxcb-render-util0 \
		libxcb-shape0 \
		libxcb-randr0 \
		libxcb-image0 \
		libxcb-keysyms1 \
		libxcb-icccm4 \
		libxcb-sync1 \
		libxcb-xfixes0 \
		libxkbcommon-x11-0


Bug with Skrypy update
----------------------

	Git must be installed, see `here <https://montigno.github.io/skrypy-pyqt5/html/installation/requirements.html#git-required>`__.


Bug with Cluster connection
---------------------------

	sshpass must be installed, see `here <https://montigno.github.io/skrypy-pyqt5/html/installation/requirements.html#sshpass-required>`__. |br|

	Test the user@host_name connection in a terminal::

		ssh user@host_name


Bug with missing package or module
----------------------------------

	If it is a Python package that needs to be installed using pip, see `How to install Python packages <https://montigno.github.io/skrypy-pyqt5/html/installation/package_install.html>`__. |br|
	If it concerns another dependency, see `How to install dependencies <https://montigno.github.io/skrypy-pyqt5/html/installation/install_dependencies.html>`__. |br|

Bug with Matlab
---------------

	To check if Matlab is recognized: |br|
	- go to the blocks library, drag the 'start_matlab' block. |br| 
	- run (click+R).

	If there is no error message, Matlab is recognized correctly.

	If the message 'no module Matlab' appears, go to chapter `How to install dependicies <https://montigno.github.io/skrypy-pyqt5/html/installation/install_dependencies.html#matlab-engine>`__.

.. # define a hard line break for HTML
.. |br| raw:: html

   <br />
