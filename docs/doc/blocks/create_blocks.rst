How to create a block
=====================

This page explains how to create a new block in the library.

   .. |pic1| image:: ../ressources/explorer_modules.png
      :width: 30%
      :alt: (skrypy buttons)

   .. |pic2| image:: ../ressources/Blocks_library_sum.png
      :width: 20%
      :alt: (arrow)

   .. |pic3| image:: ../ressources/explorer_modules_pcnn.png
      :width: 30%
      :alt: (order processes)

   .. |pic4| image:: ../ressources/Blocks_library_spat.png
      :width: 20%
      :alt: (order processes cluster)

   .. |pic5| image:: ../ressources/Blocks_library_pcnn.png
      :width: 20%
      :alt: (order processes cluster)

   .. |pic6| image:: ../ressources/block_explain1.jpg
      :width: 60%
      :alt: (skrypy buttons)

   .. |pic7| image:: ../ressources/block_explain2.jpg
      :width: 60%
      :alt: (arrow)

   .. |pic8| image:: ../ressources/explorer_modules_pcnn_options.png
      :width: 30%
      :alt: (arrow)

The source codes
----------------

All blocks in the library are written in Python and are located in the 'root_of_skrypy_venv/skrypy/NodeEditor/modules' folder. |br|

|pic1| ' ' |pic2|

|pic3| ' ' |pic4| ' ' |pic5|

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

	def out_result(self:"array_float")
	    return self.result

Here is the list of types::

	def out_result(self: "int")
	def out_result(self: "float")
        def out_result(self: "str")
        def out_result(self: "bool")
        def out_result(self: "path")
        def out_result(self: "dict")
        def out_result(self: "tuple")
        def out_result(self: "list_int")
        def out_result(self: "list_float")
        def out_result(self: "list_str")
        def out_result(self: "list_bool")
        def out_result(self: "list_path")
        def out_result(self: "array_int")
        def out_result(self: "array_float")
        def out_result(self: "array_str")
        def out_result(self: "array_bool")
        def out_result(self: "array_path")


The options
-----------

Options are stored in joint yaml files

|pic8|

If you open the .yaml file, you find a list of options with default values. |br|
You can also add comments (except for Nipype modules, in which case the comments are taken directly from the help()). |br|

Options are managed in the block source codes::

	class myfunction():
	    def __init__(self, a=[0], b=1.55, **options):
		
