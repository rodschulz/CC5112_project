##################################################
# This receives 3 arguments:
# - the file holding the stats for every color
# - the folder with the images to process
# - the threshold to use for minimum valid clasification
# Ex:
#    python segmentator.py ./path/to/stats.json ./folder/of/imgs/ threshold
#
##################################################
import sys
import json
import numpy
import os
import cv2
import hashlib
import pdb

##################################################
from __builtin__ import file


def getCacheName(stats):
    name = hashlib.sha1(str(stats)).hexdigest()
    filename = './cache/' + name + '.json'
    return filename


##################################################
def loadCache(stats):
    cache = {}
    filename = getCacheName(stats)

    try:
        with open(filename) as cacheFile:
            cache = json.load(cacheFile)
            print('Cache loaded')

    except IOError as e:
        print('Cache file not found')

    return cache


##################################################
def saveCache(cache, stats):
    try:
        filename = getCacheName(stats)
        with open(filename, 'w') as outfile:
            json.dump(cache, outfile)
            print('Cache saved')

    except IOError as e:
        print('Cant create cache file (' + filename + ')')


##################################################
def getLikelihood(pixel, mean, covariance, covInverse, sqrtDet):
    delta = numpy.subtract(pixel, mean)
    exponent = numpy.dot(delta, covInverse)
    exponent = numpy.dot(exponent, delta)
    factor = 1 / (15.7496099457 * sqrtDet)
    return factor * numpy.exp(-0.5 * exponent)


##################################################
def getTotalProb(pixel, stats):
    total = 0
    for color in stats:
        total = total + getLikelihood(pixel, color['mean'], color['covariance'], color['inverse'], color['sqrtDet'])
    return total


##################################################
def getClass(pixel, stats):
    colorIdx = -1
    maxLikelihood = -1
    index = 0

    # calculate the likelihood for each pixel
    for color in stats:
        likelihood = getLikelihood(pixel, color['mean'], color['covariance'], color['inverse'], color['sqrtDet'])

        # likelihood = likelihood / getTotalProb(pixel, colorStats)
        if likelihood > maxLikelihood:
            colorIdx = index
            maxLikelihood = likelihood

        index = index + 1

    return [colorIdx, maxLikelihood]


#################################################
def classify(pixel, threshold, stats, cache):
    colorIdx = -1
    maxLikelihood = -1

    # attempt to load from cache if can
    key = str(pixel)
    if key in cache:
        value = cache[key]
        colorIdx = value[0]
        maxLikelihood = value[1]
    else:
        cls = getClass(pixel, stats)
        cache[key] = cls
        colorIdx = cls[0]
        maxLikelihood = cls[1]

    # if maxLikelihood < threshold:
    #    colorClass = -1

    return colorIdx


##################################################
def applySegmentation(folder, threshold, stats, cache):
    print('')

    # read each image
    for f in os.listdir(folder):
        img = cv2.imread(folder + '/' + f)
        print('- Image read ' + f)

        # classify each pixel in a color class
        for i in range(len(img)):
            for j in range(len(img[i])):
                k = classify(img[i][j], threshold, stats, cache)
                if k != -1:
                    img[i][j] = numpy.array(stats[k]['mean']).astype(int).tolist()[::-1]
                else:
                    img[i][j] = [255, 255, 0]

        print('\tSaving segmented image')
        cv2.imwrite('./segmentation/' + f[:f.rfind('.')] + '.png', img, [cv2.cv.CV_IMWRITE_PNG_COMPRESSION, 9])

    print('\nAll images processed')


##################################################
def loadStats(filename):
    stats = []
    try:
        with open(filename) as statsFile:
            stats = json.load(statsFile)
            stats = stats['classes']
            print('Color stats loaded')

    except IOError as e:
        print 'Stats file not found'

    return stats


##################################################
def main():
    stats = loadStats(sys.argv[1])
    cache = loadCache(stats)

    # keep executing only if stats were loaded
    if len(stats) > 0:
        applySegmentation(sys.argv[2], float(sys.argv[3]), stats, cache)
        saveCache(cache, stats)
    else:
        print('No stats available, cant process images')

    print('Finished')


##################################################
if __name__ == '__main__':
    main()
