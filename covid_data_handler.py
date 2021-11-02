def parse_csv_data(csv_filename):
    f = open(csv_filename).read().split("\n") ## open and process file by line
    f.pop(-1) ## Remove Blank line
    return f

