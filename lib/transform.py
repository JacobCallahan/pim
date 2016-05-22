"""A collection of functions related to transforming images."""
from sys import stdout
from random import shuffle
# pylint: disable=C0103, C0325, C0111, E501


def get_y_img_map(im):
    image_map = []
    for x in range(im.width):
        x_list = []
        for y in range(im.height):
            x_list.append(im.getpixel((x, y)))
        image_map.append(x_list)
    return image_map


def scramble_y(im, step=1, group=None):
    img_map = get_y_img_map(im)
    act = True
    for x in range(im.width)[::step]:
        if group:
            if x % group == 0:
                act = False if act else True
            if not act:
                continue
        stdout.write("\rWriting layers %0.2f%%" % (float(x + 1) / im.width * 100))
        curr_list = img_map.pop(0)
        shuffle(curr_list)
        for y in range(im.height):
            im.putpixel((x, y), curr_list.pop(0))
    return im


def flip_y(im, step=1, group=None):
    img_map = get_y_img_map(im)
    act = True
    for x in range(im.width)[::step]:
        if group:
            if x % group == 0:
                act = False if act else True
            if not act:
                continue
        stdout.write("\rWriting layers %0.2f%%" % (float(x + 1) / im.width * 100))
        curr_list = img_map.pop(0)[::-1]
        for y in range(im.height):
            im.putpixel((x, y), curr_list.pop(0))
    return im


def get_x_img_map(im):
    image_map = []
    for y in range(im.height):
        y_list = []
        for x in range(im.width):
            y_list.append(im.getpixel((x, y)))
        image_map.append(y_list)
    return image_map


def scramble_x(im, step=1, group=None):
    img_map = get_x_img_map(im)
    act = True
    for y in range(im.height)[::step]:
        if group:
            if y % group == 0:
                act = False if act else True
            if not act:
                continue
        stdout.write("\rWriting layers %0.2f%%" % (float(y + 1) / im.height * 100))
        curr_list = img_map.pop(0)
        shuffle(curr_list)
        for x in range(im.width):
            im.putpixel((x, y), curr_list.pop(0))
    return im


def flip_x(im, step=1, group=None):
    img_map = get_x_img_map(im)
    act = True
    for y in range(im.height)[::step]:
        if group:
            if y % group == 0:
                act = False if act else True
            if not act:
                continue
        stdout.write("\rWriting layers %0.2f%%" % (float(y + 1) / im.height * 100))
        curr_list = img_map.pop(0)[::-1]
        for x in range(im.width):
            im.putpixel((x, y), curr_list.pop(0))
    return im
