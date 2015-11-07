import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

##################################################
##### Global variables
im = None
color = None


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
##### Register the currently selected color
def saveSamples(event):
	print('save data!')

##################################################
##### Main app

class Sampler(QWidget):
	def __init__(self):
		super(Sampler, self).__init__()
		self.initUI()

	def initUI(self):
		global im
		global color

		margin = 2
		toolbar = 30
		imgw = 800 
		imgh = 600

		button = QPushButton('Save', self)
        	button.clicked.connect(saveSamples)

		# create a combobox to select the which will be taken samples
		combo = QComboBox(self)
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

		# load the image, generate a label and put the image in it
		pixmap = QPixmap('test.tiff')
		pixmap = pixmap.scaled(imgw, imgh, Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
		im = pixmap.toImage()
		label = QLabel(self)
		label.setPixmap(pixmap)

		# set callbacks and show the image
		label.mousePressEvent = getPixelData
		combo.activated[str].connect(colorChanged)

		# set sizes and geometry and show
		combo.move(margin, margin)
		button.move(combo.size().width(), margin)
		label.move(margin, toolbar + margin)
		
		self.setGeometry(300, 300, imgw + margin * 2, imgh + margin * 2 + toolbar)
		self.setWindowTitle('Train image')
		self.show()

##################################################
##### main method #####
def main():
	app = QApplication(sys.argv)
	splr = Sampler()
	sys.exit(app.exec_())


##################################################
##### call main method #####
if __name__ == '__main__':
	main()