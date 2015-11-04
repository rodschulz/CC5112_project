import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

##################################################
##### Global variables
im = None
color = None
dest = None

##################################################
##### Store the data of the clicked pixel
def getPixelData(event):
	x = event.pos().x()
	y = event.pos().y() 
	rgb = QColor(im.pixel(x, y)).toRgb()

	print('[' +str(x) + ',' + str(y) + '] => [' + str(rgb.red()) + ', ' + str(rgb.green()) + ', ' + str(rgb.blue()) + '] (' + color + ')')

##################################################
##### Register the currently selected color
def colorChanged(event):
	global color
	color = str(event)

##################################################
##### Main app

# generate app
app = QApplication(sys.argv)

# load the image, generate a label and put the image in it
pixmap = QPixmap('test.tiff')
pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
im = pixmap.toImage()
label = QLabel()
label.setPixmap(pixmap)

# set title, callback and show the image
label.setWindowTitle('Train image')
label.mousePressEvent = getPixelData
label.show()

# create a combobox to select the which will be taken samples
combo = QComboBox()
combo.addItem("Black")
combo.addItem("Blue")
combo.addItem("Green")
combo.addItem("Orange")
combo.addItem("Red")
combo.addItem("White")
combo.addItem("Yellow")

# set the selected index and get the selected color
combo.setCurrentIndex(0)
color = str(combo.currentText())

# set callback and show the combobox
combo.activated[str].connect(colorChanged)  
combo.show()

# wait until the image dialog is closed
sys.exit(app.exec_())