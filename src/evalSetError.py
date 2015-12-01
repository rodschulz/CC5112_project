##################################################
# This receives:
# - folder with the original images
# - folder with the segmented images
# - folder with the marks
# - stats used for segmentation
#
##################################################
import sys
import os
import utils
import numpy


##################################################
def main():
    original = sys.argv[1]
    segmented = sys.argv[2]
    marksFolder = sys.argv[3]
    stats = sys.argv[4]

    # read each image
    errors = []
    for f in os.listdir(original):

        img = segmented + f[:f.rfind('.')] + '.png'
        print('Processing image ' + img)

        marks = marksFolder + utils.getMarksName(f)
        err = utils.calculateError(stats, marks, img)
        if err != -1:
            print('\terror: ' + str(err))
            errors.append(err)

    mean = numpy.mean(errors)
    std = numpy.std(errors)
    print('mean: ' + str(mean) + ' - std: ' + str(std))

    print('Finished')


##################################################
if __name__ == '__main__':
    main()
