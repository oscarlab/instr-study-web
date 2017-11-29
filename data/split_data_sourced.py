import json
input = open('data_sourced.json')
popularity = open('package_popularity.csv')
output = open('data.json', 'w+')

popDict = {}
for line in popularity:
	package_name, rank, inst = line.strip().split(",")
	popDict[package_name] = [int(rank),int(inst)]

# {"prefix":"67676748","opcode":"ff","size":6,"mnem":"ADDR32","source":"/lib/x86_64-linux-gnu/libcrypto.so.1.0.0","count":18,"tag":null,"package_name":["fqterm","hostapd","hydra","mixmaster","nmap","nodejs","ntp","opensc","openssl","pgadmin3","qterm","rdesktop","wpasupplicant"]}

curr_running_insn = ""
sources = {}
packages = []
firstLine = True

#this seems a little absurd. Just trying to create the structure JSON expects.
insns = {}
insns['instructions'] = []

ID = 1

for line in input:
	if line == "\n":
		continue
	data = json.loads(line)
	curr_insn = data['prefix'] + "," + data['opcode'] + "," + str(data['size']) + "," + data['mnem'] + "," + str(data['tag'])
	source = data['source'].rsplit('/',1)[1]
	if firstLine == True:
		firstLine = False
		curr_running_insn = curr_insn
		sources[source] = data['count']
		for package in data['package_name']:
			packages.append(package)
	elif curr_insn == curr_running_insn:
		if source in sources:
			sources[source] += data['count']
		else:
			sources[source] = data['count']
		for package in data['package_name']:
			if package not in packages:
				packages.append(package)
	else:
		#new instruction. Write out the current one.
		out_data = {}
		prefix, opcode, size, mnem, tag = curr_running_insn.split(',')
		out_data['prefix'] = prefix
		out_data['opcode'] = opcode
		out_data['size'] = int(size)
		out_data['mnem'] = mnem
		out_data['tag'] = tag
		# Write sources to individual files to keep size down.
		# out_data['sources'] = sources
		out_data['id'] = ID
		out_data['package_count'] = len(packages)
		out_data['count'] = sum(sources.itervalues())
		out_data['sources_count'] = len(sources)
		# Add to the list keeping the JSON. Hope it doesn't grow too big.
		insns['instructions'].append(out_data)
		# Time to write out the package_names
		out_data2 = {}
		out_data2['id'] = ID
		packages_ranked = []
		for package in packages:
			rank, inst = popDict[package]
			pack = {}
			pack["name"] = package
			pack["rank"] = rank
			pack["installation_count"] = inst
			packages_ranked.append(pack)
		out_data2['package_names'] = packages_ranked
		filename = 'packages/'+ str(ID) +".json"
		with open(filename, 'w+') as package_file:
			package_file.write(json.dumps(out_data2, indent=4, sort_keys=True))
				# Time to write out the package_names
		out_sources = {}
		out_sources['id'] = ID
		out_sources['sources'] = []
		for key in sources.keys():
			pack = {}
			pack['name'] = key
			pack['count'] = sources[key]
			out_sources['sources'].append(pack)
		filename = 'sources/'+ str(ID) +".json"
		with open(filename, 'w+') as package_file:
			package_file.write(json.dumps(out_sources, indent=4, sort_keys=True))
		# Update state for the new package.
		curr_running_insn = curr_insn
		sources = {}
		packages = []
		sources[source] = data['count']
		for package in data['package_name']:
			packages.append(package)
		ID +=1
output.write(json.dumps(insns, indent=4, sort_keys=True))




