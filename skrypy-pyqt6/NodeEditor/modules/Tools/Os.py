class os_environ:
    def __init__(self):
        import os
        self.dict_env = os.environ

    def os_environ(self: 'dict'):
        return self.dict_env

###############################################################################


class projet_path:
    """
    Returns the path of the current diagram.

    Args:

    Returns:
        projet_path: (path) path file of diagram

    Note:
        GUI: no
    """
    def __init__(self):
        from NodeEditor.python.Diagram_Editor import getPathWork
        self.proj_path = getPathWork().pathWork()
        print("current projet path = ", self.proj_path)

    def projet_path(self: 'path'):
        return self.proj_path

###############################################################################


class separator_path:
    def __init__(self):
        import os
        self.separator = os.sep

    def out_sep(self: 'str'):
        return self.separator
