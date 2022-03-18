import sys

from scipy import ndimage
import cv2
import numpy

depth = 3

# increases height and width by adding seams
def increase_dimensions(horizontalSeams, verticalSeams, image):
    solution = image

    if horizontalSeams > 0:
        solution = place_seams(horizontalSeams, solution)

    if verticalSeams > 0:
        solution = numpy.rot90(solution, 1)
        solution = place_seams(verticalSeams, solution)
        solution = numpy.rot90(solution, 3)

    return solution

# decreases height and width by removing seams
def decrease_dimensions(horizontalSeams, verticalSeams, image):
    solution = image

    if horizontalSeams < 0:
        solution = remove_seams(horizontalSeams, solution)

    if verticalSeams < 0:
        solution = numpy.rot90(solution, 1)
        solution = remove_seams(verticalSeams, solution)
        solution = numpy.rot90(solution, 3)

    return solution


def get_prepended_pixels(image, a, b, c):
    return image[a, :b, c]


def get_appended_pixels(image, a, b, c):
    return image[a, b:, c]

# adds seams to image
def place_seam(currentSeam, image):
    height, width, depth = image.shape
    zeroArray = numpy.zeros((height, 1 + width, depth))
    for vertical in range(height):
        horizontal = currentSeam[vertical]
        for color in range(depth):
            if not horizontal == 0:
                avaeragePixel = numpy.average(image[vertical, horizontal - 1: horizontal + 1, color])
                zeroArray[vertical, horizontal, color] = avaeragePixel

                zeroArray[vertical, : horizontal, color] = get_prepended_pixels(image, vertical, horizontal, color)
                zeroArray[vertical, horizontal + 1:, color] = get_appended_pixels(image, vertical, horizontal, color)
            else:
                avaeragePixel = numpy.average(image[vertical, horizontal: horizontal + 2, color])
                zeroArray[vertical, horizontal + 1, color] = avaeragePixel

                zeroArray[vertical, horizontal, color] = image[vertical, horizontal, color]
                zeroArray[vertical, horizontal + 1:, color] = get_appended_pixels(image, vertical, horizontal, color)

    return zeroArray

# creates seam array
def make_seam_index(energyResult, height, zeroArr):
    binaryArr = numpy.ones_like(energyResult, dtype=bool)
    all_seams = []
    b = numpy.argmin(energyResult[-1])
    for a in range(-1, height - 1):
        binaryArr[a, b] = False
        all_seams.append(b)
        b = zeroArr[a, b]

    all_seams.reverse()
    all_seams = numpy.array(all_seams)
    return all_seams, binaryArr

# finds the minimum required seam
def minseam(im):
    height, width = im.shape[:2]

    # energy function
    gradientX = ndimage.convolve1d(im, numpy.array([1, 0, -1]), axis=1, mode='wrap')
    gradientY = ndimage.convolve1d(im, numpy.array([1, 0, -1]), axis=0, mode='wrap')
    energyResult = numpy.sqrt(numpy.sum(gradientX ** 2, axis=2) + numpy.sum(gradientY ** 2, axis=2))
    h, w = 0, 1
    zeroArr = numpy.zeros((height, width), dtype=int)

    for a in range(w, height):
        for b in range(h, width):
            if not b == h:
                Ix = [numpy.argmin(energyResult[a - w, b - w:b + 2])]
                zeroArr[a, b] = Ix[0] + b - w
                minergy = energyResult[a - w, Ix[0] + b - w]
            else:
                Ix = [numpy.argmin(energyResult[a - w, b:b + 2])]
                zeroArr[a, b] = Ix[0] + b
                minergy = energyResult[a - w, Ix[0] + b]

            energyResult[a, b] += minergy

    return make_seam_index(energyResult, height, zeroArr)

# removes seams from image
def remove_seams(n, image):
    removed = 0
    n = - n
    while removed < n:
        mins = minseam(image)
        height, width = image.shape[:2]
        binarymask = numpy.stack([mins[1]] + [mins[1]] + [mins[1]], axis=2)

        image = image[binarymask].reshape((height, width - 1, depth))
        removed += 1

    return image

# makes list of seams
def create_seams_list(image, n):
    seamsList = []
    current_image = numpy.array(image)
    i = 0
    while i < n:
        Ix, binary_im = minseam(current_image)
        seamsList.extend([Ix])
        current_image = current_image[numpy.stack([binary_im] * depth, axis=2)].reshape(
            (current_image.shape[:2][0], current_image.shape[:2][1] - 1, depth))
        i += 1

    seamsList.reverse()
    return seamsList

# adds seam to image
def place_seams(n, image):
    seamsList = create_seams_list(image, n)
    i = 0
    while i < n:
        seam = seamsList[-1]
        seamsList = seamsList[:-1]
        image = place_seam(seam, image)

        for current in seamsList:
            current[numpy.where(current >= seam)] += 2
        i += 1

    return image


if __name__ == '__main__':
    # aruments are inputfile outputfile resizetype horizontalSeams verticalSeams

    if not len(sys.argv) == 6:
        print("Wrong input")
        exit()
    image = cv2.imread(sys.argv[1])
    horizontalSeams = int(sys.argv[4])
    verticalSeams = int(sys.argv[5])

    if sys.argv[3] == "increase":
        output = increase_dimensions(horizontalSeams, verticalSeams, image)
    elif sys.argv[3] == "decrease":
        output = decrease_dimensions(-horizontalSeams, -verticalSeams, image)
    else:
        print("invalid resize type")
        exit()

    cv2.imwrite(sys.argv[2], output)
