# -*- coding: utf-8 -*-

"""This is an example of a plugin with the minimal code needed for proper functioning.

The plugin file and class names must be the same.
The class name can start with the uppercase.
The class must contain the argument 'diagram' which contains the structure of the pipeline.

This plugin only displays the content of the argument 'diagram' in the terminal.
"""


class Myworkflow():

    def __init__(self, diagram, modules_path):
        super().__init__()

        print(type(self).__name__, 'is started')
        print(diagram)
        print()
        print(modules_path)
