#!/bin/bash

#pre-clean and setup
echo "performing pre-clean and setup..."
rm -rf temp
rm -rf $1_results
rm -f *.xml *.dot
mkdir $1_results

#collect last 100 non-merge commits
python3 getCommits.py $1 > $1_results/$1.commits
python3 getCommitsInfo.py $1

ver=0
cat $1_results/$1.commits | while IFS= read -r line; do
	
	#checkout commit
	python3 checkout.py $1 $line
	
	cp -r $1 $1_results/v${ver}
	ver=$((ver+1))
done

#run SATs on each version
collection=`ls -d $1_results/*/`
for ver in ${collection};
do
	echo "analyzing [$ver]..."
	#TODO (if you are analyzing a version in its entirety)
done

rm -rf $1

