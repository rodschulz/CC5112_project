##################################################
# This receives:
# - folder holding the images for the generation of sets
# - number indicating percentage split of data (x for train, 1-x for validation)
# Ex:
#    python syntheticStatsGen.py ./folder/with/images/
#
##################################################
import sys
import json
import os
import random
import shutil


##################################################
def getFileCount(folder):
    return len(os.listdir(folder))


##################################################
def main():
    folder = sys.argv[1]
    nfiles = getFileCount(folder)
    nsplit = int(float(sys.argv[2]) * nfiles)

    sample = random.sample(os.listdir(folder), nsplit)
    base = folder[:folder.rfind('/', 0, len(folder) - 1) + 1]
    train = base + 'train/'
    validation = base + 'val/'

    # remove previous folders
    shutil.rmtree(train, True)
    shutil.rmtree(validation, True)

    # create new folders
    os.makedirs(train)
    os.makedirs(validation)

    ntrain = 0
    nval = 0
    for f in os.listdir(folder):
        ext = f[f.rfind('.'):]
        if f in sample:
            shutil.copyfile(folder + f, train + 'train_' + str(ntrain) + ext)
            ntrain += 1
        else:
            shutil.copyfile(folder + f, validation + 'val_' + str(nval) + ext)
            nval += 1


##################################################
if __name__ == '__main__':
    main()
