import json

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
numSupportedPackages = 0
numSupportedMnemonics = 0
numerator = 0.0
with open('implementationOrderMnemonics.csv', 'w+') as mnemonicFileCSV:
	mnemonicFileCSV.write("numMnemonics,numPackages,weightedCompleteness\n")
	newlyAdded = []
	while packageMnemonics:
		# Calculate Deltas for all the packages
		deltas = []
		for package in packageMnemonics:
			deltas.append((len(packageMnemonics[package]),package))
		deltas = sorted(deltas)
		numNewMnemonics, packageSelected = deltas[0]
		newlyAdded = packageMnemonics.pop(packageSelected)
		numSupportedPackages += 1
		numSupportedMnemonics += numNewMnemonics
		# Remove newly added opcodes from the lists to reduce our input on
		# each round
		popMe = []
		for package in packageMnemonics:
			for mnemonic in newlyAdded:
				packageMnemonics[package].discard(mnemonic)
				if len(packageMnemonics[package]) == 0:
					numSupportedPackages += 1
					popMe.append(package)
		newlySupportedPackages = []
		newlySupportedPackages.append(packageSelected)
		for package in popMe:
			packageMnemonics.pop(package,None)
			newlySupportedPackages.append(package)
		# Calculate Weighted Completeness
		for package in newlySupportedPackages:
			numerator += pInst[package]
		weightedCompleteness = numerator/denominator
		pack = {}
		pack['stepNum'] = stepNum
		pack['weightedCompleteness'] = weightedCompleteness
		pack['numSupportedMnemonics'] = numSupportedMnemonics
		pack['numSupportedPackages'] = numSupportedPackages
		pack["newlyAddedMnemonics"] = list(newlyAdded)
		pack["newlySupportedPackages"] = newlySupportedPackages
		steps[stepNum] = pack
		stepNum += 1
		mnemonicFileCSV.write(str(numSupportedMnemonics)+","+str(numSupportedPackages)+","+str(weightedCompleteness)+"\n")

# Write out the instructions added at each step in JSON so we can use it later.
with open('implementationOrderMnemonics.json','w+') as mnemonicFileJSON:
	mnemonicFileJSON.write(json.dumps(steps, indent=4, sort_keys=True))



# # Now comes the task of figuring out how many packages are supported as each
# # instruction is added.
# steps = {}
# stepNum = 0
# numSupportedPackages = 0
# numSupportedOpcodes = 0
# numerator = 0.0
# with open('implementationOrderOpcodes.csv', 'w+') as opcodeFileCSV:
# 	opcodeFileCSV.write("numOpcodes,numPackages, weightedCompleteness\n")
# 	newlyAdded = []
# 	while packageOpcodes:
# 		# Calculate Deltas for all the packages
# 		deltas = []
# 		for package in packageOpcodes:
# 			deltas.append((len(packageOpcodes[package]),package))
# 		deltas = sorted(deltas)
# 		numNewOpcodes, packageSelected = deltas[0]
# 		newlyAdded = packageOpcodes.pop(packageSelected)
# 		numSupportedPackages += 1
# 		numSupportedOpcodes += numNewOpcodes
# 		# Remove newly added opcodes from the lists to reduce our input on
# 		# each round
# 		popMe = []
# 		for package in packageOpcodes:
# 			for opcode in newlyAdded:
# 				packageOpcodes[package].discard(opcode)
# 				if len(packageOpcodes[package]) == 0:
# 					numSupportedPackages += 1
# 					popMe.append(package)
# 		newlySupportedPackages = []
# 		newlySupportedPackages.append(packageSelected)
# 		for package in popMe:
# 			packageOpcodes.pop(package,None)
# 			newlySupportedPackages.append(package)
# 		# Calculate Weighted Completeness
# 		for package in newlySupportedPackages:
# 			numerator += pInst[package]
# 		weightedCompleteness = numerator/denominator
# 		pack = {}
# 		pack['stepNum'] = stepNum
# 		pack['weightedCompleteness'] = weightedCompleteness
# 		pack['numSupportedOpcodes'] = numSupportedOpcodes
# 		pack['numSupportedPackages'] = numSupportedPackages
# 		pack["newlyAddedOpcodes"] = list(newlyAdded)
# 		pack["newlySupportedPackages"] = newlySupportedPackages
# 		steps[stepNum] = pack
# 		stepNum += 1
# 		opcodeFileCSV.write(str(numSupportedOpcodes)+","+str(numSupportedPackages)+","+str(weightedCompleteness)+"\n")

# # Write out the instructions added at each step in JSON so we can use it later.
# with open('implementationOrderOpcodes.json','w+') as opcodeFileJSON:
# 	opcodeFileJSON.write(json.dumps(steps, indent=4, sort_keys=True))