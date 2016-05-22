"""Miscellaneous functions and toys that don't fit into the rest of pim."""
from PIL import Image
from sys import stdout
# pylint: disable=C0103, C0325, C0111


def all_colors(name='AllColors'):
    im = Image.new('RGB', (4096, 4096))
    r = g = b = 0
    for y in range(im.height):
        stdout.write("\rWriting layers %0.2f%%" % (float(y + 1) / im.height * 100))
        for x in range(im.width):
            im.putpixel((x, y), (r, g, b))
            r += 1
            if r > 255:
                r = 0
                g += 1
                if g > 255:
                    g = 0
                    b += 1
    im.save('{}.png'.format(name))
