class open_text_file():
    def __init__(self, text_file_in='path'):
        from pathlib import Path
        self.txt = Path(text_file_in).read_text()

    def out_text(self: 'str'):
        return self.txt

##############################################################################


class read_text_lines():
    def __init__(self, text_file='path'):
        with open(text_file) as f:
            self.lines = f.readlines()

    def list_lines(self: 'list_str'):
        return self.lines

##############################################################################


class save_file_text:

    def __init__(self, text_in='', file_name='path'):
        text_file = open(file_name, "w")
        text_file.write(text_in)
        text_file.close()
