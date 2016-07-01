"""A collection of functions related to transforming images."""
from helpers import pixel_value_limit, tuple_average
from PIL import Image
from random import shuffle
from sys import stdout
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


def blend_pixels(pix1, pix2, method='average'):
    new_pix = []
    for i in pix1:
        if method == 'average':
            new_pix.append(tuple_average(pix1[i], pix2[i]))
        elif method == 'sum':
            new_pix.append(pix1[i] + pix2[i])
        elif method == 'subtract':
            new_pix.append(pix1[i] - pix2[i])
        elif method == 'multiply':
            new_pix.append(pix1[i] * pix2[i])
        elif method == 'divide':
            new_pix.append(pix1[i] / pix2[i])
    return pixel_value_limit(tuple(new_pix))


def blend_images(im1, im2, method='average'):
    # make then the same size
    if im1.size > im2.size:
        im1.resize(im2.size)
    elif im2.size > im1.size:
        im2.resize(im1.size)
    # perform the image blend
    for x in range(im1.width):
        stdout.write("\rBlending layers %0.2f%%" % (float(x + 1) / im1.width * 100))
        for y in range(im1.height):
            pix1 = im1.getpixel((x, y))
            pix2 = im2.getpixel((x, y))
            im1.putpixel((x, y), blend_pixels(pix1, pix2, method))
    return im1


def double_image_size(im):
    new_im = Image.new(im.mode, (im.width * 2, im.height * 2))
    for y in range(im.height):
        for x in range(im.width):
            new_im.putpixel((x * 2, y * 2), im.getpixel((x, y)))
    return new_im
