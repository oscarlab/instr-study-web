import json

groupFile = open('groups.json')

groups = json.loads(groupFile.read())

mnemonics = {}
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
			numPackages += 1.0
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

# Read in the importance from opcoderanked and mnemonicranked.

mnemonicRanked = []
with open('mnemonicranked.csv', 'r') as mnemonicRankedFile:
	mnemonicRankedFile.readline() # get rid of header.
	for line in mnemonicRankedFile:
		mnemonic, tag, percentofpackages = line.strip().split(',')
		mnemonicRanked.append((mnemonic, tag, percentofpackages))
	mnemonicRankedFile.close()

# Set this with tags you want to check.
supportedTags = ["SYSTEM", "DATA", "CONTROL FLOW", "BINARY ARITHMETIC", "BITWISE", "MISC", "LOGICAL", "SHIFT AND ROTATE", "SSE", "STRING",  "I/O", "FLAG REGISTER INSN", "X87 FPU", "MMX"]

# Now comes the task of figuring out how many packages are supported as each
# instruction is added.

supportedMnemonics = []
supportedPackages = []
numSupportedPackages = 0
numerator = 0.0
with open('selectedTagsWCMnem.csv', 'w+') as mnemonicFile:
	mnemonicFile.write("numMnemonics,numPackages,mnemonicImportance, weightedCompleteness\n")
	for ((mnemonic, tag, percentofpackages)) in mnemonicRanked:
		if tag not in supportedTags:
			continue
		supportedMnemonics.append(mnemonic)
		# temporary list of packages to remove from the packageDict after
		# iteration (to avoid going over satisfied packages.)
		popMe = []
		for package in packagesMnemonics:
			packagesMnemonics[package].discard(mnemonic)
			if len(packagesMnemonics[package]) == 0:
				numSupportedPackages += 1
				supportedPackages.append(package)
				popMe.append(package)
		for package in popMe:
			packagesMnemonics.pop(package,None)
			numerator += pInst[package]
		weightedCompleteness = numerator/denominator
		mnemonicFile.write(str(len(supportedMnemonics)) + ',' + str(numSupportedPackages) + "," + str(percentofpackages) + "," + str(weightedCompleteness) + "\n")