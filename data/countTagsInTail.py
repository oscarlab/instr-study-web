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

tagsInTail = {}
for i in range(171, 453):
	mnemonicsAdded = steps[str(i)]['newlyAddedMnemonics']
	for mnemonic in mnemonicsAdded:
		try:
			tag = tags[mnemonic]
		except KeyError, e:
			print 'I got a KeyError - reason "%s"' % str(e)
		if tag in tagsInTail.keys():
			tagsInTail[tag] += 1
		else:
			tagsInTail[tag] = 1

tagsSorted = sorted([(count, tag) for (tag, count) in tagsInTail.items()],
	reverse = True)

with open('tagsInTail.csv', 'w') as tagsinTailFile:
	tagsinTailFile.write('tag, count\n')
	for (count, tag) in tagsSorted:
		tagsinTailFile.write(str(tag)+','+str(count)+'\n')
	tagsinTailFile.close()


