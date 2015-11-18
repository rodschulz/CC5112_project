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

##################################################
def loadCache(filename):
	cache = {}
	try:
		with open(filename) as cacheFile:
			cache = json.load(cacheFile)
			print('Cache loaded')

	except IOError as e:
		print 'Cache file not found'

	return cache

##################################################
def saveCache(filename, cache):
	with open(filename, 'w') as outfile:
		json.dump(cache, outfile)

##################################################
def getLikelihood(pixel, mean, covariance, covInverse, sqrtDet):
	delta = numpy.subtract(pixel, mean)
	exponent = numpy.dot(delta, covInverse)
	exponent = numpy.dot(exponent, delta)
	factor = 1 / (15.7496099457 * sqrtDet)
	return factor * numpy.exp(-0.5 * exponent)

##################################################
def getTotalProb(pixel, colorStats):
	total = 0
	for ck in colorStats:
		total = total + getLikelihood(pixel, ck['mean'], ck['covariance'], ck['inverse'], ck['sqrtDet'])
	return total

##################################################
def getClass(pixel, colorStats):
	colorClass = -1
	maxLikelihood = -1
	classIndex = 0

	# calculate the likelihood for each pixel
	for color in colorStats:
		likelihood = getLikelihood(pixel, color['mean'], color['covariance'], color['inverse'], color['sqrtDet'])

		likelihood = likelihood / getTotalProb(pixel, colorStats)
		if likelihood > maxLikelihood:
			colorClass = classIndex
			maxLikelihood = likelihood
		
		classIndex = classIndex + 1

	return [colorClass, maxLikelihood]

#################################################
def classify(pixel, threshold, colorStats, cache):
	colorClass = -1
	maxLikelihood = -1

	# attempt to load from cache if can
	key = str(pixel)
	if key in cache:
		value = cache[key]
		colorClass = value[0]
		maxLikelihood = value[1]
	else:
		cls = getClass(pixel, colorStats)
		cache[key] = cls
		colorClass = cls[0]
		maxLikelihood = cls[1]

	if maxLikelihood < threshold:
		colorClass = -1

	return colorClass

##################################################
def applySegmentation(folder, threshold, colorStats, cache):
	# read each image
	for f in os.listdir(folder):
		img = cv2.imread(folder + '/' + f)
		print('Image read ' + f)

		# classify each pixel in a color class
		for i in range(len(img)):
			for j in range(len(img[i])):
				k = classify(img[i][j], threshold, colorStats, cache)
				if k != -1:
					img[i][j] = numpy.array(colorStats[k]['mean']).astype(int).tolist()[::-1]
				else:
					img[i][j] = [255, 255, 0]

		print('Saving segmented image')
		cv2.imwrite('./segmentation/' + f[:f.rfind('.')]+ '.png', img, [cv2.cv.CV_IMWRITE_PNG_COMPRESSION, 9])

##################################################
def loadStats(filename):
	colorStats = []
	with open(filename) as statsFile:
		stats = json.load(statsFile)
		colorStats = stats['classes']
		print('Color stats loaded')

	return colorStats

##################################################
def main():
	cache = loadCache('./colorCache.json')
	colorStats = loadStats(sys.argv[1])
	applySegmentation(sys.argv[2], float(sys.argv[3]), colorStats, cache)
	saveCache('./colorCache.json', cache)

##################################################
if __name__ == '__main__':
	main()