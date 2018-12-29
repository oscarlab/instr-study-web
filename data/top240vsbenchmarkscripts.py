import json

mnemonicFile = open('implementationOrderMnemonics.json', 'r+')

steps = json.loads(mnemonicFile.read())

mnemonicFile.close

instructions = []
tags = {}

for i in range(0, 216):
	mnemonicsAdded = steps[str(i)]['newlyAddedMnemonics']
	for mnem in mnemonicsAdded:
		if mnem in instructions:
			continue
		else:
			instructions.append(mnem)

print instructions


mnemonicFile = open('top240_and_benchmarkinsns', 'r+')

mnemonicsBench = []
mnemonicsTop = []
for line in mnemonicFile:
	mnem, source = line.strip().split('_')
	if source == 'benchmark':
		mnemonicsBench.append(mnem)
	elif source == 'top':
		mnemonicsTop.append(mnem)

notInBench = []
for mnem in mnemonicsTop:
	if mnem not in mnemonicsBench:
		notInBench.append(mnem)

notInTop = []
for mnem in mnemonicsBench:
	if mnem not in mnemonicsTop:
		notInTop.append(mnem)

tags = {}
with open('mnem_tagged.csv', 'r') as tagFile:
	for line in tagFile:
		mnemonic, tag = line.strip().split(',')
		tags[mnemonic] = tag

print "notInBench"
for mnem in notInBench:
	try:
		tag = tags[mnem]
		print mnem, tag
	except KeyError, e:
		print 'KeyError - reason "%s"' % str(e)


print "notInTop"
for mnem in notInTop:
	try:
		tag = tags[mnem]
		print mnem, tag
	except KeyError, e:
		print 'KeyError - reason "%s"' % str(e)
