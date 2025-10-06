class json_open_file():
    def __init__(self, json_file='path'):
        import json
        with open(json_file) as f:
            self.outJson = json.load(f)

    def dict_json(self: 'dict'):
        return self.outJson

##############################################################################


class json_save_file():
    def __init__(self, data={}, json_file_out='path'):
        import json
        with open(json_file_out, 'w') as outfile:
            json.dump(data, outfile)
        self.json_file_out = json_file_out

    def json_out_file(self: 'path'):
        return self.json_file_out

##############################################################################


class json_add_element():
    def __init__(self, json_file='path', data={}):
        import json
        with open(json_file, 'r') as outfile:
            data_raw = json.load(outfile)
        data_raw.update(data)
        with open(json_file, 'w') as outfile:
            json.dump(data_raw, outfile)
        self.json_file = json_file

    def json_out_file(self: 'path'):
        return self.json_file

##############################################################################
