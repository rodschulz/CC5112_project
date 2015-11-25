##################################################
# This receives 1 argument:
# - the file holding the stats for every color
# Ex:
#	python cube.py ./path/to/stats.json
#
##################################################
import sys
import json
import segmentator as seg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


##################################################
def loadStats(filename):
    with open(filename) as statsFile:
        stats = json.load(statsFile)
        colors = stats['classes']
        print('Color stats loaded')

        return colors


##################################################
def saveCube(filename, cube):
    with open(filename, 'w') as outfile:
        json.dump(cube, outfile)


##################################################
def main():
    colors = loadStats(sys.argv[1])
    cube = {}

    thres = 0.9
    R = []
    G = []
    B = []
    col = []

    step = 10
    for i in range(0, 255, step):
        for j in range(0, 255, step):
            for k in range(0, 255, step):

                pixel = [i, j, k]
                cls = seg.getClass(pixel, colors)
                cube[str(pixel)] = cls

                # pdb.set_trace()

                if cls[1] >= thres:
                    R.append(i)
                    G.append(j)
                    B.append(k)
                    col.append([t / 255.0 for t in colors[cls[0]]['mean']])

    saveCube('./cube.json', cube)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(R, G, B, c=col, marker='o', s=30, edgecolor='black', linewidth='0', alpha=1.0)
    ax.set_xlabel('R')
    ax.set_ylabel('G')
    ax.set_zlabel('B')
    plt.show()


##################################################
if __name__ == '__main__':
    main()
