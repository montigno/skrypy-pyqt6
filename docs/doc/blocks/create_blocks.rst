How to create a block
=====================

This page explains how to create your own blocks in the library.

.. important::
   When adding new blocks, back up the 'module' folder. |br|

   .. |pic1| image:: ../ressources/explorer_modules.png
      :width: 25%
      :alt: (skrypy buttons)

   .. |pic2| image:: ../ressources/Blocks_library_sum.png
      :width: 20%
      :alt: (arrow)

   .. |pic3| image:: ../ressources/explorer_modules_interp.png
      :width: 20%
      :alt: (order processes)

   .. |pic4| image:: ../ressources/Blocks_library_interp.png
      :width: 25%
      :alt: (order processes cluster)

   .. |pic6| image:: ../ressources/block_explain1.png
      :width: 80%
      :alt: (skrypy buttons)

   .. |pic7| image:: ../ressources/block_explain2.png
      :width: 80%
      :alt: (arrow)

   .. |pic8| image:: ../ressources/explorer_modules_interp_options.png
      :width: 20%
      :alt: (arrow)

The source codes
----------------

All blocks in the library are written in Python and are located in the 'root_of_skrypy_venv/skrypy/NodeEditor/modules' folder. |br|

|pic1| ' ' |pic2|

|pic3| ' ' |pic4|

If you open a .py file, you find a list of classes. |br|
A block corresponds to a simple Python class. |br|

|pic6|
|pic7|


.. # define a hard line break for HTML
.. |br| raw:: html

   <br />


Function parameters
-------------------

You must define default values ​​for parameters in the function definition::

	def __init__(self, a=[0], b=1.55, c="title", img="path"):
	The term 'path' is used to specify that it is a file or directory path, and also represents a null value.

Function return types
---------------------

For function returns, it is necessary to add annotations and specify the type::

	def out_result(self) -> list[float]:
	    return self.result

Here is the list of types::

	def out_result(self) -> int:			(integer)
	def out_result(self) -> float:			(float)
        def out_result(self) -> str:			(string)
        def out_result(self) -> bool:			(boolean)
        def out_result(self) -> None:			(path)
        def out_result(self) -> dict:			(dictionary)
        def out_result(self) -> tuple:			(tuple)
        def out_result(self) -> list[int]:		(list of integer)
        def out_result(self) -> list[float]:		(list of float)
        def out_result(self) -> list[str]:		(list of str)
        def out_result(self) -> list[bool]:		(list of boolean)
        def out_result(self) -> list[None]:		(list of path)
        def out_result(self) -> list[list[int]]:	(array of integer)
        def out_result(self) -> list[list[float]]:	(array of float)
        def out_result(self) -> list[list[str]]:	(array of str)
        def out_result(self) -> list[list[bool]]:	(array of boolean)
        def out_result(self) -> list[list[None]]:	(array of path)


The options
-----------

Options are stored in joint yaml files

|pic8|

If you open the .yaml file, you find a list of options with default values. |br|
You can also add comments (except for Nipype modules, in which case the comments are taken directly from the help()). |br|

Options are managed in the block source codes::

	class myfunction():
	    def __init__(self, a=[0], b=1.55, **options):
		
