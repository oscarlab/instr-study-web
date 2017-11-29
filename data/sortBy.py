import json

groupFile = open('groups.json')

groups = json.loads(groupFile.read())

packages = {}
for group in groups:
	for package in groups[group]:
		with open('packages_sourced/'+package['name']+'.json','r') as packageFile:
			packageData = json.loads(packageFile.read())
			mnemSet = set([p['mnem'] for p in packageData['instructions']])
			mnemCount = len(mnemSet)
			opcodeSet = set([p['opcode'] for p in packageData['instructions']])
			opcodeCount = len(opcodeSet)
			packages[package['name']] = (package['probability'], mnemCount, opcodeCount)

sortBy = {}
sortBy['MnemCount'] = sorted([(mnemCount, probability, name) for (name, (probability, mnemCount, opcodeCount)) in packages.items()])
sortBy['OpcodeCount'] = sorted([(opcodeCount, probability, name) for (name, (probability, mnemCount, opcodeCount)) in packages.items()])

with open('sortbymnem.csv', 'w') as output2:
	for (mnemCount, probability, name) in sortBy['MnemCount']:
		output2.write(str(mnemCount)+','+str(probability)+','+name+'\n')
	output2.close


with open('sortbyOpcCount.csv', 'w') as output2:
	for (OpcodeCount, probability, name) in sortBy['OpcodeCount']:
		output2.write(str(OpcodeCount)+','+str(probability)+','+name+'\n')
	output2.close
