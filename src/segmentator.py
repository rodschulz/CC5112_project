##################################################
# This receives 3 arguments:
# - the file holding the stats for every color
# - the folder with the images to process
# - the threshold to use for minimum valid clasification
# Ex:
#	python segmentator.py ./path/to/stats.json ./folder/of/imgs/ threshold
#
##################################################
import sys
import json
import numpy
import os
import cv2
import pdb

stats = {}
colors = []

##################################################
##### calculate the likelihood #####
def getLikelihood(pixel, dimension, mean, covariance, covInverse, covDeterminant):
	delta = numpy.subtract(pixel, mean)
	exponent = numpy.dot(delta, covInverse)
	exponent = numpy.dot(exponent, delta)
	factor = 1 / (numpy.sqrt(pow(2 * numpy.pi, dimension)) * covDeterminant) 
	return factor * numpy.exp(-0.5 * exponent)

##################################################
##### get the color class for each pixel #####
def classify(pixel, threshold):
	colorClass = -1
	maxLikelihood = -1
	k = 0
	for color in colors:
		likelihood = getLikelihood(pixel, len(pixel), color['mean'], color['covariance'], color['inverse'], color['determinant'])

		#pdb.set_trace()

		acc = 0
		for ck in colors:
			acc = acc + getLikelihood(pixel, len(pixel), ck['mean'], ck['covariance'], ck['inverse'], ck['determinant'])

		#pdb.set_trace()
		#print(likelihood / acc)

		if likelihood > maxLikelihood:
			colorClass = k
			maxLikelihood = likelihood
		k = k + 1

	if maxLikelihood < threshold:
		colorClass = -1

	return colorClass

##################################################
##### initialization method #####
def init(dataFile):
	global stats
	global colors
	
	with open(dataFile) as statsFile:
		stats = json.load(statsFile)
		colors = stats['classes']
		print('Color stats loaded')

##################################################
##### method applying the color segmentation #####
def segmentate(folder, thres):
	for f in os.listdir(folder):
		img = cv2.imread(folder + '/' + f)
		print('Image read ' + f)

		for i in range(len(img)):
			for j in range(len(img[i])):
				k = classify(img[i][j], thres)
				if k != -1:
					img[i][j] = numpy.array(colors[k]['mean']).astype(int).tolist()[::-1]
				else:
					img[i][j] = [255, 255, 0]

		print('Saving segmented image')
		cv2.imwrite('./segmentation/' + f[:f.rfind('.')]+ '.png', img, [cv2.cv.CV_IMWRITE_PNG_COMPRESSION, 9])

##################################################
##### main method #####
def main():
	init(sys.argv[1])
	segmentate(sys.argv[2], float(sys.argv[3]))

##################################################
##### call main method #####
if __name__ == '__main__':
	main()