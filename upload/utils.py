def the_file_is_csv(filename):
    ext = filename.split('.')
    if len(ext) == 1:
        return False
    return ext[-1] == 'csv'