import json
import os
import cv2


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
