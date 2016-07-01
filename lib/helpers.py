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


def tuple_average(tuple1, tuple2):
    if len(tuple1) == len(tuple2):
        new_tuple = []
        for i in range(len(tuple1)):
            new_tuple.append((tuple1[i] + tuple2[i]) / 2)
        return tuple(new_tuple)


def pixel_value_limit(pixel):
    for val in pixel:
        val = 0 if val < 0 else val
        val = 255 if val > 255 else val
    return pixel
