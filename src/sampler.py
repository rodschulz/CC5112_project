##################################################
# This receives 1 argument:
# - location of the image to be sampled
# Ex:
#	python sampler.py ./path/to/images/
#
##################################################
import sys
import json
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

flag = {}
data = {}


##################################################
class Sampler(QWidget):
    output = ''
    area = []
    image = None
    color = None
    label = None

    def __init__(self, src, output):
        super(Sampler, self).__init__()
        self.output = output
        self.initUI(src)
        self.initDict()

    def initUI(self, imgLocation):
        global data

        margin = 2
        toolbar = 30

        button = QPushButton('Save', self)
        button.clicked.connect(self.saveSamples)

        # create a combobox to select the which will be taken samples
        combo = QComboBox(self)
        combo.addItem("Black")
        combo.addItem("Blue")
        combo.addItem("Green")
        combo.addItem("Red")
        combo.addItem("White")
        combo.addItem("Yellow")

        # set the selected index and get the selected color
        combo.setCurrentIndex(0)
        self.color = str(combo.currentText())

        # load the image, generate a label and put the image in it
        pixmap = QPixmap(imgLocation)
        pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.image = pixmap.toImage()
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)

        imgw = pixmap.size().width()
        imgh = pixmap.size().height()
        data['width'] = imgw
        data['height'] = imgh

        # set callbacks and show the image
        self.label.mousePressEvent = self.getPixelData
        combo.activated[str].connect(self.colorChanged)

        # set sizes and geometry and show
        combo.move(margin, margin)
        button.move(combo.size().width(), margin)
        self.label.move(margin, toolbar + margin)

        self.setGeometry(300, 300, imgw + margin * 2, imgh + margin * 2 + toolbar)
        self.setWindowTitle('Image')
        self.show()

    ##################################################
    def initDict(self):
        global data
        global flags

        data["Black"] = []
        flag["Black"] = [0, 0, 0]

        data["Blue"] = []
        flag["Blue"] = [0, 0, 255]

        data["Green"] = []
        flag["Green"] = [0, 255, 0]

        data["Red"] = []
        flag["Red"] = [255, 0, 0]

        data["White"] = []
        flag["White"] = [255, 255, 255]

        data["Yellow"] = []
        flag["Yellow"] = [255, 255, 0]

    ##################################################
    def saveSamples(self, event):
        dest = self.output

        try:
            folder = dest[:dest.rfind('/') + 1]
            if not os.path.exists(folder):
                os.makedirs(folder)

            with open(dest, 'w') as outfile:
                json.dump(data, outfile)
                print('Samples saved to ' + dest)

        except IOError as e:
            print('Unnable to save samples')

    ##################################################
    def colorChanged(self, event):
        self.color = str(event)

    ##################################################
    def getPixelData(self, event):
        global data

        x = event.pos().x()
        y = event.pos().y()
        self.area.append([x, y])

        value = qRgb(flag[self.color][0], flag[self.color][1], flag[self.color][2])

        # if there's 2 points, then add the whole zone to the data
        if len(self.area) == 2:
            xi = min(self.area[0][0], self.area[1][0] + 1)
            xf = max(self.area[0][0], self.area[1][0] + 1)
            yi = min(self.area[0][1], self.area[1][1] + 1)
            yf = max(self.area[0][1], self.area[1][1] + 1)

            print('zone [' + str(xi) + ',' + str(yi) + '][' + str(xf) + ',' + str(yf) + ']  => ' + self.color)

            for i in range(xi, xf):
                for j in range(yi, yf):
                    rgb = QColor(self.image.pixel(i, j)).toRgb()
                    r = rgb.red()
                    g = rgb.green()
                    b = rgb.blue()
                    data[self.color].append([i, j, r, g, b])

                    self.image.setPixel(i, j, value)

            # update image to show the already selected pixels
            self.label.setPixmap(QPixmap.fromImage(self.image))
            # reset list with the zone limits
            self.area = []


##################################################
def main():
    name = sys.argv[1][sys.argv[1].rfind('/') + 1:]
    dest = './samples/' + name.replace('.', '_') + '.json'
    src = sys.argv[1]

    app = QApplication(sys.argv)
    sampler = Sampler(src, dest)
    sys.exit(app.exec_())


##################################################
if __name__ == '__main__':
    main()
