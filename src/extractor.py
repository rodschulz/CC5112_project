##################################################
# This receives 2 argument:
# - folder where are stored the json with samples from each image.
# - output folder
# Ex:
#	python extractor.py ./folder/to/data/ ./output/folder/
#
##################################################
import sys
import json
import numpy
import os
import collections
import cv2
import pdb

data = collections.OrderedDict()
stats = {'classes' : []}
sR = 2; sG = 3; sB = 4
R = 0; G = 1; B = 2

##################################################
##### save the color statistics #####
def saveStats(outputFolder):
	dest = outputFolder + 'colorStats.json'
	with open(dest, 'w') as outfile:
		json.dump(stats, outfile)
	print('Stats saved to ' + dest)

def genSampleImage(outputFolder):
	rowsPerColor = 30
	colors = stats['classes']
	cols = 256
	rows = len(colors) * rowsPerColor
	img = numpy.zeros((cols, rows, 3), numpy.uint8)

	for i in range(len(colors)):
		#pdb.set_trace()
		for j in range(i * rowsPerColor, (i + 1) * rowsPerColor):
			for k in range(cols):
				img[k][j] = numpy.array(colors[i]['mean']).astype(int).tolist()[::-1]

	cv2.imwrite(outputFolder + 'sample.png', img, [cv2.cv.CV_IMWRITE_PNG_COMPRESSION, 9])

##################################################
##### calculate the 1st and 2nd orders stats for each color #####
def calculateStats():
	for key in data:
		i = len(stats['classes'])
		stats['classes'].append({'name': key, 'mean': [], 'covariance':[], 'determinant': 0, 'inverse': [], 'sampleCount': 0})
		if not data[key][R] or not data[key][G] or not data[key][B]:
			continue

		stats['classes'][i]['mean'] = [numpy.mean(data[key][R]), numpy.mean(data[key][G]), numpy.mean(data[key][B])]
		stats['classes'][i]['covariance'] = numpy.cov(data[key]).tolist()
		stats['classes'][i]['determinant'] = numpy.linalg.det(stats['classes'][i]['covariance'])
		stats['classes'][i]['sqrtDet'] = numpy.sqrt(stats['classes'][i]['determinant'])
		stats['classes'][i]['inverse'] = numpy.linalg.inv(stats['classes'][i]['covariance']).tolist()
		stats['classes'][i]['sampleCount'] = len(data[key][R])

##################################################
##### data extraction method #####
def extractData(folder):
	for f in os.listdir(folder):
		if f.endswith(".json"):
			with open(folder + '/' + f) as samplesFile:
				samples = json.load(samplesFile)
				for key in data:
					colorSamples = samples[key]
					for sample in colorSamples:
						data[key][R].append(sample[sR])
						data[key][G].append(sample[sG])
						data[key][B].append(sample[sB])

##################################################
##### initialization method #####
def init():
	global data
	data["Black"] = [[], [], []]
	data["Blue"] = [[], [], []]
	data["Green"] = [[], [], []]
	data["Red"] = [[], [], []]
	data["Orange"] = [[], [], []]
	data["Yellow"] = [[], [], []]
	data["White"] = [[], [], []]

##################################################
##### main method #####
def main():
	init()
	extractData(sys.argv[1])
	calculateStats()
	saveStats(sys.argv[2])
	genSampleImage(sys.argv[2])

##################################################
##### call main method #####
if __name__ == '__main__':
	main()