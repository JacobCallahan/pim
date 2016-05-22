# pim
Python Image Manipulator
========================

Description
-----------
Pim is a simple program to perform some interesting image manipulations.
Current functionality includes:
 - Flipping along X and/or Y axis.
 - Sorting by color, lightness, and color frequency.
 - Unhiding any transparent pixels.
 - Randomizing pixel colors.
 - Applying an averaged grayscale.

Usage
-----
Run pim as you would normally run any python script (e.g.```python pim.py <args>```).
pim has an argument set that can be queried with the ```-h``` or ```---help``` flag.
pim will default to a sort by frequency if no action is specified. Also, it will save
the new file as <oldname>_pim if a new file path is not provided.
pim allows you to run as many actions on an image as you would like. To specify more than one
modifier, seprate each one with a comma (no spaces).

**Examples:**
 - ```python pim.py '/home/user/Pictures/picmorphs/testimg.jpg' -g```
 - ```python pim.py '/home/user/Pictures/picmorphs/testimg.jpg' -s -m color```
 - ```python pim.py '/home/user/Pictures/picmorphs/testimg.jpg' -n '/home/user/Pictures/picmorphs/testimg_srgu.jpg' -s -r -g -u```
 - ```python pim.py '/home/user/Pictures/picmorphs/testimg.jpg' -n '/home/user/Pictures/picmorphs/testimg_groupxy10.jpg' -t x,y --modifier flip --group 10 --step 2```
 - ```python pim.py 'testimg.jpg' -c "(100,50,0)" --spread 10 --strength 50```
 - ```python pim.py 'testimg.jpg' -c [0,2] --spread 100 --strength 50```
 - ```python pim.py 'testimg.jpg' -c "cyan" --spread 70```
 - ```python pim.py 'testimg.jpg' --highlights --shadows --strength 100 --spread 100```

Actions and Modifiers
---------------------
**sort** - Sort an image's pixels by the specified modifier.
 * Modifiers
   * freq (default) - Sorts by most to least frequently used color.
   * color - Sorts by color value.
   * lightness - Sorts from darkest to lightest pixels.

**transform** - Rearranges an image by the specified values and modifiers.
 * Values
   * x (default) - Rearranges the image along the X axis.
   * y - Rearranges the image along the Y axis.
 * Modifiers
   * flip - Reverse the pixel order along the specified axis.
   * scramble - Randomly rearrange the pixel order along the specified axis.
 * Flags
   * --step - How many lines to skip during a tranform.
   * --group - How many lines to group together during a transform.

**color-change** - changes value of the specified target color.
 * Values
   * An rgb tuple in quotes. "(120,45,230)"
   * A positional list of colors to modify. [0,2] will change red and blue.
   * Text value of the 6 main colors. "red", "green", "blue", "yellow", "cyan", "magenta"
 * Flags
   * --strength - How much to change the color by. Max 255. Can be negative.
   * --spread - How far to look in either direction for your color range (max 255).

**grayscale** - Make the image grayscale.

**hide** - Make the specified color transparent (only on supported image types)
 * Values
   * An rgb tuple in quotes. "(120,45,230)"
   * A positional list of colors to modify. [0,2] will change red and blue.
   * Text value of the 6 main colors. "red", "green", "blue", "yellow", "cyan", "magenta"

**unhide** - Make all alpha values maxed (only on supported image types).

**randomize** - Randomly change every pixel color. Use --strength to change intensity.

**highlights** - Enhance the image's hihglights. Set modifiers for spread and strength.
 * Flags
   * --strength - How much to change the color by. Max 255. Can be negative.
   * --spread - How far to look in either direction for your color range (max 255).

**shadows** - Enhance the image's hihglights. Set modifiers for spread and strength.
 * Flags
   * --strength - How much to change the color by. Max 255. Can be negative.
   * --spread - How far to look in either direction for your color range (max 255).

**lightness** - Make the image lighter or darker. Use --strength to specify how much.
 * Flags
   * --strength - How much to change the color by. Max 255. Can be negative.

Sample gallery
--------------
 * http://imgur.com/a/UXkqr
