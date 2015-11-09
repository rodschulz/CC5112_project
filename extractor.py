import sys
import json
import numpy
import os

data = {}
stats = {}
sR = 2
sG = 3
sB = 4
R = 0
G = 1
B = 2

def saveStats():
	dest = './colorStats.json'
	with open(dest, 'w') as outfile:
		json.dump(stats, outfile)
	print('Stats saved to ' + dest)

def calculateStats():
	for key in data:
		stats[key] = {'mean': [], 'covariance':[]}
		if not data[key][R] or not data[key][G] or not data[key][B]:
			continue

		stats[key]['mean'] = [numpy.mean(data[key][R]), numpy.mean(data[key][G]), numpy.mean(data[key][B])]
		stats[key]['covariance'] = numpy.cov(data[key]).tolist()

##################################################
##### data extraction method #####
def extractData(folder):
	for f in os.listdir(folder):
		if f.endswith(".json"):
			with open(folder + '/' + f) as samplesFile:
				samples = json.load(samplesFile)
				for key in data:
					colorSamples = samples[key]
					for sample in colorSamples:
						data[key][R].append(sample[sR])
						data[key][G].append(sample[sG])
						data[key][B].append(sample[sB])

##################################################
##### initialization method #####
def init():
	global data
	data["Black"] = [[], [], []]
	data["Blue"] = [[], [], []]
	data["Green"] = [[], [], []]
	data["Orange"] = [[], [], []]
	data["Red"] = [[], [], []]
	data["White"] = [[], [], []]
	data["Yellow"] = [[], [], []]

##################################################
##### main method #####
def main():
	init()
	extractData(sys.argv[1])
	calculateStats()
	saveStats()

	#print(stats)

##################################################
##### call main method #####
if __name__ == '__main__':
	main()