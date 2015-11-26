##################################################
# This receives:
# - folder holding the images and samples (in two different folders)
# - destination folder
# - percentage split of data (x for train, 1-x for validation)
# Ex:
#    python syntheticStatsGen.py ./origin/folder/ ./destination/folder/ 0.x
#
##################################################
import sys
import os
import random
import shutil


##################################################
def main():
    origin = sys.argv[1]
    dest = sys.argv[2]

    # origin folders
    images = origin + 'images/'
    samples = origin + 'samples/'

    # number of files
    nfiles = len(os.listdir(images))
    nsplit = int(float(sys.argv[3]) * nfiles)
    filesSample = random.sample(os.listdir(images), nsplit)

    # destination folders
    train = dest + 'train/'
    train_samples = dest + 'train_samples/'
    val = dest + 'val/'
    val_samples = dest + 'val_samples/'

    # remove previous folders
    shutil.rmtree(train, True)
    shutil.rmtree(train_samples, True)
    shutil.rmtree(val, True)
    shutil.rmtree(val_samples, True)

    # create new folders
    os.makedirs(train)
    os.makedirs(train_samples)
    os.makedirs(val)
    os.makedirs(val_samples)

    # generate split
    for f in os.listdir(images):
        fname = f.replace('.', '_') + '.json'
        print('Copying ' + f + ' and ' + fname)

        if f in filesSample:
            shutil.copyfile(images + f, train + f)
            shutil.copyfile(samples + fname, train_samples + fname)
        else:
            shutil.copyfile(images + f, val + f)
            shutil.copyfile(samples + fname, val_samples + fname)

    print('Finished')


##################################################
if __name__ == '__main__':
    main()
