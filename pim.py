"""Just some random image manipulations."""
import argparse
from PIL import Image
from lib import color, helpers, sort, transform
# pylint: disable=C0103, C0325, C0111, E501
# todo: resize images


def pim(f_path, n_path=None, actions=['sort'], modifiers=['freq'], col=[0],
        h_col=None, step=1, group=None, strength=20, spread=0):
    """Main function for the python image manipulator.

    f_path: path to the image file.
    n_path: path to save the new image.
    action: what to perform on the image.
    modifiers: any modifiers available to the action.
    col: target color for color-based actions.
    step: number of lines to skip, if applicable.
    group: number of lines to group together, if applicable.
    strength: an integer value, can sometimes be neagtive.
    spread: integer denoting how wide a range is acceptable for matching color.
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
        im = color.unhide(im)

    if 'hide' in actions:
        im = color.change_color(
            im, color=h_col, ch_func=[color.hide], spread=spread, alpha=True)

    if 'randomize' in actions:
        im = color.randomize(im, strength)

    if 'grayscale' in actions:
        im = color.make_gray(im)

    if 'lightness' in actions:
        im = color.change_color(
            im, ch_func=[color.change_lightness], strength=strength)

    if 'highlights' in actions:
        im = color.change_color(
            im, ch_func=[color.enhance_highlights], spread=spread, strength=strength)

    if 'shadows' in actions:
        im = color.change_color(
            im, ch_func=[color.enhance_shadows], spread=spread, strength=strength)

    if 'color-change' in actions:
        im = color.change_color(im, color=col, spread=spread, strength=strength)

    if 'sort' in actions:
        if 'freq' in modifiers or not modifiers:
            print ("sorting by freq")
            im = sort.fill_pic(im, sort.sort_by_freq(im))
        if 'color' in modifiers:
            print ("sorting by color")
            im = sort.fill_pic(im, sort.sort_by_color(im))
        if 'light' in modifiers:
            print ("sorting by lightness")
            im = sort.fill_pic(im, sort.sort_by_lightness(im))

    if 'transform' in actions:
        if 'flip' in modifiers or not modifiers:
            if 'y' in modifiers:
                print ("flipping the image along the y axis")
                im = transform.flip_y(im, step, group)
            if 'x' in modifiers:
                print ("flipping the image along the x axis")
                im = transform.flip_x(im, step, group)
        if 'scramble' in modifiers:
            if 'y' in modifiers:
                print ("scrambling the image along the y axis")
                im = transform.scramble_y(im, step, group)
            if 'x' in modifiers:
                print ("scrambling the image along the x axis")
                im = transform.scramble_x(im, step, group)

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
        help="Sort an image. Use the --modifier flag to set modifiers (color, lightness, freq).")
    parser.add_argument(
        "-t", "--transform", type=str,
        help="Transform an image by axis (x, y). Use the --modifier flag to "
        "set modifiers (flip, scramble).")
    parser.add_argument(
        "-c", "--color-change", type=str,
        help="Make changes to the colors in an image. See readme for accepted values. "
        "Use the correct flags to set spread and strength.")
    parser.add_argument(
        "-m", "--modifier", type=str,
        help="Set modifiers for --sort and --transform.")
    parser.add_argument(
        "-g", "--grayscale", action="store_true",
        help="Make the image grayscale.")
    parser.add_argument(
        "-l", "--lightness", action="store_true",
        help="Make the image lighter or darker. Use --strength to specify how much.")
    parser.add_argument(
        "--hide", type=str,
        help="Make the specified color transparent (only on supported image types).")
    parser.add_argument(
        "-u", "--unhide", action="store_true",
        help="Make all alpha values maxed (only on supported image types).")
    parser.add_argument(
        "-r", "--randomize", action="store_true",
        help="Randomly change every pixel color. Use --strength to change intensity.")
    parser.add_argument(
        "--highlights", action="store_true",
        help="Enhance the image's hihglights. Set modifiers for spread and strength.")
    parser.add_argument(
        "--shadows", action="store_true",
        help="Enhance the image's shadows. Set modifiers for spread and strength.")
    parser.add_argument(
        "--strength", type=int,
        help="Usage depends on what you are calling. Sometimes can be negative.")
    parser.add_argument(
        "--step", type=int,
        help="How many lines to skip in a transform.")
    parser.add_argument(
        "--group", type=int,
        help="How many lines to group together in a transform.")
    parser.add_argument(
        "--spread", type=int,
        help="How far to look in either direction for your color range (max 255).")

    args = parser.parse_args()
    modifiers = ['freq'] if not args.modifier else args.modifier.split(",")

    actions = []
    col = h_col = None
    if args.transform:
        actions.append('transform')
        modifiers.extend(args.transform.split(","))
    if args.unhide:
        actions.append('unhide')
    if args.randomize:
        actions.append('randomize')
    if args.grayscale:
        actions.append('grayscale')
    if args.hide:
        if "[" in args.hide:
            h_col = helpers.str_to_list(args.hide)
        elif "(" in args.hide:
            h_col = helpers.str_to_tuple(args.hide)
        else:
            h_col = args.hide
        actions.append('hide')
    if args.lightness:
        actions.append('lightness')
    if args.highlights:
        actions.append('highlights')
    if args.shadows:
        actions.append('shadows')
    if args.color_change:
        if "[" in args.color_change:
            col = helpers.str_to_list(args.color_change)
        elif "(" in args.color_change:
            col = helpers.str_to_tuple(args.color_change)
        else:
            col = args.color_change
        actions.append('color-change')
    if args.sort or not actions:
        actions.append('sort')

    step = 1 if not args.step else args.step
    strength = 1 if not args.strength else args.strength
    spread = 0 if not args.spread else args.spread

    pim(f_path=args.path, n_path=args.new_path, actions=actions,
        modifiers=modifiers, step=step, group=args.group, col=col,
        h_col=h_col, strength=strength, spread=spread)
