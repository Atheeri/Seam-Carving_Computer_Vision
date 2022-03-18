import sys

import cv2 as cv 
import numpy as np
from scipy import ndimage 
import seam_carving as s
from PIL import Image


def loadimage(filename):
    img = cv.imread(cv.samples.findFile(filename))
    #RGB_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    return img #RGB_img

def obj_remove(img , mask_f):
    src = np.array(img)
    mask = mask_f #np.array(Image.open(mask_f).convert('L'))
    new_img = s.remove_object(src, drop_mask=mask, keep_mask=None)
    return new_img

def energy(img):
    src = np.array(img)
    h, w, c = src.shape
    backward = s.resize(src, (w - 200, h))
    forward = s.resize(src, (w - 200, h), energy_mode='forward')
    return backward , forward

if __name__ == '__main__':

    if not len(sys.argv) == 5:
       print("Wrong input")
       exit()
       
    OriginalImg = loadimage(sys.argv[1])

    if sys.argv[2] == "energy":
       new_im1 , new_im2  = energy(OriginalImg)
       cv.imwrite(sys.argv[3], new_im1)
       cv.imwrite(sys.argv[4], new_im2)

    elif sys.argv[2] == "remove":
        mask = np.array(Image.open(sys.argv[3]).convert('L'))
        new_im = obj_remove(OriginalImg , mask)
        cv.imwrite(sys.argv[4], new_im)
    else:
        print("Check your inputs arguments please")

        
