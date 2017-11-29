import json

input = open('grouped_data.json', 'r+')
# output = open('data2.json', 'w+')

insns = json.loads(input.read())
# input.close()

for insn in insns['instructions']:
	with open('grouped_packages/'+str(insn['id'])+'.json', 'r+') as package_file:
		data = json.loads(package_file.read())
		insn['package_count'] = len(data['packages'])
		package_file.close()

input.seek(0)
input.write(json.dumps(insns, indent=4, sort_keys=True))
input.close()


# input = open(sys.argv[1], 'r')


# insns = json.loads(input.read())
# new_insns = {}
# new_insns['instructions'] = []

# for insn in insns['instructions']:
# 	# delete invalid Instructions
# 	if insn['tag'] == "None":
# 		continue
# 	#seperate sources from the data.json
# 	if 'sources' not in insn.keys():
# 		print json.dumps(insn, indent=4, sort_keys=True)
# 	sources = {}
# 	sources['id'] = insn['id']
# 	sources['sources'] = insn.pop('sources')
# 	#write out sources
# 	filename = 'insn_sources/'+ str(insn['id']) +".json"
# 	with open(filename, 'w+') as package_file:
# 		package_file.write(json.dumps(sources, indent=4, sort_keys=True))
# 	#update instructions dict
# 	new_insns['instructions'].append(insn)

# output.write(json.dumps(new_insns, indent=4, sort_keys=True))