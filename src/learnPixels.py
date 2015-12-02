##################################################
# This receives:
# - json file with the data from pixels
# - output folder
#
##################################################
import sys
import random
import utils
import numpy
import segmentator


##################################################
def extractSets(data, ratio):
    trainPercent = ratio * 0.75
    valPercent = ratio * 0.25

    random.shuffle(data)
    size = len(data)

    # extract the train set
    begin = 0
    end = int(numpy.ceil(trainPercent * size))
    trainSet = data[begin:end]

    # extract the validation set
    begin = end
    end = int(end + numpy.ceil(valPercent * size))
    valSet = data[begin:end]

    # extract the validation set
    begin = end
    end = size
    testSet = data[begin:end]

    sets = {}
    sets['train'] = trainSet
    sets['val'] = valSet
    sets['test'] = testSet

    return sets


##################################################
def classify(data, threshold, stats, cache):
    classification = []
    for n in range(len(data[utils.R])):
        pixel = [data[utils.R][n], data[utils.G][n], data[utils.B][n]]
        cls = segmentator.classify(pixel, threshold, stats, cache)
        classification.append(stats[cls]['name'])

    return classification


##################################################
def classificationError(data, target):
    error = 0;
    for d in data:
        error += int(d != target)

    return error


##################################################
def meanMahalanobis(data, mean, covInv):
    dist = []
    for n in range(len(data[utils.R])):
        pixel = [data[utils.R][n], data[utils.G][n], data[utils.B][n]]
        dist.append(utils.mahalanobis(mean, covInv, pixel))

    return numpy.mean(dist)


##################################################
def getBestSets(key, pixels, ratio, attempts):
    sets = {}
    minDist = 1e10000

    for i in range(attempts):
        data = extractSets(pixels, ratio)
        data['train'] = utils.convertToCols(data['train'])
        data['val'] = utils.convertToCols(data['val'])
        data['test'] = utils.convertToCols(data['test'])
        data['stats'] = utils.calculateStats(key, data['train'])

        dist = meanMahalanobis(data['val'], data['stats']['mean'], data['stats']['inverse'])
        if dist < minDist:
            minDist = dist
            sets = data

    return sets


##################################################
def main():
    src = sys.argv[1]
    dest = sys.argv[2]
    attempts = 10
    ratio = 0.5
    thres = 0.9

    pixels = utils.loadJson(src)
    bestSamples = {}
    bestStats = {'classes': []}

    minError = 1e10000
    for n in range(attempts):
        print('** Attempt ' + str(n))
        samples = {}
        stats = {'classes': []}

        # get sets and stats from data
        for key in pixels:
            print('\tProcessing color ' + key)
            sets = getBestSets(key, pixels[key], ratio, attempts)
            stats['classes'].append(sets['stats'])
            samples[key] = sets

        # calculate the classification error
        error = 0
        cache = {}
        for key in samples:
            classification = classify(samples[key]['val'], thres, stats['classes'], cache)
            error += classificationError(classification, key)
        print('Error: ' + str(error))

        if error < minError:
            minError = error
            bestSamples = samples
            bestStats = stats

        if minError == 0:
            break

    print('Min error: ' + str(minError))
    print('Saving')
    utils.saveJson(bestStats, dest + 'learnedStats.json')

    print('Finished')


##################################################
if __name__ == '__main__':
    main()
