import json
import sys
import os
input = open('data_packages_sourced.json')
popularity = open('package_popularity.csv')

popDict = {}
for line in popularity:
	package_name, rank, inst = line.strip().split(",")
	popDict[package_name] = [int(rank),int(inst)]

#get rid of those pesky headers that PSQL insists on putting in.
# input.readline()
# input.readline()

#{"prefix":"f06642","opcode":"89","size":6,"mnem":"MOV","source":"/usr/lib/lazarus/1.6/lazarus-gtk2","count":1,"tag":"DATA","package_name":["lazarus-ide-gtk2-1.6"]}
curr_running_package = ""
last_rank = 361521
instructions = []
firstLine = True

for line in input:
	try:
		data = json.loads(line)
	except Exception as e:
		print line
		continue
	if len(data['tag']) > 1 :
		print data['tag']
	data['tag'] = data['tag'].pop()
	if data['tag'] is None:
		continue
	curr_package = data.pop('package_name')
	if os.path.isfile('packages_sourced/'+ curr_package +".json"):
		continue
	if curr_package == curr_running_package:
		instructions.append(data)
	elif firstLine == True:
		firstLine = False;
		curr_running_package = curr_package
		instructions.append(data)
	else:
		#write out the package we're currently working on.
		pack = {}
		try:
			rank, inst = popDict[curr_running_package]
		except Exception:
			last_rank += 1
			rank = last_rank
			inst = 0
		pack["name"] = curr_running_package
		pack["rank"] = rank
		pack["installation_count"] = inst
		pack["instructions"] = instructions
		filename = 'packages_sourced/'+ curr_running_package +".json"
		with open(filename, 'w+') as package_file:
			package_file.write(json.dumps(pack, indent=4, sort_keys=True))
		# Update state for the new package.
		instructions = []
		curr_running_package = curr_package
		instructions.append(data)