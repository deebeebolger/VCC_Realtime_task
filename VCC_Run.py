import os
import sys
import numpy as np
from screeninfo import get_monitors
from AppKit import NSApp
from VCC_Utils import *

if __name__ == "__main__":

    args = sys.argv

    monitors_name = [] # Initialize the list of monitor names
    M = get_monitors()
    for M in get_monitors():
        print(f"Screen name is {M.name}\n Screen width is {M.width}\n Screen height is {M.height}\n")

        if str(args[1]) == "VCC_images":

            begin_VCC_images(args[2], args[3], 12)    # Call of function to begin experiment

        elif str(args[1]) == "VCC_video":
            begin_VCC_video()            # Call of function to play the introductory video

