def is_dict_valid(d, keys):
    """
    Return True if the given dictionary (d) contains the correct keys (list) 
    (no more, no less).
    """
    for key in d.keys():
        if not key in keys:
            return False
    for key in keys:
        if not key in d.keys():
            return False
    return True