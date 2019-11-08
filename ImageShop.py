# File: ImageShop.py

"""
This program is the ImageShop program with Reset button extension
"""

from filechooser import chooseInputFile
from pgl import GWindow, GImage, GRect, GButton
from GrayscaleImage import createGrayscaleImage, luminance

# Constants

GWINDOW_WIDTH = 1024
GWINDOW_HEIGHT = 700
BUTTON_WIDTH = 125
BUTTON_HEIGHT = 20
BUTTON_MARGIN = 10
BUTTON_BACKGROUND = "#CCCCCC"

# Derived constants

BUTTON_AREA_WIDTH = 2 * BUTTON_MARGIN + BUTTON_WIDTH
IMAGE_AREA_WIDTH = GWINDOW_WIDTH - BUTTON_AREA_WIDTH

# The ImageShop application

def ImageShop():
    def addButton(label, action):
        """
        Adds a button to the region on the left side of the window
        """
        nonlocal nextButtonY
        x = BUTTON_MARGIN
        y = nextButtonY
        button = GButton(label, action)
        button.setSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        gw.add(button, x, y)
        nextButtonY += BUTTON_HEIGHT + BUTTON_MARGIN

    def setImage(image):
        """
        Sets image as the current image after removing the old one.
        """
        nonlocal currentImage
        if currentImage is not None:
            gw.remove(currentImage)
        currentImage = image
        x = BUTTON_AREA_WIDTH + (IMAGE_AREA_WIDTH - image.getWidth()) / 2
        y = (gw.getHeight() - image.getHeight()) / 2
        gw.add(image, x, y)
        

    def loadButtonAction():
        """Callback function for the Load button"""
        nonlocal Ofilename
        filename = chooseInputFile()
        if filename != "":
            Ofilename = filename
            setImage(GImage(filename))
    
    def resetAction():
        """Callback function for the Reset button"""
        if Ofilename != "":
            setImage(GImage(Ofilename))
    
    def flipVerticalAction():
        """Callback function for the Flip Vertical button"""
        if currentImage is not None:
            setImage(flipVertical(currentImage))
    
    def rotateLeftAction():
        """Callback function for the Rotate Left button"""
        if currentImage is not None:
            setImage(rotateLeft(currentImage))
    
    def rotateRightAction():
        """Callback function for the Rotate Right button"""
        if currentImage is not None:
            setImage(rotateRight(currentImage))
    
    
    def flipHorizontalAction():
        """Callback function for the Flip Horizontal button"""
        if currentImage is not None:
            setImage(flipHorizontal(currentImage))
    
    def grayscaleImageAction():
        """Callback function for the Grayscale button"""
        if currentImage is not None:
            setImage(createGrayscaleImage(currentImage))
    
    def greenScreenAction():
        """Callback function for the Green Screen button"""
        if currentImage is not None:
            filenameGreen = chooseInputFile()
            if filenameGreen != "":
                setImage(GreenScreen(currentImage, GImage(filenameGreen)))
   
    def equalizerAction():
        """Callback function for the Equalizer button"""
        if currentImage is not None:
            setImage(equalizer(currentImage))
            
    def flipHorizontal(image):
        array = image.getPixelArray()
        for row in array:
            row.reverse()
        return GImage(array)
    
    def flipVertical(image):
        array = image.getPixelArray()
        return GImage(array[::-1])
        
    def rotateLeft(image):
        array = image.getPixelArray()
        for row in array:
            row.reverse()
        resultArray = transpose(array)
        return GImage(resultArray)
            
    def rotateRight(image):
        array = image.getPixelArray()
        resultArray = transpose(array)
        for row in resultArray:
            row.reverse()
        return GImage(resultArray)
            
    def transpose(lists):
        result = [[lists[j][i] for j in range(len(lists))] for i in range(len(lists[0]))]
        return result
    
    def imageHistogram(imageArray):
        """Converts an image array into a histogram"""
        histogram = [0 for i in range(256)]
        for row in imageArray:
            for entry in row:
                luminanceP = luminance(entry)
                histogram[luminanceP] += 1
        return histogram
    
    def cumulativeHistogram(nHistogram):
        """Converts a histogram into a cumulative histogram"""
        cHistogram = [nHistogram[0]]
        for i in range(1, 256):
            cHistogram.append(nHistogram[i] + cHistogram[i-1])
        return cHistogram
    
    def equalizer(image):
        """Equalizes the image using the cumulative histogram on image array histogram"""
        array = image.getPixelArray()
        cHistogram = cumulativeHistogram(imageHistogram(array))
        totalPixels = len(array)*len(array[0])
        for i in range(len(array)):
            for j in range(len(array[0])):
                oldLum = luminance(array[i][j])
                newLum = round(255*cHistogram[oldLum]/totalPixels)
                array[i][j] = GImage.createRGBPixel(newLum, newLum, newLum)
        return GImage(array)
    
    def GreenScreen(mainImage, GreenImage):
        mainArray = mainImage.getPixelArray()
        greenArray = GreenImage.getPixelArray()
        for i in range(min(len(greenArray), len(mainArray))):
            for j in range(min(len(greenArray[0]), len(mainArray[0]))):
                pixel = greenArray[i][j]
                if GImage.getGreen(pixel) < (2*max(GImage.getBlue(pixel), GImage.getRed(pixel))): #Condition for Green Screen check
                    mainArray[i][j] = pixel
        return GImage(mainArray)
    
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    buttonArea = GRect(0, 0, BUTTON_AREA_WIDTH, GWINDOW_HEIGHT)    
    buttonArea.setFilled(True)
    buttonArea.setColor(BUTTON_BACKGROUND)
    gw.add(buttonArea)
    nextButtonY = BUTTON_MARGIN
    currentImage = None
    Ofilename = ""
    addButton("Load", loadButtonAction)
    addButton("Flip Vertical", flipVerticalAction)
    addButton("Flip Horizontal", flipHorizontalAction)
    addButton("Rotate Left", rotateLeftAction)
    addButton("Rotate Right", rotateRightAction)
    addButton("Grayscale", grayscaleImageAction)
    addButton("Green Screen", greenScreenAction)
    addButton("Equalizer", equalizerAction)
    addButton("Reset", resetAction) #This is part of my extension


# Startup code

if __name__ == "__main__":
    ImageShop()