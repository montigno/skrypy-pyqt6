class Print_type_var:
    """
    Prints the type of variable to the terminal with a specified message from comment port.

    Args:
        comment: (string) your comment
        inString: (all type) your variable whatever the type

    Returns:

    Note:
        GUI: no
    """
    def __init__(self, comment='', in_var=''):
        print(comment, type(in_var))

##############################################################################


class Print_str:
    """
    Prints the the character string to the terminal with a specified message from comment port.

    Args:
        comment: (string) your comment
        inString: (string) string

    Returns:

    Note:
        GUI: no
    """
    def __init__(self, comment='', in_String='', **options):
        from prompt_toolkit import print_formatted_text, ANSI
        if 'line_return' in options:
            if options['line_return']:
                print('change!')
                in_String = str(in_String).replace(r'\n', '\n').replace('b', '')
        print_formatted_text(ANSI('\x1b[38;2;200;0;250m' + comment))
        print_formatted_text(ANSI('\x1b[38;2;200;0;250m{}'.format(in_String)))

##############################################################################


class Print_int:
    """
    Prints the integer number to the terminal with a specified message from comment port.

    Args:
        comment: (string) your comment
        inInt: (integer) integer number

    Returns:

    Note:
        GUI: no
    """
    def __init__(self, comment='', inInt=0):
        from prompt_toolkit import print_formatted_text, ANSI
        print_formatted_text(ANSI('\x1b[38;2;0;100;255m' + comment))
        print_formatted_text(ANSI('\x1b[38;2;0;100;255m{}'.format(inInt)))

##############################################################################


class Print_float:
    """
    Prints the floating number to the terminal with a specified message from comment port.

    Args:
        comment: (string) your comment
        inFloat: (float) float number

    Returns:

    Note:
        GUI: no
    """
    def __init__(self, comment='', inFloat=0.0):
        from prompt_toolkit import print_formatted_text, ANSI
        print_formatted_text(ANSI('\x1b[38;2;200;100;0m' + comment))
        print_formatted_text(ANSI('\x1b[38;2;200;100;0m{}'.format(inFloat)))

##############################################################################


class Print_path:
    """
    Prints file/directory path to the terminal with a specified message from comment port.

    Args:
    comment: (string) your comment
    inPath: (path) file/directory paths

    Returns:

    Note:
        GUI: no
    """
    def __init__(self, comment='', inPath='path'):
        from prompt_toolkit import print_formatted_text, ANSI
        print_formatted_text(ANSI('\x1b[38;2;255;100;100m' + comment))
        print_formatted_text(ANSI('\x1b[38;2;255;100;100m{}'.format(inPath)))

##############################################################################


class Print_bool:
    """
    Prints the boolean value to the terminal with a specified message from comment port.

    Args:
        comment: (string) your comment
        inBool: (boolean) boolean value

    Returns:

    Note:
        GUI: no
    """
    def __init__(self, comment='', inBool=True):
        from prompt_toolkit import print_formatted_text, ANSI
        print_formatted_text(ANSI('\x1b[38;2;50;250;50m' + comment))
        print_formatted_text(ANSI('\x1b[38;2;50;250;50m{}'.format(inBool)))

##############################################################################


class Print_dict:
    """
    Prints the dictionary structure to the terminal with a specified message from comment port.

    Args:
        comment: (string) your comment
        inBool: (dict) dictionary structure

    Returns:

    Note:
        GUI: no
    """
    def __init__(self, comment='', in_dict={}):
        from prompt_toolkit import print_formatted_text, ANSI
        print_formatted_text(ANSI('\x1b[38;2;200;250;0m' + comment))
        print_formatted_text(ANSI('\x1b[38;2;200;250;0m{}'.format(in_dict)))

##############################################################################


class Print_tuple:
    """
    Prints the tuple structure to the terminal with a specified message from comment port.

    Args:
        comment: (string) your comment
        inString: (tuple) tuple

    Returns:

    Note:
        GUI: no
    """
    def __init__(self, comment='', in_tuple=('',)):
        from prompt_toolkit import print_formatted_text, ANSI
        print_formatted_text(ANSI('\x1b[38;2;200;180;180m' + comment))
        print_formatted_text(ANSI('\x1b[38;2;180;180;180m{}'.format(in_tuple)))

#############################################################################


class Print_json():
    def __init__(self, json_file_in='path'):
        import json
        with open(json_file_in) as f:
            outJson = json.load(f)
        json_formatted = json.dumps(outJson, indent=2)
        print(json_formatted)
