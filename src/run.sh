#/bin/bash

mkdir output

files=$1*
for f in $files
do
	if [ ! -d $f ]; then
  		echo 'Processing' $f
  		python sampler.py $f
  	fi
done