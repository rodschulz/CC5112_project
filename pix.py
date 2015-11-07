import sys
import json
from PyQt4.QtGui import *
from PyQt4.QtCore import *

##################################################
##### Global variables
imgw = 800 
imgh = 600
img = None
color = None
data = {}
dest = ''

##################################################
##### Store the data of the clicked pixel
def getPixelData(event):
	global data

	x = event.pos().x()
	y = event.pos().y() 
	rgb = QColor(img.pixel(x, y)).toRgb()
	r = rgb.red()
	g = rgb.green()
	b = rgb.blue()

	print('[' +str(x) + ',' + str(y) + '] => [' + str(r) + ', ' + str(g) + ', ' + str(b) + '] (' + color + ')')

	data[color].append([x, y, r, g, b])

##################################################
##### Register the currently selected color
def colorChanged(event):
	global color
	color = str(event)

##################################################
##### Register the currently selected color
def saveSamples(event):
	print('Saving data to ' + dest)
	with open(dest, 'w') as outfile:
    		json.dump(data, outfile)

##################################################
##### Main app

class Sampler(QWidget):
	def __init__(self, imgLocation):
		super(Sampler, self).__init__()
		self.initUI(imgLocation)
		self.initDict()

	def initUI(self, imgLocation):
		global img
		global color

		margin = 2
		toolbar = 30

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
		pixmap = QPixmap(imgLocation)
		pixmap = pixmap.scaled(imgw, imgh, Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
		img = pixmap.toImage()
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

	def initDict(self):
		global data
		data["Black"] = []
		data["Blue"] = []
		data["Green"] = []
		data["Orange"] = []
		data["Red"] = []
		data["White"] = []
		data["Yellow"] = []

##################################################
##### main method #####
def main():
	global dest
	name = sys.argv[1][sys.argv[1].rfind('/') + 1:]
	dest = './output/' + name.replace('.', '_') + '.json'
	print(dest)

	app = QApplication(sys.argv)
	splr = Sampler(sys.argv[1])
	sys.exit(app.exec_())


##################################################
##### call main method #####
if __name__ == '__main__':
	main()