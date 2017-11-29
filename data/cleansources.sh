#! /bin/bash
for file in ./sources/*.json
do
	  python ./split_sources_temp_deleteme.py $file
  done
