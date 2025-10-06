class csv_open_file:
    """
    CSV File Reading.

    Args:
        file: (path) path of CSV file

    Returns:
        array_csv: (string array) string array contained in the CSV file

    Note:
        GUI: no
        link_web: https://docs.python.org/3/library/csv.html
                        (click Ctrl + U)
    """
    def __init__(self, file='path', access="enumerate(('row', 'column'))", **options):
        import csv
        self.res = []
        if 'quoting' in options.keys():
            options['quoting'] = ['csv.QUOTE_ALL',
                                  'csv.QUOTE_MINIMAL',
                                  'csv.QUOTE_NONE',
                                  'csv.QUOTE_NONNUMERIC'].index(options['quoting'])
        with open(file) as csvfile:
            reader = csv.reader(csvfile, **options)
            for row in reader:
                self.res.append(row)

        if access == 'column':
            self.res = list(map(list, zip(*self.res)))

    def array_csv(self: 'array_str'):
        return self.res

##############################################################################


class csv_save_file:
    """
    CSV File Writting.

    Args:
        file_output: (path) path of the out CSV file
        header: (list of str) headers of the table
        data: (array of float or int or str)

    Returns:
        csv_out: (path) path of the saved CSV file

    Note:
        GUI: no
        link_web: https://docs.python.org/3/library/csv.html
                        (click Ctrl + U)
    """
    def __init__(self, file_output='path', header=[''], data=[['']], **options):
        import csv
        delimiter = ','
        if 'transpose' in options:
            if options['transpose']:
                data = list(map(list, zip(*data)))
        if 'delimiter' in options:
            delimiter = options['delimiter']
        with open(file_output, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter)
            if header[0]:
                writer.writerow(header)
            writer.writerows(data)
        self.out_f = file_output

    def csv_out(self: 'path'):
        return self.out_f

##############################################################################


class csv_reader_text:
    """
    CSV text Reading.

    Args:
        txt: (string) text in CSV format

    Returns:
        array_csv: (string array) string array contained in the text

    Note:
        GUI: no
        link_web: https://docs.python.org/3/library/csv.html
                        (click Ctrl + U)
    """
    def __init__(self, txt='', **options):
        import csv
        self.res = []
        if 'quoting' in options.keys():
            options['quoting'] = ['csv.QUOTE_ALL',
                                  'csv.QUOTE_MINIMAL',
                                  'csv.QUOTE_NONE',
                                  'csv.QUOTE_NONNUMERIC'].index(options['quoting'])
        reader = csv.reader(txt.split('\n'), **options)
        for row in reader:
            self.res.append(row)

    def array_csv(self: 'array_str'):
        return self.res

##############################################################################


class csv_txt_to_array():
    def __init__(self, csv_in=''):
        import csv
        reader = csv.reader(csv_in, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:  # each row is a list
            self.output.append(row)

    def out_array(self: 'array_float'):
        return self.output
