"""A collection of fucntions related to modifying pixel color."""
from sys import stdout
from random import randint
# pylint: disable=C0103, C0325, C0111, E501

COLOR_MAP = {
    'red': [0],
    'green': [1],
    'blue': [2],
    'yellow': [0, 1],
    'cyan': [1, 2],
    'magenta': [0, 2]
}


def change_pixel_color(pixel, color, spread, strength, alpha, coupled=False):
    """Function to change the color values of an individual pixel.

    pixel: a pixel tuple rpresenting (r, g, b) and a if available.
    color: can either be a pixel tuple, a positional list [0, 1, 2, 3], or one
        of the values listed in the COLOR_MAP.
    spread: int - how wide of a range of values are acceptable to match the color.
    strength: int - how much of a value change is desired.
    alpha: bool - if true, then any matching colors will become transparent.
    couplled: bool - if true, then all specified colors must be changed.
    """
    if isinstance(color, str):
        color = COLOR_MAP[color]
        coupled = True
    if len(pixel) == 3:
        r, g, b = pixel
        a = None
    else:
        r, g, b, a = pixel

    if isinstance(color, tuple):
        if (color[0] >= r - spread and color[0] <= r + spread and
                color[1] >= g - spread and color[1] <= g + spread and
                color[2] >= b - spread and color[2] <= b + spread):
            if alpha and a:
                a = 0
            else:
                r, g, b = (r + strength, g + strength, b + strength)
    else:
        if 0 in color and r > g - spread and r > b - spread:
            r += strength
        if 1 in color and g > r - spread and g > b - spread:
            g += strength
        if 2 in color and b > g - spread and b > r - spread:
            b += strength
        # Check to see if colors were changed independently when they should be coupled
        if len([[r, g, b][x] for x in color if [r, g, b][x] != pixel[x]]) != len(color):
            if coupled:
                r, g, b = pixel[:3]
                if a:
                    a = pixel[3]
            elif alpha and a:
                a = 0

    for c in (r, g, b, a):
        if c:
            c = 0 if c < 0 else c
            c = 255 if c > 255 else c

    return (r, g, b, a) if a else (r, g, b)


def change_lightness(pixel, color, spread, alpha, strength=20):
    return change_pixel_color(
        pixel, color=[0, 1, 2], spread=255, strength=strength, alpha=False)


def enhance_highlights(pixel, color, alpha, spread=50, strength=20):
    return change_pixel_color(
        pixel, color=(255, 255, 255), spread=spread, strength=strength, alpha=False)


def enhance_shadows(pixel, color, alpha, spread=50, strength=20):
    return change_pixel_color(
        pixel, color=(0, 0, 0), spread=spread, strength=-strength, alpha=False)


def hide(pixel, color, strength=255, alpha=True, spread=0):
    return change_pixel_color(
        pixel, color=color, spread=spread, strength=-strength, alpha=True, coupled=True)


def unhide(im):
    if not len(im.getpixel((0, 0))) == 4:
        print ("Image has no alpha channel")
        return im
    for x in range(im.width):
        stdout.write("\rUnhiding layers %0.2f%%" % (float(x + 1) / im.width * 100))
        for y in range(im.height):
            pixel = im.getpixel((x, y))
            pixel = (pixel[0], pixel[1], pixel[2], 255)
            im.putpixel((x, y), pixel)
    return im


def change_color(im, color=[0], ch_func=[change_pixel_color], spread=20, strength=20, alpha=True):
    if not len(im.getpixel((0, 0))) == 4:
        alpha = False
    for x in range(im.width):
        stdout.write("\rChanging layers %0.2f%%" % (float(x + 1) / im.width * 100))
        for y in range(im.height):
            pixel = im.getpixel((x, y))
            for func in ch_func:
                pixel = func(
                    pixel, color=color, spread=spread,
                    strength=strength, alpha=alpha
                )
            im.putpixel((x, y), pixel)
    return im


def mut(value, strength):
    min_v = value - strength
    min_v = 0 if min_v < 1 else min_v
    max_v = value + strength
    max_v = 255 if max_v > 255 else max_v
    return randint(min_v, max_v)


def mutate_color(pixel, strength):
    if len(pixel) == 4:  # has transparency
        return (
            mut(pixel[0], strength),
            mut(pixel[1], strength),
            mut(pixel[2], strength),
            mut(pixel[3], strength))
    else:
        return (
            mut(pixel[0], strength),
            mut(pixel[1], strength),
            mut(pixel[2], strength))


def grayscale(pixel):
    avg = (pixel[0] + pixel[1] + pixel[2]) / 3
    if len(pixel) == 4:
        return (avg, avg, avg, pixel[3])
    else:
        return (avg, avg, avg)


def make_gray(im):
    for x in range(im.width):
        stdout.write("\rGraying layers %0.2f%%" % (float(x + 1) / im.width * 100))
        for y in range(im.height):
            pixel = im.getpixel((x, y))
            pixel = grayscale(pixel)
            im.putpixel((x, y), pixel)
    return im


def randomize(im, strength=20):
    for x in range(im.width):
        stdout.write("\rRandomizing layers %0.2f%%" % (float(x + 1) / im.width * 100))
        for y in range(im.height):
            pixel = im.getpixel((x, y))
            pixel = mutate_color(pixel, strength)
            im.putpixel((x, y), pixel)
    return im
