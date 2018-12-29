import json
import pickle
import os

groupFile = open('groups.json')

groups = json.loads(groupFile.read())

mnemonics = {}
packagesMnemonics = {}
numPackages = 0.0

pmFileExists = os.path.isfile('./packagesMnemonics.pickle')
print pmFileExists
if pmFileExists:
	with open('packagesMnemonics.pickle', 'rb') as handle:
		packagesMnemonics = pickle.load(handle)
		numPackages = len(packagesMnemonics)
print numPackages

mFileExists = os.path.isfile('./mnemonics.pickle')
print mFileExists
if mFileExists:
	with open('mnemonics.pickle', 'rb') as handle:
		mnemonics = pickle.load(handle)

# If either of these pickles doesn't exist, gather the data again.
if (not pmFileExists) or (not mFileExists):
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

	with open('packagesMnemonics.pickle', 'wb') as pmFile:
		pickle.dump(packagesMnemonics, pmFile, protocol=pickle.HIGHEST_PROTOCOL)

	with open('mnemonics.pickle', 'wb') as mFile:
		pickle.dump(mnemonics, mFile, protocol=pickle.HIGHEST_PROTOCOL)


#Read in Pinst.json
pinstFile = open('pinst.json', 'r')
pInst = json.loads(pinstFile.read())

#############################################################################
# weighted_completeness = SUMMATION(PInst(supported)/Summation(PInst(all))) #
# notation :								    #
# PInst(name) -> PInst of all packages falling under the category "name"    #
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
# "DATA", "CONTROL FLOW", "BINARY ARITHMETIC", "MISC", "BITWISE", "LOGICAL", "SHIFT AND ROTATE", "SSE", "STRING", "MMX", "AVX", "FLAG REGISTER INSN", "X87 FPU", "I/O", "BMI1/BMI2", "SYTEM", "AES", "SYSTEM", "AVXAVX", "CLMUL", "ATOMIC", "3DNOW", "RANDOM NUMBER GENERATORS", "TSX", "FLAG REIGSTER INSN", "VMX", "SMX"
baseTags = ["DATA", "CONTROL FLOW", "BINARY ARITHMETIC", "MISC",
		"BITWISE", "LOGICAL", "SHIFT AND ROTATE", "STRING",
		"FLAG REGISTER INSN", "X87 FPU", "I/O", "BMI1/BMI2", "SYTEM",
		"AES", "SYSTEM", "CLMUL", "ATOMIC","RANDOM NUMBER GENERATORS",
		"TSX", "FLAG REIGSTER INSN", "VMX", "SMX"]

extendedTags =  ["SSE", "MMX", "XOP", "3DNOW", "AVX", "AVXAVX"]
# ["MMX", "SSE", "XOP", "3DNOW", "AVX", "AVXAVX"]

# Now comes the task of figuring out how many packages are supported as each
# instruction is added.
supportedMnemonics = []
supportedPackages = []
numSupportedPackages = 0
numerator = 0.0
with open('selectedTagsWCMnem.csv', 'w+') as mnemonicFile:
	mnemonicFile.write("numMnemonics,numPackages,mnemonicImportance, weightedCompleteness\n")
	for ((mnemonic, tag, percentofpackages)) in mnemonicRanked:
		if tag not in baseTags:
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
	print str(len(supportedMnemonics)) + ',' + str(numSupportedPackages) + "," + str(percentofpackages) + "," + str(weightedCompleteness)
	for newTag in extendedTags:
		print "adding "+ newTag
		for ((mnemonic, tag, percentofpackages)) in mnemonicRanked:
			if tag in baseTags:
				continue
			if tag == newTag:
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
		print str(len(supportedMnemonics)) + ',' + str(numSupportedPackages) + "," + str(percentofpackages) + "," + str(weightedCompleteness)
		baseTags.append(newTag)

print packagesMnemonics