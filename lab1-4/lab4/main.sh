#!/bin/bash

tail -n +2 projects.csv | while IFS= read -r line; do
	project=$line; 
	project=${project##*/}
	project=`echo $project | cut -d"," -f1`
	line=`echo $line | cut -d"," -f2`
	git clone $line
	bash analysis.sh $project
done
