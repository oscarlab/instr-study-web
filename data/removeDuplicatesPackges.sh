#! /bin/bash
for file in ./grouped_packages/*.json
do
	  python ./remove_duplicates_in_packages.py $file
  done
