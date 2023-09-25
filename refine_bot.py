from purchase_bot import *
import cv2
import numpy as np
import pyautogui
import time
import random
from typing import List
from PIL import Image


class refineBot():
    def __init__(self, parent=None):
        """!
        @brief      Constructs a new instance.

        """
        self.screen = cv2.cvtColor(np.array(pyautogui.screenshot(region = SCREEN_REGION)), cv2.COLOR_BGR2GRAY)

# in the end of the refine process, "get premium" will come out

if __name__ == '__main__':

    rBot = refineBot()
