import random

def the_file_is_csv(filename):
    ext = filename.split('.')
    if len(ext) == 1:
        return False
    return ext[-1] == 'csv'

def random_string_generator(length):
    """
    Generate random string of passed length.
    """
    string = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password = "".join(random.sample(string, length))
    return password
