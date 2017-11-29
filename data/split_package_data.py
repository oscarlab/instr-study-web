import json
input = open('data_complete.json')
popularity = open('package_popularity.csv')
output = open('data.json', 'w+')

popDict = {}
for line in popularity:
	package_name, rank, inst = line.strip().split(",")
	popDict[package_name] = [int(rank),int(inst)]

# #throw away first 2 lines due to formatting that psql insists on including
# input.readline()
# input.readline()

ID = 1
output.write("{\n\"instructions\":\n[\n")
for line in input:
	data = json.loads(line)
	data["id"] = ID
	data["package_count"] = len(data["package_name"])
	if len(data['tag']) > 1 :
		print data['tag']
	data['tag'] = data['tag'].pop()
	data2 = {}
	data2["id"] = ID
	data2["package_name"] = data.pop('package_name')
	output.write(json.dumps(data, indent=4, sort_keys=True))
	output.write(",\n")
	packages = []
	for package in data2["package_name"]:
		rank, inst = popDict[package]
		pack = {}
		pack["name"] = package
		pack["rank"] = rank
		pack["installation_count"] = inst
		packages.append(pack)
	data2["package_name"] = packages
	filename = 'packages/'+ str(ID) +".json"
	with open(filename, 'w+') as package_file:
		package_file.write(json.dumps(data2, indent=4, sort_keys=True))
	ID += 1

output.write("]")
