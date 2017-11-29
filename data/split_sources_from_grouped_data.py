import json
import os
input = open('grouped_data.json')
output = open('grouped_data2.json', 'w+')

groups = json.loads(input.read())

for group in groups.keys():
	ID = 1
	os.mkdir('./groups/'+group)
	for instruction in groups[group]:
		sources = instruction.pop('sources')
		instruction['source_count'] = len(sources)
		pack = {}
		pack['id'] = ID
		pack['sources'] = sources
		with open('./groups/'+group+'/'+str(ID)+'.json', 'w+') as source_file:
			source_file.write(json.dumps(pack, indent=4, sort_keys=True))
		ID += 1

output.write(json.dumps(groups, indent=4, sort_keys=True))