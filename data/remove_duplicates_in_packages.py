import json
import sys

packageFile = open(sys.argv[1], 'r+')
data = json.loads(packageFile.read())
packageFile.close()

packageDict = {}
newList = []

for package in data['packages']:
	if package['name'] in packageDict:
		continue
	else:
		packageDict[package['name']] = True
		newList.append(package)

data['packages'] = newList
# print data['packages']

with open(sys.argv[1], 'w+') as packageFile:
	packageFile.write(json.dumps(data, indent=4, sort_keys=True))
packageFile.close()
