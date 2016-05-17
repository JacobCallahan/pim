""" Just some random image manipulations """
import argparse
from PIL import Image
from random import randint, shuffle
from sys import stdout
# pylint: disable=C0103, C0325, C0111
# todo: replace color


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


def pim(f_path, n_path=None, actions=['sort'], modifiers=['freq'], step=1,
        group=None, strength=20):
    """Main function for the python image manipulator.

        f_path: path to the image file.
        n_path: path to save the new image.
        action: what to perform on the image.
        modifiers: any modifiers available to the action.
        step: number of lines to skip, if applicable.
        group: number of lines to group together, if applicable.
    """
    if not n_path:
        # Contruct a new path to avoiding writing over the original.
        split_path = f_path.split("/")
        image_name = split_path.pop(len(split_path) - 1).split(".")
        image_name = "{}_pim.{}".format(image_name[0], image_name[1])
        if split_path:
            n_path = "{}/{}".format("/".join(split_path), image_name)
        else:
            n_path = image_name
    im = Image.open(f_path)

    if 'unhide' in actions:
        im = unhide(im)

    if 'randomize' in actions:
        im = randomize(im, strength)

    if 'grayscale' in actions:
        im = make_gray(im)

    if 'sort' in actions:
        if 'freq' in modifiers or not modifiers:
            print ("sorting by freq")
            im = fill_pic(im, sort_by_freq(im))
        if 'color' in modifiers:
            print ("sorting by color")
            im = fill_pic(im, sort_by_color(im))
        if 'light' in modifiers:
            print ("sorting by lightness")
            im = fill_pic(im, sort_by_lightness(im))

    if 'transform' in actions:
        if 'flip' in modifiers or not modifiers:
            if 'y' in modifiers:
                print ("flipping the image along the y axis")
                im = flip_y(im, step, group)
            if 'x' in modifiers:
                print ("flipping the image along the x axis")
                im = flip_x(im, step, group)
        if 'scramble' in modifiers:
            if 'y' in modifiers:
                print ("scrambling the image along the y axis")
                im = scramble_y(im, step, group)
            if 'x' in modifiers:
                print ("scrambling the image along the x axis")
                im = scramble_x(im, step, group)

    print ("Saving image as {}".format(n_path))
    im.save(n_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str,
        help="The path to the image (e.g 'images/test.png').")
    parser.add_argument(
        "-n", "--new-path", type=str,
        help="The path to write the new image to (e.g 'images/test_change.png').")
    parser.add_argument(
        "-s", "--sort", action="store_true",
        help="Sort an image. Use the --modifier flag to set a modifiers (color, lightness, freq).")
    parser.add_argument(
        "-t", "--transform", type=str,
        help="Transform an image by axis (x, y). Use the --modifier flag to "
        "set a modifiers (flip, scramble).")
    parser.add_argument(
        "-m", "--modifier", type=str,
        help="Set modifiers for --sort and --transform.")
    parser.add_argument(
        "-g", "--grayscale", action="store_true",
        help="Make the image grayscale.")
    parser.add_argument(
        "-u", "--unhide", action="store_true",
        help="Make all alpha values maxed (only on supported image types).")
    parser.add_argument(
        "-r", "--randomize", action="store_true",
        help="Randomly change every pixel color. Use --strength to change intensity.")
    parser.add_argument(
        "--strength", type=int,
        help="How wide a gap the randomized color can be.")
    parser.add_argument(
        "--step", type=int,
        help="How many lines to skip in a transform.")
    parser.add_argument(
        "--group", type=int,
        help="How many lines to group together in a transform.")

    args = parser.parse_args()
    modifiers = ['freq'] if not args.modifier else args.modifier.split(",")

    actions = []
    if args.transform:
        actions.append('transform')
        modifiers.extend(args.transform.split(","))
    if args.unhide:
        actions.append('unhide')
    if args.randomize:
        actions.append('randomize')
    if args.grayscale:
        actions.append('grayscale')
    if args.sort or not actions:
        actions.append('sort')

    step = 1 if not args.step else args.step
    strength = 1 if not args.strength else args.strength

    pim(f_path=args.path, n_path=args.new_path, actions=actions,
        modifiers=modifiers, step=step, group=args.group, strength=strength)
