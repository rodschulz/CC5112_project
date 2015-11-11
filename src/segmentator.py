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

stats = {}
colors = []
thres = 0
R = 0; G = 1; B = 2

##################################################
##### calculate the likelihood #####
def getLikelihood(sigma, detSigma):
	return (1 / sqrt(pow(2 * pi, 2)))

def classify(pixel):
	return 1

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
def segmentate(folder):
	for f in os.listdir(folder):
		img = cv2.imread(folder + '/' + f)
		print('Image read ' + f)


		# here has to be implemented the classification part!!

		i = 0
		for row in img:
			for col in row:
				print(str(i) + ': ' + str(col))
				i = i + 1
				k = classify(col)
			pause

##################################################
##### main method #####
def main():
	global thres
	init(sys.argv[1])
	thres = float(sys.argv[3])
	segmentate(sys.argv[2])

##################################################
##### call main method #####
if __name__ == '__main__':
	main()