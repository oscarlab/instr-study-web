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
			mnemSet = set([(p['mnem'], p['tag']) for p in packageData['instructions']])
			for (mnem, tag) in mnemSet:
				if mnem in mnemonics.keys():
					mnemonics[mnem][1].add(package['name'])
				else:
					mnemonics[mnem] = [tag, set(package['name'])]
			opcodeSet = set([(p['opcode'], p['tag']) for p in packageData['instructions']])
			for (opcode, tag) in opcodeSet:
				if opcode in opcodes.keys():
					opcodes[opcode][1].add(package['name'])
				else:
					opcodes[opcode] = [tag, set(package['name'])]
			numPackages += 1.0
			packagesOpcodes[package['name']] = opcodeSet
			packagesMnemonics[package['name']] = mnemSet
			packageFile.close()

#calculate the order of importance for mnemonics and opcodes
opcodeImportance = {}
for opcode in opcodes:
	tag, packages = opcodes[opcode]
	packagenum = len(packages)
	percentofpackages = (packagenum*100.0)/(numPackages*1.0)
	opcodeImportance[opcode] = (tag, percentofpackages)

mnemonicImportance = {}
for mnemonic in mnemonics:
	tag, packages = mnemonics[mnemonic]
	packagenum = len(packages)
	percentofpackages = (packagenum*100.0)/(numPackages*1.0)
	mnemonicImportance[mnemonic] = (tag, percentofpackages)

# Sort the importance by importance of the instructions
# These form the order in which instructions are on the x-axis
opcodeRanked = sorted([(percentofpackages, opcode, tag) for (opcode, (tag,percentofpackages)) in opcodeImportance.items()], reverse=True)

with open('opcoderanked.csv', 'w') as opcodeRankedFile:
	opcodeRankedFile.write('opcode, tag, Percent of Packages depending on Opcode\n')
	for (percentofpackages, opcode, tag) in opcodeRanked:
		opcodeRankedFile.write(str(opcode)+','+str(tag)+','+str(percentofpackages)+'\n')

mnemonicRanked = sorted([(percentofpackages, mnemonic, tag) for (mnemonic, (tag, percentofpackages)) in mnemonicImportance.items()], reverse=True)

with open('mnemonicranked.csv', 'w') as mnemonicRankedFile:
	mnemonicRankedFile.write('mnemonic, Percent of Packages depending on mnemonic\n')
	for (percentofpackages, mnemonic, tag) in mnemonicRanked:
		mnemonicRankedFile.write(str(mnemonic)+','+str(tag)+','+str(percentofpackages)+'\n')