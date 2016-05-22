"""Includes some functions to help throughout the project."""

def str_to_list(str_val, delim=","):
    if "[" in str_val:
        str_val = str_val.replace("[", "")
    if "]" in str_val:
        str_val = str_val.replace("]", "")
    if " " in str_val:
        str_val = str_val.replace(" ", "")
    return [int(x) for x in str_val.split(delim)]


def str_to_tuple(str_val, delim=","):
    if "(" in str_val:
        str_val = str_val.replace("(", "")
    if ")" in str_val:
        str_val = str_val.replace(")", "")
    if " " in str_val:
        str_val = str_val.replace(" ", "")
    return tuple([int(x) for x in str_val.split(delim)])
