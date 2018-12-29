import json
from math import sqrt

listOfPackagesFile = open('list')

packageListDict = listOfPackagesFile.read().strip().split(",")

def calc_mean_var_sd(lst, population=True):
    """Calculates the standard deviation for a list of numbers."""
    num_items = len(lst)
    mean = sum(lst) / num_items
    differences = [x - mean for x in lst]
    sq_differences = [d ** 2 for d in differences]
    ssd = sum(sq_differences)
    if population is True:
        variance = ssd / num_items
    else:
        variance = ssd / (num_items - 1)
    sd = sqrt(variance)
    return mean, variance, sd


data = {}
data['instructions'] = []
data['group'] = {}
data['group']['name'] = "benchmarks"
data['group']['count'] = len(packageListDict)

popDict = {}

tempDict = {}
ID = 50359
for package in packageListDict:
	with open('packages_sourced/'+package+'.json', 'r') as package_file:
		packageData = json.loads(package_file.read())
		popDict[str(package)] = []
		popDict[str(package)].append(packageData['rank'])
		popDict[str(package)].append(packageData['installation_count'])
		for insn in packageData['instructions']:
			key = insn['prefix'] + insn['opcode'] + str(insn['size'])
			source = insn['source'].strip().rsplit('/', 1)[1]
			if key in tempDict.keys():
				newInsn = tempDict[key]
				sources = newInsn['sources']
				found = False
				for src in sources:
					if src['name'] == source:
						found = True
						src['count'] += insn['count']
				if found == False:
					pack = {}
					pack['name'] = source
					pack['count'] = insn['count']
					sources.append(pack)
				newInsn['count'] += insn['count']
				newInsn['countArray'].append(insn['count'])
				if package not in newInsn['packages']:
					newInsn['packages'].append(package)
			else:
				if insn['tag'] == None:
					continue
				newInsn = {}
				sources = []
				src = {}
				src['name'] = source
				src['count'] = insn['count']
				sources.append(src)
				newInsn['sources'] = sources
				newInsn['mnem'] = insn['mnem']
				newInsn['prefix'] = insn['prefix']
				newInsn['opcode'] = insn['opcode']
				newInsn['size'] = insn['size']
				newInsn['tag'] = insn['tag']
				newInsn['count'] = insn['count']
				newInsn['countArray'] = []
				newInsn['countArray'].append(insn['count'])
				newInsn['packages'] = []
				newInsn['packages'].append(package)
				tempDict[key] = newInsn
for insn in tempDict.values():
	insn['id'] = ID
	insn['group'] = "benchmarks"
	insn['source_count'] = len(insn['sources'])
	with open('grouped_sources/'+str(ID)+'.json', 'w') as source_file:
		sourceDict = {}
		sourceDict['id'] = ID
		sourceDict['sources'] = insn.pop('sources')
		source_file.write(json.dumps(sourceDict, indent=4, sort_keys=True))
	insn['package_count'] = len(insn['packages'])
	with open('grouped_packages/'+str(ID)+'.json', 'w') as package_file:
		packageDict = {}
		packageDict['id'] = ID
		packageDict['packages'] = []
		tempPackages = insn.pop('packages')
		for package in tempPackages:
			rank, inst = popDict[package]
			pack = {}
			pack["name"] = package
			pack["rank"] = rank
			pack["installation_count"] = inst
			packageDict['packages'].append(pack)
		package_file.write(json.dumps(packageDict, indent=4, sort_keys=True))
	mean, variance, sd = calc_mean_var_sd(insn['countArray'])
	insn['mean'] = mean
	insn['variance'] = variance
	insn['sd'] = sd
	with open('countarray/'+str(ID)+'.json', 'w') as countArrayFile:
		countArrayDict = {}
		countArrayDict['id'] = ID
		countArrayDict['countArray'] = insn.pop('countArray')
		countArrayFile.write(json.dumps(countArrayDict, indent=4, sort_keys=True))
	data['instructions'].append(insn)
	ID += 1

with open('grouped_benchmarks.json', 'w+') as group_file:
	group_file.write(json.dumps(data, indent=4, sort_keys=True))
