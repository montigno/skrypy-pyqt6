class bool_to_list_dyn():
    def __init__(self, bool_in=True, **dynamicsInputs):
        self.out = [bool_in]
        for di in dynamicsInputs:
            self.out.append(dynamicsInputs[di])

    def list_bool(self: 'list_bool'):
        return self.out

#############################################################################
