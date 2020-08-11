import os, sys 
import xml.etree.ElementTree as ET
from collections import Counter

classes = []
classNameCountArray = []
directory = 'E:/models/research/object_detection/images/train'


# Get a list of all the files ending in .xml
files = os.listdir(directory)
print("Found ", len(files) , " annotations")

# Open a file
firstFile = files[0]

error = ""
# Get the 
for filename_short in files:
    if (not filename_short.endswith(".xml") ):
        print("Skipping invalid XML file", filename_short)
        
    else:
        filename = directory+"/"+filename_short
        tree = ET.parse(filename)
        size = tree.find('size')
        imageWidth = int(size.find('width').text)
        imageHeight = int(size.find('height').text)
        imageArea = imageWidth * imageHeight   

        if ( tree.find('folder').text != "images" ):
            tree.find('folder').text  = "images"
            print("Changing folder name to images")
            error = "folder name ERROR"

        if (".JPG" in tree.find('filename').text ):
            print(filename,"Error .jpg to JPG")
            error = "file format ERROR"

        name = tree.find('object').find('name').text
        if (not (name in classes) ):
            classes.append(name)
        classNameCountArray.append(name)


        boundingBox = tree.find('object').find('bndbox')
        xmin = int( boundingBox.find('xmin').text )
        ymin = int( boundingBox.find('ymin').text )
        xmax = int( boundingBox.find('xmax').text )
        ymax = int( boundingBox.find('ymax').text )


        boxWidth  = xmax - xmin
        boxHeight = ymax - ymin
        boxArea = boxWidth * boxHeight

        # make sure that box size is more than 1%
        if (boxArea < 0.01 * imageArea):
            print(filename, "Too Small object")
            error = "box area ERROR"

        # Make sure that xmin > xmax or ymin > ymax
        if (xmin > xmax or ymin > ymax):
            print(filename,"Invalid Min Max relationship",xmin,xmax,ymin,ymax)
            error = "min and max ERROR"

        # Make sure that xmax < width and ymax < height
        if (xmax > imageWidth or ymax > imageHeight):
            print(filename,"Invalid Limits of Bounding Box",xmin,xmax,ymin,ymax)
            error = "max ERROR"

        # make sure that everything is positive numbers
        if (xmin <= 0 or xmax <= 0 or ymin <= 0 or ymax <= 0):
            print(filename,"Bounding box is zero",xmin,xmax,ymin,ymax)
            error = "zero or not positive ERROR"

print("Found  " + str( len(classes) ) + " Classes = ",classes)
c = Counter(classNameCountArray)
print(c)

if (not error):
    print("SUCCESS!")
sys.exit(error)
