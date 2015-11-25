##################################################
# This receives:
# - destination path for the output file
# Ex:
#    python syntheticStatsGen.py ./destination/path/
#
##################################################
import sys
import json
import numpy
import os
import time
import random


##################################################
def getColorSet():
    colors = ['black', 'white', 'red', 'blue', 'green', 'yellow']
    return colors


##################################################
def genStats(colors):
    classes = []

    for color in colors:
        sts = {}
        mean = 0
        var = 650
        covariance = [[var, 0, 0], [0, var, 0], [0, 0, var]]

        if color == 'black':
            mean = [0, 0, 0]
        elif color == 'white':
            mean = [255, 255, 255]
        elif color == 'red':
            mean = [255, 0, 0]
        elif color == 'blue':
            mean = [0, 0, 255]
        elif color == 'green':
            mean = [0, 255, 0]
        elif color == 'yellow':
            mean = [255, 255, 0]

        sts['name'] = color
        sts['sampleCount'] = -1
        sts['mean'] = mean
        sts['covariance'] = covariance
        sts['inverse'] = numpy.linalg.inv(covariance).tolist()
        sts['determinant'] = numpy.linalg.det(covariance)
        sts['sqrtDet'] = numpy.sqrt(sts['determinant'])

        classes.append(sts)

    stats = {'classes': classes}
    return stats


##################################################
def genRandomStats(colors):
    classes = []

    for color in colors:
        sts = {}

        mean = []
        if color == 'black':
            mu = 20
            sigma = 30
            mean = [getRandom(mu, sigma), getRandom(mu, sigma), getRandom(mu, sigma)]

        elif color == 'white':
            mu = 235
            sigma = 30
            mean = [getRandom(mu, sigma), getRandom(mu, sigma), getRandom(mu, sigma)]

        elif color == 'red':
            mu1 = 220
            mu2 = 20
            sigma = 30
            mean = [getRandom(mu1, sigma), getRandom(mu2, sigma), getRandom(mu2, sigma)]

        elif color == 'blue':
            mu1 = 220
            mu2 = 20
            sigma = 30
            mean = [getRandom(mu2, sigma), getRandom(mu2, sigma), getRandom(mu1, sigma)]

        elif color == 'green':
            mu1 = 220
            mu2 = 20
            sigma = 30
            mean = [getRandom(mu2, sigma), getRandom(mu1, sigma), getRandom(mu2, sigma)]

        elif color == 'yellow':
            mean = [255, 255, 0]

            mu1 = 220
            mu2 = 20
            sigma = 30
            mean = [getRandom(mu1, sigma), getRandom(mu1, sigma), getRandom(mu2, sigma)]

        varMu = 750
        varSigma = 250
        covariance = [[abs(random.gauss(varMu, varSigma)), abs(random.gauss(varMu, varSigma)),
                       abs(random.gauss(varMu, varSigma))],
                      [0, abs(random.gauss(varMu, varSigma)), abs(random.gauss(varMu, varSigma))],
                      [0, 0, abs(random.gauss(varMu, varSigma))]]

        covariance[1][0] = covariance[0][1]
        covariance[2][0] = covariance[0][2]
        covariance[2][1] = covariance[1][2]

        covariance = numpy.dot(covariance, covariance)
        for i in range(len(covariance)):
            for j in range(len(covariance[i])):
                covariance[i][j] /= 4000

        sts['name'] = color
        sts['sampleCount'] = -1
        sts['mean'] = mean
        sts['covariance'] = covariance.tolist()
        sts['inverse'] = numpy.linalg.inv(covariance).tolist()
        sts['determinant'] = numpy.linalg.det(covariance)
        sts['sqrtDet'] = numpy.sqrt(sts['determinant'])

        classes.append(sts)

    stats = {'classes': classes}
    return stats


##################################################
def getRandom(mu, sigma):
    value = abs(random.gauss(mu, sigma))
    if value >= 255:
        value = value - abs(random.gauss(mu / 5, sigma))

    return value


##################################################
def saveStats(stats, folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)

        destination = folder + 'colorStats_syn.json'
        with open(destination, 'w') as outfile:
            json.dump(stats, outfile)
        print('Stats saved to ' + destination)

    except IOError as e:
        print('Unnable to save stats')


##################################################
def main():
    random.seed(time.time())

    if len(sys.argv) < 3:
        useRandom = False
    else:
        useRandom = sys.argv[2] == '1'

    colors = getColorSet()
    if useRandom:
        syntheticStats = genRandomStats(colors)
    else:
        syntheticStats = genStats(colors)

    saveStats(syntheticStats, sys.argv[1])


##################################################
if __name__ == '__main__':
    main()
