# File: GrayscaleImage.py

"""
This program displays an image together with its grayscale equivalent.
"""

from pgl import GWindow, GImage

# Constants

GWINDOW_WIDTH = 500
GWINDOW_HEIGHT = 400
IMAGE_FILENAME = "images/ColorWheel.png"
IMAGE_SEP = 50

# Main program

def GrayscaleImage():
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    image = GImage(IMAGE_FILENAME)
    gw.add(image, (gw.getWidth() - IMAGE_SEP) / 2 - image.getWidth(),
                  (gw.getHeight() - image.getHeight()) / 2)
    grayscale = createGrayscaleImage(image)
    gw.add(grayscale, (gw.getWidth() + IMAGE_SEP) / 2,
                      (gw.getHeight() - image.getHeight()) / 2)

def createGrayscaleImage(image):
    """
    Creates a grayscale image based on the luminance of each pixel
    """
    array = image.getPixelArray()
    height = len(array)
    width = len(array[0])
    for i in range(height):
        for j in range(width):
            gray = luminance(array[i][j])
            array[i][j] = GImage.createRGBPixel(gray, gray, gray)
    return GImage(array)

def luminance(pixel):
    """
    Returns the luminance of a pixel, which indicates its subjective
    brightness.  This implementation uses the NTSC formula.
    """
    r = GImage.getRed(pixel)
    g = GImage.getGreen(pixel)
    b = GImage.getBlue(pixel)
    return round(0.299 * r + 0.587 * g + 0.114 * b)

# Startup code

if __name__ == "__main__":
    GrayscaleImage()
