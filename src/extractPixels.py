##################################################
# This receives:
# - folder json samples are
# - output folder
#
##################################################
import sys
import os
import utils


##################################################
def extractRGB(array):
    data = []
    for row in array:
        data.append(row[2:5])
    return data


##################################################
def main():
    src = sys.argv[1]
    dest = sys.argv[2]
    pixels = {}

    for f in os.listdir(src):
        print('Processing ' + f)

        data = utils.loadJson(src + f)
        for key in data:
            if key != 'height' and key != 'width' and len(data[key]) > 0:
                if not key in pixels:
                    pixels[key] = []

                pixels[key] = pixels[key] + extractRGB(data[key])

    for key in pixels:
        print('Extracted ' + str(len(pixels[key])) + ' pixels for ' + key)

    print('Saving')
    utils.saveJson(pixels, dest + 'pixels.json')

    print('Finished')


##################################################
if __name__ == '__main__':
    main()
