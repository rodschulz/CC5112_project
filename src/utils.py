import json
import os
import cv2
import numpy

R = 0
G = 1
B = 2


##################################################
# Loads the target json file as a dictionary.
# Returns None if the file can't be loaded
#
def loadJson(filename):
    try:
        with open(filename) as cacheFile:
            return json.load(cacheFile)

    except IOError as e:
        print('Cant read file' + filename)
        return None


##################################################
# Saves the given data (a dictionary) as a json file.
#
def saveJson(data, filename):
    try:
        folder = filename[:filename.rfind('/') + 1]
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(filename, 'w') as outfile:
            json.dump(data, outfile)

    except IOError as e:
        print('Cant save file ' + filename)


##################################################
# Saves the given data (a dictionary) as a json file.
#
def reshapeMarks(marks):
    for key in marks:
        if key != 'width' and key != 'height':
            newEntry = []
            for entry in marks[key]:
                newEntry.append([[entry[0], entry[1]], [entry[2], entry[3], entry[4]]])

            marks[key] = newEntry


##################################################
# Truncates to int all the elements in the given array
#
def truncateToInt(array):
    truncated = [int(x) for x in array]
    return truncated


##################################################
# Calculates the segmentation error over a set of ground truth pixels.
# Receives:
# - path to the json file with the stats to evaluate
# - path to the ground truth markings
# - path to the segmented image to evaluate
#
def getColorIndices(stats):
    indices = {}

    for data in stats:
        index = len(indices)
        indices[data['name']] = index

    return indices


##################################################
# Returns a dictionary with the indices of the colors stored in the stats file.
# The stats have to be delivered as an array holding the entries for that color.
#
def calculateError(statsFilename, marksFilename, imageFilename):
    stats = loadJson(statsFilename)
    marks = loadJson(marksFilename)

    ratio = -1
    if stats != None and marks != None:
        # prepare stats
        stats = stats['classes']
        for entry in stats:
            entry['mean'] = truncateToInt(entry['mean'])

        # prepare marks
        reshapeMarks(marks)

        # load the image
        img = cv2.imread(imageFilename)
        image = cv2.resize(img, (marks['width'], marks['height']))

        total = 0
        good = 0

        idx = getColorIndices(stats)
        for key in marks:
            if key != 'width' and key != 'height':
                for entry in marks[key]:
                    i = entry[0][0]
                    j = entry[0][1]
                    px = image[j][i][::-1]  # turn over the pixels, since opencv used them backwards

                    total += 1
                    good += int(sum(stats[idx[key]]['mean'] == px) == 3)

        ratio = float(good) / float(total)

    return ratio


##################################################
# Returns the name of the marks associated to the given image filename
#
def getMarksName(imageFilename):
    return imageFilename.replace('.', '_') + '.json'


##################################################
# Calculate the stats for the given data array
#
def calculateStats(key, data):
    stats = {}

    stats['name'] = key
    stats['mean'] = [numpy.mean(data[R]), numpy.mean(data[G]), numpy.mean(data[B])]
    stats['covariance'] = numpy.cov(data).tolist()
    stats['determinant'] = numpy.linalg.det(stats['covariance'])
    stats['sqrtDet'] = numpy.sqrt(stats['determinant'])
    stats['inverse'] = numpy.linalg.inv(stats['covariance']).tolist()
    stats['sampleCount'] = len(data[R])

    return stats


##################################################
# Extract an RGB array from the given array holding the samples
#
def extractRGB(array):
    data = []
    for row in array:
        data.append(row[2:5])
    return data


##################################################
# An array from a list of triples to 3 columns of data
#
def convertToCols(array):
    data = [[], [], []]
    for row in array:
        data[R].append(row[R])
        data[G].append(row[G])
        data[B].append(row[B])
    return data


##################################################
# Calculates the mahalanobis distance
#
def mahalanobis(mean, covInv, pixel):
    delta = numpy.subtract(pixel, mean)
    m = numpy.dot(covInv, delta)
    m = numpy.dot(delta, m)
    return numpy.sqrt(m)

##################################################
# Generates an empty stats dictionary
#
# def emptyStats():
#     stats = {'classes': []}
#     stats['classes'] = []
