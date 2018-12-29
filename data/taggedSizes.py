import json
import pickle
import os

groupFile = open('groups.json')

groups = json.loads(groupFile.read())

sizesByTag = {}

pickleExists = os.path.isfile('./sizesByTag.pickle')
if pickleExists:
	with open('sizesByTag.pickle', 'rb') as handle:
		sizesByTag = pickle.load(handle)

# If either of these pickles doesn't exist, gather the data again.
if (not pickleExists):
	sizesByTag = {}
	numPackages = 0.0
	for group in groups:
		for package in groups[group]:
			with open('packages_sourced/'+package['name']+'.json','r') as packageFile:
				packageData = json.loads(packageFile.read())
				for insn in packageData['instructions']:
					tag = insn['tag']
					size = insn['size']
					if size in sizesByTag.keys():
						if tag in sizesByTag[size].keys():
							sizesByTag[size][tag] += insn['count']
						else:
							sizesByTag[size][tag] = insn['count']
					else:
						sizesByTag[size] = {}
						sizesByTag[size][tag] = insn['count']
				packageFile.close()

	with open('sizesByTag.pickle', 'wb') as pmFile:
		pickle.dump(sizesByTag, pmFile, protocol=pickle.HIGHEST_PROTOCOL)

totalInsns = 0
tags = dict()
for size in sizesByTag.keys():
	for tag in sizesByTag[size].keys():
		if tag == "FLAG REIGSTER INSN":
			tag = "FLAG REGISTER INSN"
		if tag not in tags.keys():
			tags[tag] = dict()
		tags[tag][size] = sizesByTag[size][tag]
		if 'total' not in tags[tag].keys():
			tags[tag]['total'] = sizesByTag[size][tag]
		else:
			tags[tag]['total'] += sizesByTag[size][tag]
		totalInsns += sizesByTag[size][tag]

with open('sizesByTag.csv', 'w+') as outFile:
	# outFile.write("tag,size,totalPercentage,tagPercentage\n")
	for tag in tags.keys():
		for size in tags[tag].keys():
			outFile.write(tag+","+str(size)+","+str(round((tags[tag][size]*100.0)/(totalInsns*1.0),1))+","+str(round((tags[tag][size]*100.0)/(tags[tag]['total']*1.0),1))+"\n")