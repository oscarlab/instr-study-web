import os
import json

PInstDict = {}
totalNumInstallations =  2964073.0

for filename in os.listdir('packages_sourced'):
	# print "filename: "+filename
	with open('packages_sourced/'+filename, 'r+') as package_file:
		data = json.loads(package_file.read())
		name = data['name']
		# print "package_name: "+name
		instCount = data['installation_count']
		PInst = (float(instCount)/totalNumInstallations)*100.0
		PInstDict[name] = PInst
		package_file.close()

with open('pinst.json', 'w+') as pinstFile:
	pinstFile.write(json.dumps(PInstDict, indent=4, sort_keys=True))

PInstSorted = sorted(PInstDict.items(), key=lambda (k, v): v, reverse=True)

rankedDict = {}
for i in range(11):
	name = i
	rankedDict[name] = []

# group by probability value, rather than fixed intervals. so >90 80-90 70-80 etc.
for (name, value) in PInstSorted:
	pack = {}
	pack['name'] = name
	pack['probability'] = value
	group = int(value/10)
	if value > 0.98 and value < 10:
		group = 10
	rankedDict[group].append(pack)

with open('groups.json', 'w+') as pinstFile:
	pinstFile.write(json.dumps(rankedDict, indent=4, sort_keys=True))

# numItems = len(PInstDict)
# tenPercent = numItems/10

# rankedDict = {}

# for i in range(0,9):
# 	start = i*tenPercent
# 	end = (i+1)*tenPercent
# 	newList = []
# 	for (name,value) in PInstSorted[start:end]:
# 		newList.append(name)
# 	groupname = 'group'+str(i)
# 	rankedDict[groupname] = newList

# tempList = []
# for (name,value) in PInstSorted[9*tenPercent:]:
# 	tempList.append(name)

# rankedDict['group9'] = tempList

# output.write(json.dumps(rankedDict, indent=4, sort_keys=True))
