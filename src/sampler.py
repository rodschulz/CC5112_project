##################################################
# This receives 1 argument:
# - location of the image to be sampled
# Ex:
#	python sampler.py ./path/to/image
#
##################################################
import sys
import json
import pdb
from PyQt4.QtGui import *
from PyQt4.QtCore import *

img = None
color = None
flag = {}
data = {}
destination = ''
imgContainer = None


##################################################
def getPixelData(event):
	global data
	global img
	global imgContainer

	x = event.pos().x()
	y = event.pos().y() 
	rgb = QColor(img.pixel(x, y)).toRgb()
	r = rgb.red()
	g = rgb.green()
	b = rgb.blue()

	print('[' +str(x) + ',' + str(y) + '] => [' + str(r) + ', ' + str(g) + ', ' + str(b) + '] (' + color + ')')

	# update image to show the already selected pixels
	value = qRgb(flag[color][0],flag[color][1], flag[color][2] )
	img.setPixel(x, y, value)
	imgContainer.setPixmap(QPixmap.fromImage(img))


	data[color].append([x, y, r, g, b])

##################################################
def colorChanged(event):
	global color
	color = str(event)

##################################################
def saveSamples(event):
	print('Saving data to ' + destination)
	with open(destination, 'w') as outfile:
		json.dump(data, outfile)

##################################################
class Sampler(QWidget):
	def __init__(self, imgLocation):
		super(Sampler, self).__init__()
		self.initUI(imgLocation)
		self.initDict()

	def initUI(self, imgLocation):
		global img
		global color
		global data
		global imgContainer

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
		pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
		img = pixmap.toImage()
		imgContainer = QLabel(self)
		imgContainer.setPixmap(pixmap)

		imgw = pixmap.size().width()
		imgh = pixmap.size().height()
		data['width'] = imgw
		data['height'] = imgh

		# set callbacks and show the image
		imgContainer.mousePressEvent = getPixelData
		combo.activated[str].connect(colorChanged)

		# set sizes and geometry and show
		combo.move(margin, margin)
		button.move(combo.size().width(), margin)
		imgContainer.move(margin, toolbar + margin)
		
		self.setGeometry(300, 300, imgw + margin * 2, imgh + margin * 2 + toolbar)
		self.setWindowTitle('Image')
		self.show()

	def initDict(self):
		global data
		global flags

		data["Black"] = []
		flag["Black"] = [0,0,0]

		data["Blue"] = []
		flag["Blue"] = [0,0,255]

		data["Green"] = []
		flag["Green"] = [0,255,0]

		data["Orange"] = []
		flag["Orange"] = [255,165,0]

		data["Red"] = []
		flag["Red"] = [255,0,0]

		data["White"] = []
		flag["White"] = [255,255,255]

		data["Yellow"] = []
		flag["Yellow"] = [255,255,0]

##################################################
def main():
	global destination
	name = sys.argv[1][sys.argv[1].rfind('/') + 1:]
	destination = './samples/' + name.replace('.', '_') + '.json'

	app = QApplication(sys.argv)
	splr = Sampler(sys.argv[1])
	sys.exit(app.exec_())


##################################################
if __name__ == '__main__':
	main()