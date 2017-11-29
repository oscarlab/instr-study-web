import json

mnemonicFile = open('implementationOrderMnemonics.json', 'r+')

steps = json.loads(mnemonicFile.read())

mnemonicFile.close

# mnemonics = 171 - 452

tagFile = open('mnem_tagged.csv', 'r')

tags = {}
for line in tagFile:
	mnemonic, tag = line.strip().split(',')
	tags[mnemonic] = tag

tagFile.close()

tagsInHead = {}
for i in range(0, 172):
	mnemonicsAdded = steps[str(i)]['newlyAddedMnemonics']
	for mnemonic in mnemonicsAdded:
		try:
			tag = tags[mnemonic]
		except KeyError, e:
			print 'I got a KeyError - reason "%s"' % str(e)
		if tag in tagsInHead.keys():
			tagsInHead[tag] += 1
		else:
			tagsInHead[tag] = 1

tagsSorted = sorted([(count, tag) for (tag, count) in tagsInHead.items()],
	reverse = True)

with open('tagsInHead.csv', 'w') as tagsInHeadFile:
	tagsInHeadFile.write('tag, count\n')
	for (count, tag) in tagsSorted:
		tagsInHeadFile.write(str(tag)+','+str(count)+'\n')
	tagsInHeadFile.close()


