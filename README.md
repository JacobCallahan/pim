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
the new file as <oldnam>_pim if a new file path is not provided.
pim allows you to run as many actions on an image as you would like. To specify more than one
modifier, seprate each one with a comma (no spaces).
Examples:
 - ```python pim.py '/home/user/Pictures/picmorphs/testimg.jpg' -g```
 - ```python pim.py '/home/user/Pictures/picmorphs/testimg.jpg' -s -m color```
 - ```python pim.py '/home/user/Pictures/picmorphs/testimg.jpg' -n '/home/user/Pictures/picmorphs/testimg_srgu.jpg' -s -r -g -u```
 - ```python pim.py '/home/user/Pictures/picmorphs/testimg.jpg' -n '/home/user/Pictures/picmorphs/testimg_groupxy10.jpg' -t x,y --modifier flip --group 10 --step 2```

Sample gallery:
 - http://imgur.com/a/UXkqr
