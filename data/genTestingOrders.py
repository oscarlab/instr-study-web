import json
import pickle
import os

groupFile = open('groups.json')

groups = json.loads(groupFile.read())

packageOpcodes = {}
opcodes = {}
packageMnemonics = {}
mnemonics = {}
numPackages = 0

pmFileExists = os.path.isfile('./packagesMnemonics.pickle')
if pmFileExists:
	with open('packagesMnemonics.pickle', 'rb') as handle:
		packageMnemonics = pickle.load(handle)
		numPackages = len(packageMnemonics)

poFileExists = os.path.isfile('./packageOpcodes.pickle')
if poFileExists:
	with open('packageOpcodes.pickle', 'rb') as handle:
		packageOpcodes = pickle.load(handle)

mFileExists = os.path.isfile('./mnemonics.pickle')
if mFileExists:
	with open('mnemonics.pickle', 'rb') as handle:
		mnemonics = pickle.load(handle)

oFileExists = os.path.isfile('./opcodes.pickle')
if oFileExists:
	with open('opcodes.pickle', 'rb') as handle:
		opcodes = pickle.load(handle)

# If either of these pickles doesn't exist, gather the data again.
# Calculate the set of opcodes and mnemonics that each package needs.
if (not pmFileExists) or (not mFileExists) or (not poFileExists) or (not oFileExists):
	for group in groups:
		for package in groups[group]:
			with open('packages_sourced/'+package['name']+'.json','r') as packageFile:
				packageData = json.loads(packageFile.read())
				mnemSet = set([p['mnem'] for p in packageData['instructions']])
				for mnem in mnemSet:
					if mnem in mnemonics.keys():
						mnemonics[mnem].add(package['name'])
					else:
						mnemonics[mnem] = set(package['name'])
				opcodeSet = set([p['opcode'] for p in packageData['instructions']])
				for opcode in opcodeSet:
					if opcode in opcodes.keys():
						opcodes[opcode].add(package['name'])
					else:
						opcodes[opcode] = set(package['name'])
				packageOpcodes[package['name']] = opcodeSet
				packageMnemonics[package['name']] = mnemSet
				packageFile.close()
	with open('packagesMnemonics.pickle', 'wb') as pmFile:
		pickle.dump(packageMnemonics, pmFile, protocol=pickle.HIGHEST_PROTOCOL)
	with open('packageOpcodes.pickle', 'wb') as poFile:
		pickle.dump(packageOpcodes, poFile, protocol=pickle.HIGHEST_PROTOCOL)
	with open('mnemonics.pickle', 'wb') as mFile:
		pickle.dump(mnemonics, mFile, protocol=pickle.HIGHEST_PROTOCOL)
	with open('opcodes.pickle', 'wb') as oFile:
		pickle.dump(opcodes, oFile, protocol=pickle.HIGHEST_PROTOCOL)


#Read in Pinst.json
pinstFile = open('pinst.json', 'r')
pInst = json.loads(pinstFile.read())

#############################################################################
# weighted_completeness = SUMMATION(PInst(supported)/Summation(PInst(all)))	#
# notation :																#
# PInst(name) -> PInst of all packages falling under the category "name"	#
#############################################################################

# we need fractions for weighted completeness. Also calculate the denominator.
denominator = float(0)
for package in pInst.keys():
	# convert back to fraction from %
	pInst[package] = pInst[package]/100.0
	denominator += pInst[package]

