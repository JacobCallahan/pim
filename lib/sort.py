"""A collection of functions related to sorting images."""
from sys import stdout
# pylint: disable=C0103, C0325, C0111, E501


def pixel_sum_wght(pix):
    px_sum = int("{}{}{}".format(
        "00{}".format(pix[0])[-3:],
        "00{}".format(pix[1])[-3:],
        "00{}".format(pix[2])[-3:],
    ))
    if len(pix) == 4:
        px_sum += pix[3]
    return px_sum


def pixel_sum(pix):
    px_sum = pix[0] + pix[1] + pix[2]
    if len(pix) == 4:
        px_sum += pix[3]
    return px_sum


def get_pixel_list(im):
    pixel_list = []
    for x in range(im.width):
        for y in range(im.height):
            pixel_list.append(im.getpixel((x, y)))
    return pixel_list


def sort_by_color(im):
    pixel_list = get_pixel_list(im)
    reds = greens = blues = rg = gb = rb = gray = []
    for px in pixel_list:
        if px[0] > px[1] and px[0] > px[2]:
            reds.append(px)
        elif px[1] > px[0] and px[1] > px[2]:
            greens.append(px)
        elif px[2] > px[0] and px[2] > px[0]:
            blues.append(px)
        elif px[0] == px[1] == px[2]:
            gray.append(px)
        elif px[0] == px[1]:
            rg.append(px)
        elif px[0] == px[2]:
            rb.append(px)
        elif px[1] == px[2]:
            gb.append(px)
    output = []
    for group in [reds, rg, greens, gb, blues, rb, gray]:
        output.extend(sorted(group))
    return output


def sort_by_lightness(im):
    print ("Getting pixel list.")
    pixel_list = get_pixel_list(im)
    print ("Sorting pixel list.")
    return sorted(pixel_list, key=pixel_sum)


def sort_by_freq(im):
    pixel_dict = {}
    for x in range(im.width):
        for y in range(im.height):
            pixel = im.getpixel((x, y))
            if pixel in pixel_dict:
                pixel_dict[pixel] += 1
            else:
                pixel_dict[pixel] = 1
    print ("Found {} total colors.".format(len(pixel_dict)))
    output = []
    for item in sorted(pixel_dict, key=pixel_dict.get, reverse=True):
        output.extend([item] * pixel_dict[item])
    return output


def fill_pic(im, pixel_list):
    tmp = pixel_list[:im.width * 250]
    pixel_list = pixel_list[im.width * 250:]
    for y in range(im.height):
        stdout.flush()
        stdout.write("\rWriting layers %0.2f%%" % (float(y + 1) / im.height * 100))
        buff = tmp[:im.width]
        tmp = tmp[im.width:]
        if len(tmp) == 0:
            tmp = pixel_list[:im.width * 250]
            pixel_list = pixel_list[im.width * 250:]
        for x in range(im.width):
            im.putpixel((x, y), buff.pop(0))
    return im
