Troubleshooting
===============


Bugs with Qt
------------

1. Error with "xcb":

   .. |pic1| image:: ../ressources/Bug_Qt6.png
      :width: 100%
      :alt: (bug Qt6)

|pic1|

   Solution::

	sudo apt-get install -y libxcb-cursor-dev


Bug with Matlab
---------------

	To check if Matlab is recognized: |br|
	- go to the blocks library, drag the 'start_matlab' block. |br| 
	- run (click+R).

	If there is no error message, Matlab is recognized correctly.

	If the message 'no module Matlab' appears, go to chapter `How to install dependicies <https://montigno.github.io/skrypy/html/installation/install_dependencies.html#matlab-engine>`__.

.. # define a hard line break for HTML
.. |br| raw:: html

   <br />