# # Now comes the task of figuring out how many packages are supported as each
# # instruction is added.
# steps = {}
# stepNum = 0
# packagesToTest = []
# numPackagesToTest = 0
# numSupportedOpcodes = 0
# opcodesTested = []
# numerator = 0.0
# with open('testingOrderOpcodes.csv', 'w+') as opcodeFileCSV:
# 	opcodeFileCSV.write("numOpcodes,numPackages, weightedCompleteness\n")
# 	newlyAddedOpcodes = []
# 	packageOpcodeFootprints = []
# 	for package in packageOpcodes:
# 		packageOpcodeFootprints.append((len(packageOpcodes[package]),package))
# 	packageOpcodeFootprints = sorted(packageOpcodeFootprints, reverse=True)
# 	while opcodes:
# 		if not packageOpcodeFootprints:
# 			break
# 		numNewOpcodes, packageSelected = packageOpcodeFootprints.pop(0)
# 		packageFootPrint = packageOpcodes.pop(packageSelected)
# 		# Remove newly added opcodes from the lists
# 		usePackage = False
# 		for opcode in packageFootPrint:
# 			if opcode in opcodes:
# 				opcodes.pop(opcode, None)
# 				opcodesTested.append(opcode)
# 				newlyAddedOpcodes.append(opcode)
# 				numSupportedOpcodes += 1
# 				usePackage = True
# 			else:
# 				continue
# 		if usePackage is True:
# 			packagesToTest.append(packageSelected)
# 			numPackagesToTest += 1
# 			pack = {}
# 			pack['stepNum'] = stepNum
# 			pack['numSupportedOpcodes'] = numSupportedOpcodes
# 			pack['numPackagesToTest'] = numPackagesToTest
# 			pack['packagesToTest'] = list(packagesToTest)
# 			pack["newlyAddedOpcodes"] = list(newlyAddedOpcodes)
# 			steps[stepNum] = pack
# 			stepNum += 1
# 			opcodeFileCSV.write(str(numSupportedOpcodes)+","+str(numPackagesToTest)+",")
# 			for package in packagesToTest:
# 				opcodeFileCSV.write(package+' ')
# 			opcodeFileCSV.write("\n")


# # Write out the instructions added at each step in JSON so we can use it later.
# with open('testingOrderOpcodes.json','w+') as opcodeFileJSON:
# 	opcodeFileJSON.write(json.dumps(steps, indent=4, sort_keys=True))


mnemonicRankedFull = {}
with open('mnemonicranked.csv', 'r') as mnemonicRankedFile:
	mnemonicRankedFile.readline() # get rid of header.
	for line in mnemonicRankedFile:
		mnemonic, tag, percentofpackages = line.strip().split(',')
		mnemonicRankedFull[mnemonic] = percentofpackages
	mnemonicRankedFile.close()

# Now comes the task of figuring out how many packages are supported as each
# instruction is added.
steps = {}
stepNum = 0
packagesToTest = []
numPackagesToTest = 0
numSupportedMnemonics = 0
numerator = 0.0
with open('testingOrderMnemonics.csv', 'w+') as mnemonicFileCSV:
	mnemonicFileCSV.write("numMnemonics,numPackages, weightedCompleteness\n")
	newlyAddedMnemonics = []
	packageMnemonicFootprints = []
	for package in packageMnemonics:
		packageMnemonicFootprints.append((len(packageMnemonics[package]),package))
	packageMnemonicFootprints = sorted(packageMnemonicFootprints, reverse=True)
	while mnemonics:
		if not packageMnemonicFootprints:
			break
		numNewMnemonics, packageSelected = packageMnemonicFootprints.pop(0)
		packageFootPrint = packageMnemonics.pop(packageSelected)
		# Remove newly added Mnemonics from the lists
		usePackage = False
		for mnemonic in packageFootPrint:
			if mnemonic in mnemonics:
				mnemonics.pop(mnemonic,None)
				newlyAddedMnemonics.append(mnemonic)
				numSupportedMnemonics += 1
				usePackage = True
			else:
				continue
		if usePackage is True:
			packagesToTest.append(packageSelected)
			numPackagesToTest += 1
			pack = {}
			pack['stepNum'] = stepNum
			pack['numSupportedMnemonics'] = numSupportedMnemonics
			pack['numPackagesToTest'] = numPackagesToTest
			pack['packagesToTest'] = list(packagesToTest)
			pack["newlyAddedMnemonics"] = list(newlyAddedMnemonics)
			steps[stepNum] = pack
			stepNum += 1
			mnemonicFileCSV.write(str(numSupportedMnemonics)+","+str(numPackagesToTest)+",")
			for package in packagesToTest:
				mnemonicFileCSV.write(package+' ')
			mnemonicFileCSV.write("\n")

# Write out the instructions added at each step in JSON so we can use it later.
with open('testingOrderMnemonics.json','w+') as mnemonicFileJSON:
	mnemonicFileJSON.write(json.dumps(steps, indent=4, sort_keys=True))