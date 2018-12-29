import json
import pickle
import os
import json
from math import sqrt

listOfBenchmarksFile = open('list')

benchmarks = listOfBenchmarksFile.read().strip().split(",")
numBenchmarks = len(benchmarks)

tempDict = {}
ID = 50359
for package in benchmarks:
	with open('packages_sourced/'+package+'.json', 'r') as package_file:
		packageData = json.loads(package_file.read())
		for insn in packageData['instructions']:
			key = insn['mnem']
			source = insn['source'].strip().rsplit('/', 1)[1]
			if key in tempDict.keys():
				newInsn = tempDict[key]
				newInsn['count'] += insn['count']
				if package not in newInsn['packages']:
					newInsn['packages'].append(package)
			else:
				if insn['tag'] == None:
					continue
				newInsn = {}
				newInsn['count'] = insn['count']
				newInsn['packages'] = []
				newInsn['packages'].append(package)
				tempDict[key] = newInsn

# this contains the number of benchmarks an instruction occurs in
insnsBenchmarkedPC = dict()
# this contains the number of times an instruction occurs in the entire data set
insnsBenchmarkedRC = dict()
for mnem in tempDict.keys():
	insnsBenchmarkedPC[mnem] = len(tempDict[mnem]['packages'])
	insnsBenchmarkedRC[mnem] = int(tempDict[mnem]['count'])

mnemonicImportanceBenchmarks = dict()
for (mnem, packageCount) in insnsBenchmarkedPC.items():
	mnemonicImportanceBenchmarks[mnem] = (packageCount*100.0)/numBenchmarks*1.0

mnemonicRankedRawBenchmarks = sorted([(count, mnem) for (mnem, count) in insnsBenchmarkedRC.items()], reverse=True)

mnemonicRankedFull = {}
with open('mnemonicranked.csv', 'r') as mnemonicRankedFile:
	mnemonicRankedFile.readline() # get rid of header.
	for line in mnemonicRankedFile:
		mnemonic, tag, percentofpackages = line.strip().split(',')
		mnemonicRankedFull[mnemonic] = percentofpackages
	mnemonicRankedFile.close()

# x-axis as order of popularity of instructions in benchmarks and y-axis as the instruction importance in the larger set
with open('benchmarkInsnFreqVSInsnImp.csv', 'w') as outFile:
	counter = 1;
	for (count, mnem) in mnemonicRankedRawBenchmarks:
		if mnem in mnemonicRankedFull.keys():
			outFile.write(mnem+str(counter)+","+str(mnemonicRankedFull[mnem])+"\n")
		else:
			print mnem
			outFile.write(str(counter)+",0\n")
		counter += 1

# x-axis as the order of instruction importance in the larger set and y-axis as the popularity in the benchmarks.
mnemonicRankedFull = sorted([(percentofpackages, mnem) for (mnem, percentofpackages) in mnemonicRankedFull.items()], reverse=True)

with open('fullInsnImpvsBenchmarkImp.csv', 'w') as outFile:
	counter = 1
	for (percentofpackages, mnem) in mnemonicRankedFull:
		if mnem in mnemonicImportanceBenchmarks.keys():
			outFile.write(str(counter)+","+str(mnemonicImportanceBenchmarks[mnem])+"\n")
		else:
			outFile.write(str(counter)+",0\n")
		counter += 1