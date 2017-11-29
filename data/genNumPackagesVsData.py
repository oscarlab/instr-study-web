import json

groupFile = open('groups.json')

groups = json.loads(groupFile.read())

opcodes = {}
mnemonics = {}
packagesOpcodes = {}
packagesMnemonics = {}
numPackages = 0.0
# First aggregate all the opcodes and mnemonics used in each application.
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
			numPackages += 1.0
			packagesOpcodes[package['name']] = opcodeSet
			packagesMnemonics[package['name']] = mnemSet
			packageFile.close()

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

#calculate the order of importance for mnemonics and opcodes
opcodeImportance = {}
for opcode in opcodes:
	packages = opcodes[opcode]
	packagenum = len(packages)
	percentofpackages = (packagenum*100.0)/(numPackages*1.0)
	opcodeImportance[opcode] = percentofpackages

mnemonicImportance = {}
for mnemonic in mnemonics:
	packages = mnemonics[mnemonic]
	packagenum = len(packages)
	percentofpackages = (packagenum*100.0)/(numPackages*1.0)
	mnemonicImportance[mnemonic] = percentofpackages

# Sort the importance by importance of the instructions
# These form the order in which instructions are on the x-axis
opcodeRanked = sorted([(percentofpackages, opcode) for (opcode, percentofpackages) in opcodeImportance.items()], reverse=True)

mnemonicRanked = sorted([(percentofpackages, mnemonic) for (mnemonic, percentofpackages) in mnemonicImportance.items()], reverse=True)

# Now comes the task of figuring out how many packages are supported as each
# instruction is added.
supportedOpcodes = []
numSupportedPackages = 0
numerator = 0.0
with open('NumPackagesVsRankedOpcodes.csv', 'w+') as opcodeFile:
	opcodeFile.write("numOpcodes,numPackages,opcodeImportance, weightedCompleteness\n")
	for (percentofpackages, opcode) in opcodeRanked:
		supportedOpcodes.append(opcode)
		# temporary list of packages to remove from the packageDict after
		# iteration (to avoid going over satisfied packages.)
		popMe = []
		for package in packagesOpcodes:
			packagesOpcodes[package].discard(opcode)
			if len(packagesOpcodes[package]) == 0:
				numSupportedPackages += 1
				popMe.append(package)
		for package in popMe:
			packagesOpcodes.pop(package,None)
			numerator += pInst[package]
		weightedCompleteness = numerator/denominator
		opcodeFile.write(str(len(supportedOpcodes)) + ',' + str(numSupportedPackages) + "," + str(percentofpackages) + "," + str(weightedCompleteness) + "\n")


supportedMnemonics = []
numSupportedPackages = 0
numerator = 0.0
with open('NumPackagesVsRankedMnemonics.csv', 'w+') as mnemonicFile:
	mnemonicFile.write("numMnemonics,numPackages,mnemonicImportance, weightedCompleteness\n")
	for (percentofpackages, mnemonic) in mnemonicRanked:
		supportedMnemonics.append(mnemonic)
		# temporary list of packages to remove from the packageDict after
		# iteration (to avoid going over satisfied packages.)
		popMe = []
		for package in packagesMnemonics:
			packagesMnemonics[package].discard(mnemonic)
			if len(packagesMnemonics[package]) == 0:
				numSupportedPackages += 1
				popMe.append(package)
		for package in popMe:
			packagesMnemonics.pop(package,None)
			numerator += pInst[package]
		weightedCompleteness = numerator/denominator
		mnemonicFile.write(str(len(supportedMnemonics)) + ',' + str(numSupportedPackages) + "," + str(percentofpackages) + "," + str(weightedCompleteness) + "\n")