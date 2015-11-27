##################################################
# This receives:
# - source folder with the images to process
# - destination folder for segmented images
# - file holding the stats for every color
# - threshold for minimum valid classification
#
##################################################
import sys
import numpy
import os
import cv2
import hashlib
import time
import utils
import shutil


##################################################
def getCacheName(stats):
    name = hashlib.sha1(str(stats)).hexdigest()
    filename = './cache/' + name + '.json'
    return filename


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

        likelihood = likelihood / getTotalProb(pixel, stats)
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

    if maxLikelihood < threshold:
        colorClass = -1

    return colorIdx


##################################################
def applySegmentation(src, dest, threshold, stats, cache):
    print('')

    # create destination folder if it doesn't exists
    if not os.path.exists(dest):
        os.makedirs(dest)

    # read each image
    for f in os.listdir(src):
        img = cv2.imread(src + '/' + f)
        print('Read image ' + f)

        # classify each pixel in a color class
        start = time.time()
        for i in range(len(img)):
            for j in range(len(img[i])):
                # turn over the pixels, since opencv used them backwards
                px = img[i][j][::-1]

                k = classify(px, threshold, stats, cache)
                if k != -1:
                    img[i][j] = numpy.array(stats[k]['mean']).astype(int).tolist()[::-1]
                else:
                    img[i][j] = [255, 255, 0]

        elapsed = '{:3.4f} [s]'.format(time.time() - start)
        filename = dest + f[:f.rfind('.')] + '.png'
        print('\tSaving segmented image to ' + filename + ' (processed in ' + elapsed + ')')

        cv2.imwrite(filename, img, [cv2.cv.CV_IMWRITE_PNG_COMPRESSION, 9])

    print('\nAll images processed')


##################################################
def main():
    src = sys.argv[1]
    dest = sys.argv[2]
    stats = utils.loadJson(sys.argv[3])
    threshold = float(sys.argv[4])

    # keep executing only if stats were loaded
    if stats != None:
        stats = stats['classes']
        cache = utils.loadJson(getCacheName(stats))
        if cache == None:
            cache = {}

        applySegmentation(src, dest, threshold, stats, cache)
        utils.saveJson(cache, getCacheName(stats))
    else:
        print('No stats available, cant process images')

    print('Finished')


##################################################
if __name__ == '__main__':
    main()
