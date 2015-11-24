#/bin/bash
##################################################
# Receives 1 argument:
# - path to the folder where the images are stored
# example:
#	./run.sh /folder/with/images/
##################################################

files=$1*
for f in $files
do
	if [ ! -d $f ]; then
  		echo 'Processing' $f
  		python ./src/sampler.py $f
  	fi
done