import csv


class genCsv:
    def __init__(self, filename, headers):
        self.file = open(filename, 'wt')
        self.filename = filename
        self.f_csv = csv.DictWriter(self.file, headers)
        self.f_csv.writeheader()
        pass

    # def write_header(self):
    #

    def write_data(self, row):
        self.f_csv.writerow(row)

    def file_close(self):
        self.file.close()