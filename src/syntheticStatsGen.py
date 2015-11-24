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
import pdb


##################################################
def getColorSet():
    colors = ['black', 'white', 'red', 'blue', 'green', 'yellow']
    return colors


##################################################
def genStats(colors):
    classes = []

    for color in colors:
        var = 750
        sts = {}
        mean = 0
        covariance = [[], [], []]

        if color == 'black':
            mean = [0, 0, 0]
            covariance = [[var, 0, 0], [0, var, 0], [0, 0, var]]
        elif color == 'white':
            mean = [255, 255, 255]
            covariance = [[var, 0, 0], [0, var, 0], [0, 0, var]]
        elif color == 'red':
            mean = [255, 0, 0]
            covariance = [[var, 0, 0], [0, var, 0], [0, 0, var]]
        elif color == 'blue':
            mean = [0, 0, 255]
            covariance = [[var, 0, 0], [0, var, 0], [0, 0, var]]
        elif color == 'green':
            mean = [0, 255, 0]
            covariance = [[var, 0, 0], [0, var, 0], [0, 0, var]]
        elif color == 'yellow':
            mean = [255, 255, 0]
            covariance = [[var, 0, 0], [0, var, 0], [0, 0, var]]

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
    colors = getColorSet()
    syntheticStats = genStats(colors)
    saveStats(syntheticStats, sys.argv[1])


##################################################
if __name__ == '__main__':
    main()
